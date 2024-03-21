# Extract data from forexfactory.com
# Date: 2024/03/21
# Usage:
#   Ví dụ: mở https://www.forexfactory.com/calendar?week=mar17.2024
#   vào developer tools -> network -> https://www.forexfactory.com/calendar?week=mar17.2024
#   copy toàn bộ
#   chạy python

import win32clipboard
import re
import json
from datetime import datetime, timedelta
import requests

rootdir = './data/'
# Theo cài đặt trên trang web: - timeZone - 4???
timeZone = timedelta(hours=-11)
oneweek = timedelta(days=7)

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
    elif s.startswith('Non'): return 'Non'
    else: return ''
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

def parseNSave():
    jDays = extractData(getClipboard())
    print(f'Number of found blocks: {len(jDays)}')
    for s in jDays:
        days = json.loads(s)
        tn_events, tn_sow = convertToDatFile(days)    
        sow = datetime.fromtimestamp(tn_sow)

        key = sow.strftime('%Y.%m.%d')
        val = json.dumps(tn_events, separators=(',', ':'))
        fn = f'{rootdir}{key}.dat'
        
        txt = json.dumps({key: val}, separators=(',', ':'))
        f = open(fn, "w")
        f.write(txt)
        f.close()
        
        print(f'Save to {fn}')

def crawlff(startDate: datetime, endDate: datetime):
    """ startDate must be Sunday """
    while startDate < endDate:
        # url = 'https://www.forexfactory.com/calendar?week=feb25.2024'
        url = f'https://www.forexfactory.com/calendar?week={startDate.strftime('%b%d.%Y')}'
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36' }
        x = requests.get(url, headers=headers)
        if x.status_code == 200:
            txt = x.content.decode()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(txt, win32clipboard.CF_TEXT)
            win32clipboard.CloseClipboard()
            parseNSave()
        else:
            print(x.status_code)
        startDate = startDate + oneweek

# Lay du lieu tung nam tu nam 2007
# crawlff(datetime(year=2007,month=1,day=7), datetime(year=2008,month=1,day=1))
# crawlff(datetime(year=2008,month=1,day=6), datetime(year=2009,month=1,day=1))
# crawlff(datetime(year=2009,month=1,day=4), datetime(year=2010,month=1,day=1))
# crawlff(datetime(year=2010,month=1,day=3), datetime(year=2011,month=1,day=1))
# crawlff(datetime(year=2011,month=1,day=2), datetime(year=2012,month=1,day=1))
# crawlff(datetime(year=2012,month=1,day=1), datetime(year=2013,month=1,day=1))
# crawlff(datetime(year=2013,month=1,day=6), datetime(year=2014,month=1,day=1))
# crawlff(datetime(year=2014,month=1,day=5), datetime(year=2015,month=1,day=1))
# crawlff(datetime(year=2015,month=1,day=4), datetime(year=2016,month=1,day=1))
# crawlff(datetime(year=2016,month=1,day=3), datetime(year=2017,month=1,day=1))
# crawlff(datetime(year=2017,month=1,day=1), datetime(year=2018,month=1,day=1))
# crawlff(datetime(year=2018,month=1,day=7), datetime(year=2019,month=1,day=1))
# crawlff(datetime(year=2019,month=1,day=6), datetime(year=2020,month=1,day=1))
# crawlff(datetime(year=2020,month=1,day=5), datetime(year=2021,month=1,day=1))
# crawlff(datetime(year=2021,month=1,day=3), datetime(year=2022,month=1,day=1))
# crawlff(datetime(year=2022,month=1,day=2), datetime(year=2023,month=1,day=1))
crawlff(datetime(year=2023,month=1,day=1), datetime(year=2024,month=1,day=1))
# crawlff(datetime(year=2024,month=1,day=7), datetime(year=2024,month=3,day=21))
