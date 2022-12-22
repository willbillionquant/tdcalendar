import os
codepath_td = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append('..')

from datetime import datetime, timedelta
import pandas as pd

def getnyholidays(startyear=1990, endyear=2046):
    """Obtain US stock market full-day holidays."""
    dfhday_ny = pd.DataFrame()

    for year in range(startyear, endyear + 1):
        try:
            tablelist = pd.read_html(f'http://www.market-holidays.com/{year}')
            dfraw = tablelist[0].copy()
            dfhday = pd.DataFrame(columns=['date', 'wday', 'name'])
            dfhday['date'] = dfraw[1].apply(lambda x: datetime.strptime(x, '%B %d, %Y'))
            dfhday['wday'] = dfhday['date'].apply(lambda x: x.weekday() + 1)
            dfhday['name'] = dfraw[0]
            dfhday_ny = pd.concat([dfhday_ny, dfhday], axis=0)
            print(f'{year} US holiday done.')
        except:
            print(f'{year} US holiday not available.')
            break

    dfhday_ny.set_index('date', inplace=True)
    dfhday_ny['name'] = dfhday_ny['name'].replace('Martin Luther King, Jr. Day', 'MLK Day')\
                                         .replace('Juneteenth National Independence Day', '619 Day')
    dfhday_ny = dfhday_ny[dfhday_ny['name'] != 'Martin Luther King, Jr. Day(1-minute pause at noon)']
    dfhday_ny.to_csv(os.path.join(codepath_td, 'holiday_ny.csv'))


def gethkholidays(startyear=2007, endyear=2046):
    """Obtain US stock market full-day holidays."""
    dfhday_hk = pd.DataFrame()

    for year in range(startyear, endyear + 1):
        try:
            tablelist = pd.read_html(f'https://www.gov.hk/en/about/abouthk/holiday/{year}.htm')
            dfraw = tablelist[0].loc[1:]
            dfhday = pd.DataFrame(columns=['date', 'wday', 'name'])
            dfhday['date'] = dfraw[1].apply(lambda x: datetime.strptime(x + f',{year}', '%d %B,%Y'))
            dfhday['wday'] = dfhday['date'].apply(lambda x: x.weekday() + 1)
            dfhday['name'] = dfraw[0]
            dfhday_hk = pd.concat([dfhday_hk, dfhday], axis=0)
            print(f'{year} HK holiday done.')
        except:
            print(f'{year} HK holiday not available.')
            break

    dfhday_hk.set_index('date', inplace=True)
    dfhday_hk.to_csv('holiday_hk.csv')

# US stock market holidays
holidayfile_ny = os.path.join(codepath_td, 'holiday_ny.csv')

if not os.path.exists(holidayfile_ny):
    getnyholidays()
elif (datetime.today().month == 1) and (datetime.today().day == 1):
    os.remove(holidayfile_ny)
    getnyholidays()

with open(holidayfile_ny, 'r') as f:
    holidaylines_ny = f.readlines()
    holidaylist_ny = [datetime.strptime(row.split(',')[0], '%Y-%m-%d') for row in holidaylines_ny[1:]]

# HK stock market holidays
holidayfile_hk = os.path.join(codepath_td, 'holiday_hk.csv')

if not os.path.exists(holidayfile_hk):
    gethkholidays()
elif (datetime.today().month == 1) and (datetime.today().day == 1):
    os.remove(holidayfile_hk)
    gethkholidays()

with open(holidayfile_hk, 'r') as f:
    holidaylines_hk = f.readlines()
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

def getlatesttradingday(holidaylist, tday=datetime.today(), days=1, offset=6, form='%Y-%m-%d'):
    """Obtain the latest trading date."""
    today = tday - timedelta(days=days, hours=offset)
    earlyday = today - timedelta(days=30)
    tdlist = [dtstr for dtstr in gettradedays(holidaylist, earlyday, today, form)]

    return tdlist[-1]

def getdayslater(date='2022-01-01', numday=0):
    """Obtain datestring format in the form '%Y-%m-%d %H:%M:%S:%f'."""
    afterdate = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=numday) - timedelta(seconds=1)
    afterstr = afterdate.strftime('%Y-%m-%d %H:%M:%S:%f')
    return afterstr

def getnthweekday(date):
    """Obtain the nth weekday of a calendar day."""
    return (date.day-1) // 7 + 1, date.weekday() + 1