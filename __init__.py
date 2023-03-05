import os
codepath_td = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append('..')

from datetime import datetime, timedelta
import pandas as pd

def getHolidays_ny(startYear=1990, endYear=2046):
    """Obtain US stock market full-day holidays."""
    dfHolidays = pd.DataFrame()

    for year in range(startYear, endYear + 1):
        try:
            tableList = pd.read_html(f'http://www.market-holidays.com/{year}')
            dfRaw = tableList[0].copy()
            dfNew = pd.DataFrame(columns=['date', 'wday', 'name'])
            dfNew['date'] = dfRaw[1].apply(lambda x: datetime.strptime(x, '%B %d, %Y'))
            dfNew['wday'] = dfNew['date'].apply(lambda x: x.weekday() + 1)
            dfNew['name'] = dfRaw[0]
            dfHolidays = pd.concat([dfHolidays, dfNew], axis=0)
            print(f'{year} US holiday done.')
        except:
            print(f'{year} US holiday not available.')
            break

    dfHolidays.set_index('date', inplace=True)
    dfHolidays['name'] = dfHolidays['name'].replace('Martin Luther King, Jr. Day', 'MLK Day')\
                                         .replace('Juneteenth National Independence Day', '619 Day')
    dfHolidays = dfHolidays[dfHolidays['name'] != 'Martin Luther King, Jr. Day(1-minute pause at noon)']
    dfHolidays.to_csv(os.path.join(codepath_td, 'holiday_ny.csv'))


def getHolidays_hk(startYear=2007, endYear=2046):
    """Obtain US stock market full-day holidays."""
    dfHolidays = pd.DataFrame()

    for year in range(startYear, endYear + 1):
        try:
            tableList = pd.read_html(f'https://www.gov.hk/en/about/abouthk/holiday/{year}.htm')
            dfRaw = tableList[0].loc[1:]
            dfNew = pd.DataFrame(columns=['date', 'wday', 'name'])
            dfNew['date'] = dfRaw[1].apply(lambda x: datetime.strptime(x + f',{year}', '%d %B,%Y'))
            dfNew['wday'] = dfNew['date'].apply(lambda x: x.weekday() + 1)
            dfNew['name'] = dfRaw[0]
            dfHolidays = pd.concat([dfHolidays, dfNew], axis=0)
            print(f'{year} HK holiday done.')
        except:
            print(f'{year} HK holiday not available.')
            break

    dfHolidays.set_index('date', inplace=True)
    dfHolidays.to_csv(os.path.join(codepath_td, 'holiday_hk.csv'))

# US stock market holidays
holidayFile_ny = os.path.join(codepath_td, 'holiday_ny.csv')

if not os.path.exists(holidayFile_ny):
    getHolidays_ny()
elif (datetime.today().month == 1) and (datetime.today().day == 1):
    os.remove(holidayFile_ny)
    getHolidays_ny()

with open(holidayFile_ny, 'r') as f:
    holidayLines_ny = f.readlines()
    holidayList_ny = [datetime.strptime(row.split(',')[0], '%Y-%m-%d') for row in holidayLines_ny[1:]]

# HK stock market holidays
holidayFile_hk = os.path.join(codepath_td, 'holiday_hk.csv')

if not os.path.exists(holidayFile_hk):
    getHolidays_hk()
elif (datetime.today().month == 1) and (datetime.today().day == 1):
    os.remove(holidayFile_hk)
    getHolidays_hk()

with open(holidayFile_hk, 'r') as f:
    holidayLines_hk = f.readlines()
    holidayList_hk = [datetime.strptime(row.split(',')[0], '%Y-%m-%d') for row in holidayLines_hk[1:]]

# List of all weekdays
def getWeekdays(startyr=1997, endyr=2046, form='%Y-%m-%d'):
    """Get all working days (non-weekend) to string in a list."""
    dtlist = []
    date = datetime.strptime(f'{startyr}-01-01', '%Y-%m-%d')
    while (date.year >= startyr) and (date.year <= endyr):
        if date.weekday() <= 4:
            dtlist.append(date.strftime(form))
        date += timedelta(days=1)

    return dtlist

weekdayList0 = getWeekdays()  #  Format yyyy-mm-dd
weekdayList1 = getWeekdays(form='%Y%m%d')  # Format yyyymmdd
weekdayList2 = getWeekdays(form='%y%m%d')  # Format yymmdd

def getTradingDays(holidayList, startDate=datetime(2010, 1, 1), endDate=datetime(2046, 12, 31), form='%Y-%m-%d'):
    """Get all trading day spanning a period, excluding holidays."""
    if form == '%Y-%m-%d':
        weekdayList = weekdayList0
    elif form == '%Y%m%d':
        weekdayList = weekdayList1
    elif form == '%y%m%d':
        weekdayList = weekdayList2
    else:
        weekdayList = getWeekdays(form=form)

    startStr = startDate.strftime(form)
    endStr = endDate.strftime(form)
    holidayStrList = [date.strftime(form) for date in holidayList]
    tDayList = [dayStr for dayStr in weekdayList if (dayStr >= startStr) and (dayStr <= endStr)]
    tDayList = [dayStr for dayStr in tDayList if dayStr not in holidayStrList]

    return tDayList

def getLatestTradingDay(holidayList, nowDay=datetime.today(), days=1, offset=6, form='%Y-%m-%d'):
    """Obtain the latest trading date."""
    nowDay -= timedelta(days=days, hours=offset)
    earlierDay = nowDay - timedelta(days=14)
    tDayList = [dayStr for dayStr in getTradingDays(holidayList, earlierDay, nowDay, form)]

    return tDayList[-1]

def getDaysLater(date='2022-01-01', numday=0):
    """Obtain datestring format in the form '%Y-%m-%d %H:%M:%S:%f'."""
    afterDate = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=numday) - timedelta(seconds=1)
    return afterDate.strftime('%Y-%m-%d %H:%M:%S:%f')

def getNthWeekday(date):
    """Obtain the nth weekday of a calendar day."""
    return (date.day-1) // 7 + 1, date.weekday() + 1