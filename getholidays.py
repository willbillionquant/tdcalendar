import os
codepath_td = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append('..')

from datetime import datetime
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

if __name__ == '__main__':
    getnyholidays()
    gethkholidays()