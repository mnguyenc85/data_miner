# Extract data from forexfactory.com sử dụng selenium
# Date: 2024/03/21

from datetime import datetime, timedelta
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from ffscraper import parseNSave, parseNSaveCsv

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

    while startDate < endDate:
        print(f'Mine week: {startDate.strftime('%a %Y/%m/%d')}')
        # url = 'https://www.forexfactory.com/calendar?week=feb25.2024'
        url = f'https://www.forexfactory.com/calendar?week={startDate.strftime('%b%d.%Y')}'
        
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(10)
        html = driver.page_source
        driver.quit()

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


# Lấy dữ liệu năm 2025
# crawlff_selenium(get1stWeek(2025), datetime(year=2026,month=1,day=1), False)
crawlff_selenium(datetime(year=2025, month=1, day=12), datetime(year=2025,month=3,day=1), False)
        
