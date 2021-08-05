import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime as dt
import mplfinance as mpf

currency = input('Enter the currency unit(Eg: INR, USD): ')
start = dt.datetime(2021,1,1)
end = dt.datetime.now()

a = True
while(a):
    crypto = input('Enter the Crypto ticker which you wish to visualize: ')
    b = input('Press 0 to visualize or any other key to keep adding the coins: ')
    print("\n")
    data = web.DataReader(f'{crypto}-{currency}','yahoo', start, end)
    plt.yscale("log")         # Logarathmic Scale
    plt.plot(data['Close'], label = crypto)
    plt.legend(loc="upper left")
    if b == '0':
        a = False
    
plt.show()