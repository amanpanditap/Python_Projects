import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime as dt
import mplfinance as mpf

currency = input('Enter the currency unit(Eg: INR, USD): ')
start = dt.datetime(2021,1,1)
end = dt.datetime.now()

a = True
while(a):
    crypto_ticker = input('Enter the Crypto Ticker which you wish to visualize: ')
    # stock_ticker = input('Enter the Stock Ticker which you wish to visualize: ')
    b = input('Press 0 to visualize or any other key to keep adding the coins/stocks: ')
    print("\n")

    data = web.DataReader(f'{crypto_ticker}-{currency}','yahoo', start, end)
    # data = web.DataReader(stock_ticker,'yahoo', start, end)

    plt.yscale("log")         # Logarathmic Scale as the difference between crypto prices is too large.[Not required for visualizing stocks]
    plt.plot(data['Close'], label = crypto_ticker)
    # plt.plot(data['Close'], label = stock_ticker)
    
    plt.legend(loc="upper left")
    if b == '0':
        a = False
    
plt.show()