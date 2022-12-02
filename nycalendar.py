import os
codepath_td = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append('..')

from datetime import datetime, timedelta
from itertools import product

from tdcalendar import *

def getnymonthexpiry(monthstr='JAN-21'):
    """
    Obtain US monthly option expiry, defined as 3rd Friday or (in case holiday itself) the last trading day
    prior to 3rd Friday.
    """
    monthstart = datetime.strptime(monthstr, '%b-%y')
    expirydate = datetime.strptime(monthstr, '%b-%y')
    while ((expirydate.day // 7 != 2) or (expirydate.weekday() != 4)):
        expirydate += timedelta(days=1)

    holidaylistyr = [date for date in holidaylist_ny if date.year == year]

    if holidaylistyr == []:
        raise AttributeError(f'US Holiday for year {year} NOT available!')
    else:
        if expirydate in holidaylist_ny:
            tdlist = gettradedays(holidaylist_ny, monthstart, expirydate)
            expiry = tdlist[-1]
        else:
            expiry = expirydate.strftime('%Y-%m-%d')

        return expiry

nyexpiryfile = os.path.join(codepath_td, 'monthexpiry_ny.csv')
nyexpirydict = {}

if os.path.exists(nyexpiryfile):
    with open(nyexpiryfile, 'r') as f:
        nyexpirylines = f.readlines()
        nyexpirydict = {}
        for row in nyexpirylines:
            monthstart = datetime.strptime(row[:7], '%Y-%m')
            monthstr = monthstart.strftime('%b-%y').upper()
            nyexpirydict[monthstr] = row[:-1]
else:
    with open(nyexpiryfile, 'w') as f:
        for year, month in product(range(1999, 2047), range(1, 13)):
            try:
                monthstr = (datetime(year, month, 1).strftime('%b-%y')).upper()
                expiry = getnymonthexpiry(monthstr)
                nyexpirydict[monthstr] = expiry
                f.writelines(f'{expiry}\n')
            except:
                break

nyexpirylist = list(nyexpirydict.values())
nyexpirylist.sort()



