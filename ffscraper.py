# Extract data from forexfactory.com
# Date: 2024/03/21

import win32clipboard
import re
import json
from datetime import datetime, timedelta

rootdir = ''
# Theo cài đặt trên trang web
timeZone = 7

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

def convertToDatFile(days):
    """ Chuyen doi tuong trich tu html sang doi tuong dung cho Expert 'trading_news' """
    events = []
    for d in days:
        for e in d['events']:            
            tne = {}
            tne['title'] = e['name']
            tne['country'] = e['currency']
            dt = datetime.strptime(f'{e['date']} {e['timeLabel']}', '%b %d, %Y %I:%M%p')
            # Need recheck!!!
            tne['date'] = (dt - timedelta(hours=timeZone)).strftime('%Y-%m-%d %H:%M:%S')
            tne['impact'] = getImpact(e['impactTitle'])
            tne['forecast'] = e['forecast']
            tne['previous'] = e['previous']
            events.append(tne)

    return events

# for s in findJavascript(getClipboard()):
#     data = extractData(s)
#     if data is not None and len(data) > 0:
#         print(s)
#         print(data)

# cb = getClipboard()
# data = extractData(cb)
# for s in data:
#     print(s)
#     arr_events = json.loads(s)
#     for e in arr_events:
#         print(e)

# 1709325000

# dt = datetime.strptime('Mar 2, 2024 3:30am', '%b %d, %Y %I:%M%p')
# print(dt)
# dt1 = datetime.fromtimestamp(1709325000)
# print(dt1)