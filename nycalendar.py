import os
codepath_td = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append('..')

from datetime import datetime, timedelta
from itertools import product

from tdcalendar import *

def getMonthExpiry_ny(monthStr='JAN-21'):
    """
    Obtain US monthly option expiry, defined as 3rd Friday or (in case holiday itself) the last trading day
    prior to 3rd Friday.
    """
    monthStart = datetime.strptime(monthStr, '%b-%y')
    expiryDate = datetime.strptime(monthStr, '%b-%y')
    while ((expiryDate.day // 7 != 2) or (expiryDate.weekday() != 4)):
        expiryDate += timedelta(days=1)

    holidayList_year = [date for date in holidayList_ny if date.year == year]

    if holidayList_year == []:
        raise AttributeError(f'US Holiday for year {year} NOT available!')
    else:
        if expiryDate in holidayList_ny:
            tdlist = getTradingDays(holidayList_ny, monthStart, expiryDate)
            expiry = tdlist[-1]
        else:
            expiry = expiryDate.strftime('%Y-%m-%d')

        return expiry

expiryFile_ny = os.path.join(codepath_td, 'monthexpiry_ny.csv')
expiryDict_ny = {}

if os.path.exists(expiryFile_ny):
    with open(expiryFile_ny, 'r') as f:
        expiryLines_ny = f.readlines()
        expiryDict_ny = {}
        for row in expiryLines_ny:
            monthStart = datetime.strptime(row[:7], '%Y-%m')
            monthStr = monthStart.strftime('%b-%y').upper()
            expiryDict_ny[monthStr] = row[:-1]
else:
    with open(expiryFile_ny, 'w') as f:
        for year, month in product(range(1999, 2047), range(1, 13)):
            try:
                monthStr = (datetime(year, month, 1).strftime('%b-%y')).upper()
                expiry = getMonthExpiry_ny(monthStr)
                expiryDict_ny[monthStr] = expiry
                f.writelines(f'{expiry}\n')
            except:
                break

expiryList_ny = list(expiryDict_ny.values())
expiryList_ny.sort()

expiryDateList_ny = [datetime.strptime(dayStr, '%Y-%m-%d') for dayStr in expiryList_ny]
expiryDateList_ny.sort()

