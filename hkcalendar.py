import os
codepath_td = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append('..')

from datetime import datetime
from itertools import product

from tdcalendar import *

def gethkexpiry(monthstr='JAN-21'):
    """Obtain HK monthly expiry day in a month."""
    monthstart = datetime.strptime(monthstr, '%b-%y')
    monthstr = monthstart.strftime('%Y-%m')
    year = monthstart.year
    holidaylistyr = [date for date in holidaylist_hk if date.year == year]
    if holidaylistyr != []:
        tdaylist = gettradedays(holidaylist_hk, datetime(year, 1, 1), datetime(year, 12, 31))
        tdaylist = [dtstr for dtstr in tdaylist if dtstr[:7] == monthstr]
        return tdaylist[-2]
    else:
        raise AttributeError(f'HK Holiday for year {year} NOT available!')

hkexpiryfile = os.path.join(codepath_td, 'monthexpiry_hk.csv')
hkexpirydict = {}

if os.path.exists(hkexpiryfile):
    with open(hkexpiryfile, 'r') as f:
        hkexpirylines = f.readlines()
        hkexpirydict = {}
        for row in hkexpirylines:
            monthstart = datetime.strptime(row[:7], '%Y-%m')
            monthstr = monthstart.strftime('%b-%y').upper()
            hkexpirydict[monthstr] = row[:-1]
else:
    with open(hkexpiryfile, 'w') as f:
        for year, month in product(range(2007, 2047), range(1, 13)):
            try:
                monthstr = (datetime(year, month, 1).strftime('%b-%y')).upper()
                expiry = gethkexpiry(monthstr)
                hkexpirydict[monthstr] = expiry
                f.writelines(f'{expiry}\n')
            except:
                break

hkexpirylist = list(hkexpirydict.values())
hkexpirylist.sort()

