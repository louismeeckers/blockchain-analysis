from os.path import isfile
import pandas as pd
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta

# list of tested tickers
# btc-usd and ltc-usd have longest history
tested_tickers = ['btc-usd', 'ltc-usd', 'eth-usd', 'bch-usd', 'eth-btc', 'ltc-btc', 'bch-btc', 'doge-btc', 'shib-btc', 'uni3-btc']

def fetch_data(ticker, start_date, end_date) -> pd.DataFrame:
        data_df = yf.download(ticker, start=start_date, end=end_date, proxy=None)
        data_df = data_df.reset_index()

        # standerdise names
        data_df.columns = ["date", "open", "high", "low", "close", "adjcp", "volume"]
        
        data_df["close"] = data_df["adjcp"]
        data_df = data_df.drop(labels="adjcp", axis=1)
        data_df["day"] = data_df["date"].dt.dayofweek
        data_df["date"] = data_df.date.apply(lambda x: x.strftime("%Y-%m-%d"))
        data_df = data_df.dropna()
        data_df = data_df.reset_index(drop=True)
        data_df = data_df.sort_values(by=["date"]).reset_index(drop=True)

        return data_df

def get_ticker_data(ticker, start_date, end_date, force_reload=False):
    if isfile('./financial/'+ticker+'.csv') and not force_reload:
        data = pd.read_csv('financial/'+ticker+'.csv')
    else:
        if ticker not in tested_tickers: print("Warning! Untested ticker")
        data = fetch_data(start_date='2009-01-01', end_date='2021-11-01', ticker=ticker)  
        data.to_csv('financial/'+ticker+'.csv', index=False)
    
    data['date'] = pd.to_datetime(data['date'])
    print("Shape of DataFrame: ", data.shape)
    return data

def get_data_recurrently(start_date='2016-01-01', n=10, years=0, months=0, weeks=0, days=0):
    """Get price of btc-usd reccurently based on an interval size (in years, months, weeks, days)

    Parameters
    ----------
    start_date: first date we get data from
    n: number of dates we are going to take data from (number of intervals)
    years: number of years between each interval
    months: number of months between each interval
    weeks: number of weeks between each interval
    days: number of days between each interval

    Returns
    -------
    output: pandas dataframe where rows corresponds to intervals
    """

    date = datetime.strptime(start_date, '%Y-%m-%d')
    print(date.strftime('%Y-%m-%d'))
    btc_data = fetch_data(ticker='btc-usd', start_date=date.strftime('%Y-%m-%d'), end_date=date.strftime('%Y-%m-%d'))
    
    for i in range(n-1):
        date = date + relativedelta(years=years, months=months, weeks=weeks, days=days)
        print(date.strftime('%Y-%m-%d'))
        new_btc_data = fetch_data(ticker='btc-usd', start_date=date.strftime('%Y-%m-%d'), end_date=date.strftime('%Y-%m-%d'))
        btc_data = pd.concat([btc_data, new_btc_data])
    
    return btc_data.reset_index()

if __name__ == '__main__':
    print(get_ticker_data('btc-usd', True).head)
    