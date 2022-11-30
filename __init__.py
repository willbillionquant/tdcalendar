import os
codepath_td = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append('..')

from datetime import datetime, timedelta

# US stock market holidays
holidayfile_ny = open(os.path.join(codepath_td, 'holiday_ny.csv'), 'r')
holidaylines_ny = holidayfile_ny.readlines()
holidaylist_ny = [datetime.strptime(row.split(',')[0], '%Y-%m-%d') for row in holidaylines_ny[1:]]

# HK stock market holidays
holidayfile_hk = open(os.path.join(codepath_td, 'holiday_hk.csv'), 'r')
holidaylines_hk = holidayfile_hk.readlines()
holidaylist_hk = [datetime.strptime(row.split(',')[0], '%Y-%m-%d') for row in holidaylines_hk[1:]]

# List of all weekdays
def getwkdays(startyr=1997, endyr=2046, form='%Y-%m-%d'):
    """Get all working days (non-weekend) to string in a list."""
    dtlist = []
    date = datetime.strptime(f'{startyr}-01-01', '%Y-%m-%d')
    while (date.year >= startyr) and (date.year <= endyr):
        if date.weekday() <= 4:
            dtlist.append(date.strftime(form))
        date += timedelta(days=1)

    return dtlist

workdtlist0 = getwkdays()  #  Format yyyy-mm-dd
workdtlist1 = getwkdays(form='%Y%m%d')  # Format yyyymmdd
workdtlist2 = getwkdays(form='%y%m%d')  # Format yymmdd

def gettradedays(holidaylist, startdt=datetime(2010, 1, 1), enddt=datetime(2046, 12, 31), form='%Y-%m-%d'):
    """Get all trading day spanning a period, excluding holidays."""
    if form == '%Y-%m-%d':
        workdtlist = workdtlist0
    elif form == '%Y%m%d':
        workdtlist = workdtlist1
    elif form == '%y%m%d':
        workdtlist = workdtlist2
    else:
        workdtlist = getwkdays(form=form)

    startstr = startdt.strftime(form)
    endstr = enddt.strftime(form)
    holidaystrlist = [date.strftime(form) for date in holidaylist]
    tdlist = [dtstr for dtstr in workdtlist if (dtstr >= startstr) and (dtstr <= endstr)]
    tdlist = [dtstr for dtstr in tdlist if dtstr not in holidaystrlist]

    return tdlist

def getlatesttradingday(holidaylist, offset=6, form='%Y-%m-%d'):
    """Obtain the latest trading date."""
    today = datetime.today() - timedelta(days=1, hours=offset)
    earlyday = today - timedelta(days=30)
    tdlist = [dtstr for dtstr in gettradedays(holidaylist, earlyday, today, form)]

    return tdlist[-1]

def getdayslater(date='2022-01-01', numday=0):
    """Obtain datestring format in the form '%Y-%m-%d %H:%M:%S:%f'."""
    afterdate = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=numday) - timedelta(seconds=1)
    afterstr = afterdate.strftime('%Y-%m-%d %H:%M:%S:%f')
    return afterstr