import datetime as dt
import matplotlib.pyplot as plt
from numpy.lib.twodim_base import tri
import pandas_datareader as web

# Adj Close is for adjusted Closing Price for stock split

plt.style.use("dark_background")

# Change moving averages as per your need
ma_1 = 30       # 30 day moving average
ma_2 = 100      # 100 day moving average

start = dt.datetime.now() - dt.timedelta(days=365*3)    # Last 3 years
end = dt.datetime.now()

ticker_symbol = input('Enter the Stock Ticker(listed on market for atleast past 3 years): ')

data = web.DataReader(ticker_symbol, 'yahoo', start, end)
#print(data)

#Aggregate the values over a timeframe and apply mean function
data[F'SMA_{ma_1}'] = data['Adj Close'].rolling(window = ma_1).mean()   
data[F'SMA_{ma_2}'] = data['Adj Close'].rolling(window = ma_2).mean()

#data = data.iloc[ma_2:]         # Start looking after 100 days
""" .iloc[] is primarily integer position based (from 0 to length-1 of the axis), but may also be used with a boolean array. """

buy_signals = []        # Buy at this point
sell_signals = []       # Sell at this point
trigger = 0             # Change state after buying/selling

# Algorithmic Trading
for x in range(len(data)):
    if data[f'SMA_{ma_1}'].iloc[x] > data[f'SMA_{ma_2}'].iloc[x] and trigger != 1:      
        # If moving average 1 of that position is larger than moving average 2 at same position and trigger isn't equal to 1, then signal to buy.
        buy_signals.append(data['Adj Close'].iloc[x])           # append the adjusted closing price of that position
        sell_signals.append(float('nan'))
        trigger = 1                                             # Change trigger

    elif data[f'SMA_{ma_1}'].iloc[x] < data[f'SMA_{ma_2}'].iloc[x] and trigger != -1:
        # If moving average 1 of that position is smaller than moving average 2 at same position and trigger isn't equal to -1, then signal to sell.
        buy_signals.append(float('nan'))
        sell_signals.append(data['Adj Close'].iloc[x])
        trigger = -1

    else:
        buy_signals.append(float('nan'))
        sell_signals.append(float('nan'))

data['Buy Signals'] = buy_signals
data['Sell Signals'] = sell_signals
print(data)

plt.plot(data['Adj Close'], label='Share Price', alpha = 0.5)
plt.plot(data[f'SMA_{ma_1}'], label=f'SMA_{ma_1}', color = 'orange', linestyle = "--")        # Average of last 30 days
plt.plot(data[f'SMA_{ma_2}'], label=f'SMA_{ma_2}', color = 'pink', linestyle = "--")          # Average of last 100 days
plt.scatter(data.index, data['Buy Signals'], label="Buy Signal", marker="^", color="#00ff00", lw=3)
plt.scatter(data.index, data['Sell Signals'], label="Sell Signal", marker="v", color="#ff0000", lw=3)
plt.legend(loc="upper left")
plt.title('{} Share Price'.format(ticker_symbol))
plt.show()
