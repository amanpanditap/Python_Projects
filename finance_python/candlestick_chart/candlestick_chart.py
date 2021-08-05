# Note: The commented code is for the mpl_finance method which is deprecated now.

import datetime as dt
import pandas_datareader as web
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
import mplfinance as mpf
#from mpl_finance import candlestick_ohlc

# Find Time Frame (Range) 

start = dt.datetime(2021,5,1) #Year, Month, Day
# This date range can be any considering the company existed on market during that time.

end = dt.datetime.now()

# Load Data
ticker_symbol = input('Enter the stock ticker which you wish to plot the chart: ')
data = web.DataReader(ticker_symbol, 'yahoo', start, end)

# print(data)

# Restructuring the Data
data = data[['Open', 'High', 'Low', 'Close']]
# data.reset_index(inplace = True)
# data['Date'] = data['Date'].map(mdates.date2num)
# print(data.head())

# Visualization

""" First, install mpl_finance

pip install https://github.com/matplotlib/mpl_finance/archive/master.zip
Second, upgrade mpl_finance

pip install --upgrade mplfinance """

# ax = plt.subplot()
# ax.grid(True)
# ax.set_axisbelow(True)
# ax.set_title('{} Share Price'.format(ticker_symbol), color='white')
# ax.set_facecolor('black')
# ax.figure.set_facecolor('#121212')
# ax.tick_params(axis = 'x', colors='white')
# ax.tick_params(axis = 'y', colors='white')
# ax.xaxis_date()

# candlestick_ohlc(ax, data.values, width = 0.5, colorup = '#00ff00')
# plt.show()

data.index.name = 'Date'
colors = mpf.make_marketcolors(up='#00ff00', down='#ff0000', wick='inherit', edge='inherit', volume="in")
mpf_style = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colors)

mpf.plot(data, type='candle',title = '{} Share Price'.format(ticker_symbol), style = mpf_style, ylabel = 'Price')
mpf.show()
