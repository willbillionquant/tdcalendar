import os
codepath_td = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append('..')

from datetime import datetime

from tdcalendar import *

def gethkexpiry(monthstr='JAN-21'):
    """Obtain HK monthly expiry day in a month."""
    monthstart = datetime.strptime(monthstr, '%b-%y')
    monthstr = monthstart.strftime('%Y-%m')
    year = monthstart.year
    try:
        tdaylist = gettradedays(holidaylist_hk, datetime(year, 1, 1), datetime(year, 12, 31))
        tdaylist = [dtstr for dtstr in tdaylist if dtstr[:7] == monthstr]
        return tdaylist[-2]
    except:
        print(f'Holiday list for year {year} NOT available.')
        return None

hkexpiryfile = os.path.join(codepath_td, 'monthexpiry_hk.csv')



