# Lấy dữ liệu từ forexfactory, sử dụng cloudscraper

from datetime import datetime, timedelta
from ffscraper import parseNSave, parseNSaveCsv
import cloudscraper

rootdir = './data/'
# Theo cài đặt trên trang web: - timeZone - 4???
timeZone = timedelta(hours=7)
timeZoneMq5 = timedelta(hours=11)
oneweek = timedelta(days=7)

def crawlff_selenium(startDate: datetime, endDate: datetime, saveCSV = False):
    '''
    Lay du lieu tu forexfactory, bat dau tu startDate den endDate
    Args:
        startDate: phai la chu nhat
        saveCSV: true -> luu vao file .csv theo nam, false -> luu vao file .dat theo tuan
    '''
    noerr = 0
    scraper = cloudscraper.create_scraper(
        browser = {
            'browser': 'firefox',
            'platform': 'windows',
            'mobile': False
        },
        debug=False
    )

    while startDate < endDate:
        print(f'Mine week: {startDate.strftime('%a %Y/%m/%d')}')
        # url = 'https://www.forexfactory.com/calendar?week=feb25.2024'
        url = f'https://www.forexfactory.com/calendar?week={startDate.strftime('%b%d.%Y')}'
        
        html = scraper.get(url).text

        if html:
            if saveCSV == True:
                fn = f'{rootdir}ff{startDate.strftime('%Y')}.csv'
                noerr += parseNSaveCsv(html, fn)
            else:
                noerr += parseNSave(html)
        else:
            print(f'No response')
            noerr += 1
        startDate = startDate + oneweek

    print(f"No. error: {noerr}")

crawlff_selenium(datetime(year=2025, month=1, day=5), datetime(year=2025,month=3,day=1), True)