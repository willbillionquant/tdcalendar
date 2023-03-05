import os
codepath_td = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append('..')

from datetime import datetime
from itertools import product

from tdcalendar import *

def getMonthExpiry_hk(month, form='%Y-%m-%d'):
    """Obtain HK monthly FOPs expiry, defined as 2nd last HK trading day in a calendar month."""
    if type(month) == tuple:  # e.g. (2021, 1)
        monthStart = datetime(month[0], month[1], 1)
        month = monthStart.strftime('%Y-%m')
    elif type(month) == str:
        if len(month) == 6: # e.g. JAN-21
            monthStart = datetime.strptime(month, '%b-%y')
            month = monthStart.strftime('%Y-%m')
        else:  # e.g. 2021-01
            monthStart = datetime.strptime(f'{month}-01', '%Y-%m-%d')
    else:
        raise AttributeError(f'Input for month must be %b-%y, %Y-%m or (%Y, %m)')
    year = monthStart.year
    holidayList_year = [date for date in holidayList_hk if date.year == year]
    if holidayList_year != []:
        tDayList = getTradingDays(holidayList_hk, datetime(year, 1, 1), datetime(year, 12, 31))
        tDayList = [dayStr for dayStr in tDayList if dayStr[:7] == month]
        return datetime.strptime(tDayList[-2], '%Y-%m-%d').strftime(form)
    else:
        raise AttributeError(f'HK Holiday for year {year} NOT available!')

expiryFile_hk = os.path.join(codepath_td, 'monthexpiry_hk.csv')
expiryDict_hk = {}

if os.path.exists(expiryFile_hk):
    with open(expiryFile_hk, 'r') as f:
        expiryLines_hk = f.readlines()
        expiryDict_hk = {}
        for row in expiryLines_hk:
            monthStart = datetime.strptime(row[:7], '%Y-%m')
            monthStr = monthStart.strftime('%b-%y').upper()
            expiryDict_hk[monthStr] = row[:-1]
else:
    with open(expiryFile_hk, 'w') as f:
        for year, month in product(range(2007, 2047), range(1, 13)):
            try:
                monthStr = (datetime(year, month, 1).strftime('%b-%y')).upper()
                expiry = getMonthExpiry_hk(monthStr)
                expiryDict_hk[monthStr] = expiry
                f.writelines(f'{expiry}\n')
            except:
                break

expiryDateDict_hk = {yrmonth: datetime.strptime(expiry, '%Y-%m-%d') for yrmonth, expiry in expiryDict_hk.items()}

expiryList_hk = list(expiryDict_hk.values())
expiryList_hk.sort()

expiryDateList_hk = [datetime.strptime(dayStr, '%Y-%m-%d') for dayStr in expiryList_hk]
expiryDateList_hk.sort()

