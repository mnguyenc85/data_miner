# Format .csv:
#   sort by gmt7 or dateline

import pandas as pd
from datetime import datetime, timedelta
import json

dataFolder = './data/'
week = timedelta(days=7)
timeZoneMq5 = timedelta(hours=11)

def get1stWeek(year: int) -> datetime:
    # 2000 -> 2030
    sun = [ 2, 7, 6, 5, 4, 2, 1, 7, 6, 4, 3, 2, 1, 6, 5, 4, 3, 1, 7, 6, 5, 3, 2, 1, 7, 5, 4, 3, 2, 7, 6 ]
    if year >= 2000 and year <= 2030:
        return datetime(year=year, month=1, day=sun[year - 2000])
    return None

def getWeek(d: datetime) -> datetime:
    """ Return first day (Sunday) of week """
    return d - timedelta(days=((d.weekday() + 1) % 7))

def loadYear(year: int):
    df = pd.read_csv(f'{dataFolder}ff{year}.csv')
    df = df.astype({ 'currency': str, 'impact': str, 'timeLabel': str, 'name': str, 'actual': str, 'forecast': str, 'previous': str })
    return df

def examineCsv(df: pd.DataFrame):
    # print(df.shape)
    print(df.info())
    print(df.head())
    isSortedByGmt7 = df['gmt7'].is_monotonic_increasing
    print(f'Is gmt7 sorted: {isSortedByGmt7}')
    # print(df['impact'].unique())

def parseImpact(s: str) -> str:
    if s.startswith('Low'): return 'Low'
    elif s.startswith('Medium'): return 'Medium'
    elif s.startswith('High'): return 'High'
    elif s.startswith('Non'): return 'Non'
    else: return s
    # elif s.startswith('Very high'): return 'Very High'

def saveToDat(year: int, startDate = None, endDate = None):
    '''
    Load data from .csv va save vao file .dat
    Args:
        year: nam can load
        startDate: tuan bat dau: None -> tuan dau tien cua nam
        endDate: tuan ket thuc: None -> het ca nam (1/1/year+1)
    '''
    
    df = loadYear(year)    

    # Sort by dateline
    df = df.sort_values(by=['dateline'], ignore_index=True)    
    
    # For each week
    w0 = get1stWeek(year) if startDate is None else getWeek(startDate)
    wend = datetime(day=1, month=1, year=year+1) if endDate is None else endDate

    while w0 < wend:
        w1 = w0 + week
        w_df = df[(df['dateline'] >= w0.timestamp()) & (df['dateline'] < w1.timestamp())]
        if w_df.shape[0] > 0:
            print(f'Week {w0} has {w_df.shape[0]} events')
            events = []
            for r in w_df.itertuples(index=False, name=None):
                e = {}
                e['title'] = r[5]
                e['country'] = r[2]
                dt = datetime.fromtimestamp(r[1])
                e['date'] = (dt - timeZoneMq5).strftime('%Y-%m-%dT%H:%M:%S-04:00')
                e['impact'] = parseImpact(r[3])
                e['forecast'] = r[7]
                e['previous'] = r[8]
                if e['impact'] is not None: events.append(e)

            key = w0.strftime('%Y.%m.%d')
            val = json.dumps(events, separators=(',', ':'))
            fn = f'{dataFolder}{key}.dat'
            
            txt = json.dumps({key: val}, separators=(',', ':'))
            f = open(fn, "w")
            f.write(txt)
            f.close()

            print(f'   --> Save to {fn}')

        w0 = w1

# ff_df = loadYear(2006)
saveToDat(2006)
saveToDat(2007)
saveToDat(2008)
saveToDat(2009)
saveToDat(2010)
saveToDat(2011)
saveToDat(2012)
saveToDat(2013)
saveToDat(2014)
saveToDat(2015)
saveToDat(2016)
saveToDat(2017)
saveToDat(2018)
saveToDat(2019)
saveToDat(2020)
saveToDat(2021)
saveToDat(2022)
saveToDat(2023)
saveToDat(2024, None, datetime(day=1,month=4,year=2024))
