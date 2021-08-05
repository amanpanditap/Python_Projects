import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime as dt

start = dt.datetime(2021,1,1) 
end = dt.datetime.now()

ticker_symbol = input('Enter the stock ticker which you wish to analyse: ')
data = web.DataReader(ticker_symbol, 'yahoo', start, end)

#print(data)

delta = data['Adj Close'].diff(1)      #Calculate difference to the day before that
delta.dropna(inplace = True)  # Keep the DataFrame with valid entries in the same variable.

positive = delta.copy()
negative = delta.copy()

positive[positive < 0] = 0
negative[negative > 0] = 0

days = 14      # Standard, but can be lowered to increase sensitivity or raised to decrease sensitivity.

average_gain = positive.rolling(window = days).mean()
average_loss = abs(negative.rolling(window = days).mean())

relative_strength = average_gain/average_loss
RSI = 100.0 - (100.0 / (1.0 + relative_strength))     # Formula

combined = pd.DataFrame()
combined['Adj Close'] = data['Adj Close']
combined['RSI'] = RSI

plt.figure(figsize=(12,8))
ax1 = plt.subplot(211)   # subplot(nrows, ncols, plot_number) hence nrows=2, ncols=1, plot_number=1
ax1.plot(combined.index, combined['Adj Close'], color = 'lightgray')
ax1.set_title("{} Adjusted Close Price".format(ticker_symbol), color = 'white')
ax1.grid(True, color = "#555555")
ax1.set_axisbelow(True)
ax1.set_facecolor('black')
ax1.figure.set_facecolor('#121212')
ax1.tick_params(axis = 'x', colors = 'white')
ax1.tick_params(axis = 'y', colors = 'white')

# RSI Values of 70 or above indicate an overbought or overvalued condition.
# RSI Values of 30 or below indicates an oversold or undervalued condition.
ax2 = plt.subplot(212, sharex = ax1)  # Share same x axis.
ax2.plot(combined.index, combined['RSI'], color = 'lightgray')
ax2.axhline(0, linestyle='--',alpha=0.5, color = '#ff0000')
ax2.axhline(10, linestyle='--',alpha=0.5, color = '#ffaa00')
ax2.axhline(20, linestyle='--',alpha=0.5, color = '#00ff00')
ax2.axhline(30, linestyle='--',alpha=0.5, color = '#cccccc')
ax2.axhline(70, linestyle='--',alpha=0.5, color = '#cccccc')
ax2.axhline(80, linestyle='--',alpha=0.5, color = '#00ff00')
ax2.axhline(90, linestyle='--',alpha=0.5, color = '#ffaa00')
ax2.axhline(100, linestyle='--',alpha=0.5, color = '#ff0000')

ax2.set_title('{} RSI Value'.format(ticker_symbol), color = 'white')
ax2.grid(False)
ax2.set_axisbelow(True)
ax2.set_facecolor('black')
ax2.tick_params(axis = 'x', colors = 'white')
ax2.tick_params(axis = 'y', colors = 'white')

plt.show()