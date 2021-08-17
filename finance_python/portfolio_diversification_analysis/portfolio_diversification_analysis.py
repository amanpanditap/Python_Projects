import yfinance as yf
from yahoo_fin import stock_info as si
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

plt.style.use("dark_background")

stocks = ['AAPL', 'FB', 'MSFT', 'NVDA', 'BABA', 'NSRGY', 'SPOT', 'BCS']         # Stock Tickers
amounts = [20, 15, 20, 30, 40, 50, 40, 70]
values = [si.get_live_price(stocks[i]) * amounts[i] for i in range(len(stocks))]
sectors = [yf.Ticker(x).get_info()['industry'] for x in stocks]
countries = [yf.Ticker(x).get_info()['country'] for x in stocks]
market_caps = [yf.Ticker(x).get_info()['marketCap'] for x in stocks]

# print(yf.Ticker('AAPL').get_info())       To return the dictionary values and see all available parameters

cash = 50000            # 50K USD in hand

etfs = ['IVV', 'XWD.TO', 'QQQ']         # ETFs
etf_amounts = [30, 20, 10]
etf_values = [si.get_live_price(etfs[i]) * etf_amounts[i] for i in range(len(etfs))]

cryptos = ['ETH-USD', 'BTC-USD']                # Cryptocurrencies
crypto_amounts = [0.90, 0.50]
crypto_values = [si.get_live_price(cryptos[i]) * crypto_amounts[i] for i in range(len(cryptos))]

# General distribution by % of stocks, etfs, crypto and cash in hand
general_dist = {
    'Stocks': sum(values),
    'ETFs': sum(etf_values),
    'Cryptos': sum(crypto_values),
    'Cash': cash
}

# Categorize a stock by its sector/industry
sector_dist = {}
for i in range(len(sectors)):
    if sectors[i] not in sector_dist.keys():
        sector_dist[sectors[i]] = 0
    sector_dist[sectors[i]] += values[i]

# Categorize a stock by its country
country_dist = {}
for i in range(len(countries)):
    if countries[i] not in country_dist.keys():
        country_dist[countries[i]] = 0
    country_dist[countries[i]] += values[i]

# Categorize a stock by its market cap
""" Small - less than 2 billion
Mid - less than 10 billion
Large - less than 1 trillion
Huge - more than 1 trillion """
market_cap_dist = {'small': 0.0, 'mid': 0.0, 'large': 0.0, 'huge': 0.0}
for i in range(len(stocks)):
    if market_caps[i] < 2000000000:
        market_cap_dist['small'] += values[i]
    elif market_caps[i] < 10000000000:
        market_cap_dist['mid'] += values[i]
    elif market_caps[i] < 1000000000000:
        market_cap_dist['large'] += values[i]
    else:
        market_cap_dist['huge'] += values[i]

fig, axs = plt.subplots(2, 2)
fig.suptitle('Portfolio Diversification Analysis', fontsize= 18)

# https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.pie.html
axs[0,0].pie(general_dist.values(), labels=general_dist.keys(), autopct="%1.1f%%", pctdistance=0.8, colors=mcolors.TABLEAU_COLORS)  # Upper Left Pie Chart
axs[0,0].set_title('General Distribution')

axs[0,1].pie(sector_dist.values(), labels=sector_dist.keys(), autopct="%1.1f%%", pctdistance=0.8, colors=mcolors.TABLEAU_COLORS)  # Upper Right Pie Chart
axs[0,1].set_title('Stocks by Industry')

axs[1,0].pie(country_dist.values(), labels=country_dist.keys(), autopct="%1.1f%%", pctdistance=0.8, colors=mcolors.TABLEAU_COLORS)  # Bottom Left Pie Chart
axs[1,0].set_title('Stocks by Country')

axs[1,1].pie(market_cap_dist.values(), labels=market_cap_dist.keys(), autopct="%1.1f%%", pctdistance=0.8, colors=mcolors.TABLEAU_COLORS)  # Bottom Right Pie Chart
axs[1,1].set_title('Stocks by Market Cap')

plt.show()