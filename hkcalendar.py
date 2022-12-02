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
    tdaylist = gettradedays(holidaylist_hk, datetime(year, 1, 1), datetime(year, 12, 31))
    tdaylist = [dtstr for dtstr in tdaylist if dtstr[:7] == monthstr]
    return tdaylist[-2]

hkexpiryfile = os.path.join(codepath_td, 'monthexpiry_hk.csv')

if os.path.exists(hkexpiryfile):
    with open(hkexpiryfile, 'r') as f:
        hkexpirylines = f.readlines()
        hkexpirydict = {}
        for row in hkexpirylines:
            monthstart = datetime.strptime(row[:7], '%Y-%m')
            monthstr = monthstart.strftime('%b-%y').upper()
            hkexpirydict[monthstr] = row[:-1]

    hkexpirylist = list(hkexpirydict.values())
    hkexpirylist.sort()

else:
    hkexpirydict = {}

    for year, month in product(range(2007, 2047), range(1, 13)):
        try:
            monthstr = (datetime(year, month, 1).strftime('%b-%y')).upper()
            hkexpirydict[monthstr] = gethkexpiry(monthstr)
        except:
            print(f'HK holiday for year {year} NOT available.')
            break

