import bs4 as bs
import pickle
import requests
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
import os


if not os.path.exists('PrimaryDataFrames'):
    os.makedirs('PrimaryDataFrames')

#You can set your date frames here (yyyy, mm, d)
start = dt.datetime(2000,1,1)
end =dt.datetime(2017,3,28)

#You may set which data (stock) to extract in ('STOCK', 'yahoo', start, end) 
df = web.DataReader('SPY', 'yahoo', start, end) 
df.to_csv('PrimaryDataFrames/SPDR.csv')  #Will retrieve all data for Stock and save in folder (Open, High , Low, Close)

#Below the 30(blue), 90(purple), and 120(green) day moving averages will be computed along with weekly candles for swings in prices
style.use('ggplot')

df = pd.read_csv('PrimaryDataFrames/SPDR.csv', parse_dates = True, index_col=0)

df['30ma'] = df['Adj Close'].rolling(window=30, min_periods=0).mean() #30 day moving avg
df.dropna(inplace=True)
df['90ma'] = df['Adj Close'].rolling(window=90, min_periods=0).mean() #90 day moving acg
df.dropna(inplace=True)
df['120ma'] = df['Adj Close'].rolling(window=120, min_periods=0).mean() #120 day moving avg
df.dropna(inplace=True)
df_ohlc = df['Adj Close'].resample('5D').ohlc() #5d candles for +/- in stock prices
df_volume = df['Volume'].resample('5D').sum() #Volume on bottom of graph

df_ohlc.reset_index(inplace=True)

df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
print(df_ohlc.head())

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()
ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['30ma'])
ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['90ma'])
ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['120ma'])
ax2.bar(df.index, df['Volume'])

candlestick_ohlc(ax1, df_ohlc.values, width=3, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

plt.legend()
plt.show()
