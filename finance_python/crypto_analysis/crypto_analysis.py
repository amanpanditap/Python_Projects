import pandas_datareader as web
import matplotlib.pyplot as plt
import mplfinance as mpf
import seaborn as sns
import datetime as dt

currency = input('Enter the currency unit(Eg: INR, USD): ')
start = dt.datetime(2021,1,1)
end = dt.datetime.now()

crypto = []
stock = []

metric = 'Close'         # Choose either 'Open', 'Close', 'High', 'Low', 'Volume', 'Adj Close' that you wish to analyse.
colnames = []

a = True
while(a):
    # stock_ticker = input('Enter the Stock Ticker which you wish to Analyse: ')
    # stock.append(stock_ticker)

    crypto_ticker = input('Enter the Crypto Ticker which you wish to Analyse: ')
    crypto.append(crypto_ticker)

    b = input('Press 0 to analyse or any other key to keep adding the coins: ')
    print("\n")
    if b == '0':
        a = False

first = True     
for ticker in crypto:                # Stock Analysis: for ticker in stock
    data = web.DataReader(f'{ticker}-{currency}', 'yahoo', start, end)
    # data = web.DataReader(ticker, 'yahoo', start, end)      
    # This method can also be used to analyse stocks where ticker is stock ticker.

    if first:                      # For first ticker in the list
        combined = data[[metric]].copy()
        colnames.append(ticker)
        combined.columns = colnames
        first = False
    else:
        combined = combined.join(data[metric])
        colnames.append(ticker)
        combined.columns = colnames
    
#print(combined)

combined = combined.pct_change().corr(method = "pearson")    # Get price movements in percentage points with correlation using pearson method
sns.heatmap(combined, annot=True, cmap="RdYlGn", vmax=1.0, vmin=-1.0)

# plt.yscale('log')

# for ticker in crypto:
#     plt.plot(combined[ticker], label=ticker)

# plt.legend(loc="upper right")

plt.show()