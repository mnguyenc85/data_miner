# Extract data from forexfactory.com
# Date: 2024/03/21
# Usage:
#   Ví dụ: mở https://www.forexfactory.com/calendar?week=mar17.2024
#   vào developẻ tools -> network -> https://www.forexfactory.com/calendar?week=mar17.2024
#   copy toàn bộ
#   chạy python

import win32clipboard
import re
import json
from datetime import datetime, timedelta

rootdir = './data/'
# Theo cài đặt trên trang web: - timeZone - 4???
timeZone = timedelta(hours=-11)

def getClipboard() -> str:
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


def findJavascript(s: str):
    """ Trích javascript code từ html """
    return re.findall(r'<script\b[^>]*>[\s\S]*?<\/script\b[^>]*>', s)

def extractData(s: str):
    """ Trích dữ liệu năm giữa 'days:' và 'time:' """
    return re.findall(r'(?<=days:)[\S\s]*?(?=,\s*time:)', s)

def getImpact(s: str) -> str:
    if s.startswith('Low'): return 'Low'
    elif s.startswith('Medium'): return 'Medium'
    elif s.startswith('High'): return 'High'
    # elif s.startswith('Very high'): return 'Very High'

def convertTime(tstr: str):
    tstr = tstr.lower()
    if tstr == 'all day': 
        return timedelta()
    # elif tstr == '22nd-23rd':
    #     pass
    else:
        t:datetime = datetime.strptime(tstr, "%I:%M%p")
        return timedelta(hours=t.hour, minutes=t.minute)


def convertToDatFile(days):
    """ Chuyen doi tuong trich tu html sang doi tuong dung cho Expert 'trading_news' """
    startOfWeek = None
    events = []
    for d in days:
        startOfWeek = d['dateline'] if startOfWeek is None else min(startOfWeek, d['dateline'])
        for e in d['events']:            
            tne = {}
            tne['title'] = e['name']
            tne['country'] = e['currency']
            dt = datetime.fromtimestamp(e['dateline'])
            tne['date'] = (dt - timeZone).strftime('%Y-%m-%dT%H:%M:%S-04:00')
            tne['impact'] = getImpact(e['impactTitle'])
            tne['forecast'] = e['forecast']
            tne['previous'] = e['previous']
            events.append(tne)

    return events, startOfWeek

jDays = extractData(getClipboard())
print(f'Number of found blocks: {len(jDays)}')
for s in jDays:
    days = json.loads(s)
    tn_events, tn_sow = convertToDatFile(days)    
    sow = datetime.fromtimestamp(tn_sow)

    key = sow.strftime('%Y.%M.%d')
    val = json.dumps(tn_events, separators=(',', ':'))
    fn = f'{rootdir}{key}.dat'
    
    txt = json.dumps({key: val}, separators=(',', ':'))
    f = open(fn, "w")
    f.write(txt)
    f.close()
    
    print(f'Save to {fn}')
