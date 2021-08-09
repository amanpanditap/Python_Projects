import pandas_datareader as web
import pandas as pd
import yahoo_fin.stock_info as si
import datetime as dt

tickers = si.tickers_nifty50()   # Gives Top 30 Components of NIFTY 50 from https://finance.yahoo.com/quote/%5ENSEI/components?p=%5ENSEI

start = dt.datetime.now() - dt.timedelta(days=365)      # From now to 365 days before
end = dt.datetime.now()

# For Nifty 50 index
nifty50_df = web.DataReader('^NSEI', 'yahoo', start, end)
nifty50_df['Pct Change'] = nifty50_df['Adj Close'].pct_change()             # Get daily percentage change
nifty50_return = (nifty50_df['Pct Change'] + 1).cumprod()[-1]               # Get actual return over the timeframe, cumprod() = cumulative product

return_list = []
final_df = pd.DataFrame(columns= ['Ticker', 'Latest_Price', 'Score', 'PE_Ratio', 'PEG_Ratio', 'SMA_150', 'SMA_200', '52_Week_Low', '52_Week_High'])        
# Choose the parameters in columns as per your interest to screen stocks.

# For each stock in Nifty 50 index
for ticker in tickers:
    if ticker == 'MM.NS':
        ticker = 'M&M.NS'
        df = web.DataReader(ticker, 'yahoo', start, end)
        df.to_csv(f'stock_data/{ticker}.csv')               # Save into CSV File
    else:
        df = web.DataReader(ticker, 'yahoo', start, end)
        df.to_csv(f'stock_data/{ticker}.csv')               # Save into CSV File

    df['Pct Change'] = df['Adj Close'].pct_change()
    stock_return = (df['Pct Change'] + 1).cumprod()[-1]

    returns_compared = round((stock_return/nifty50_return), 2)      # Compare Nifty 50 and individual stock returns, rounding to 2 decimal places
    return_list.append(returns_compared)

# Best Performers
best_performers = pd.DataFrame(list(zip(tickers, return_list)), columns=['Ticker', 'Returns Compared'])
best_performers['Score'] = best_performers['Returns Compared'].rank(pct=True) * 100              # Ranks the best
best_performers = best_performers[best_performers['Score'] >= best_performers['Score'].quantile(0.7)]      # Top 30% percent.

for ticker in best_performers['Ticker']:
    try:
        df = pd.read_csv(f'stock_data/{ticker}.csv', index_col=0)       # Load dataframe from csv file
        moving_averages = [150, 200]        #these numbers can be added more, 100 days, 150 days ....
        for ma in moving_averages:
            df['SMA_' + str(ma)] = round(df['Adj Close'].rolling(window=ma).mean(), 2)      #Aggregate the values over a timeframe and apply mean function and round to 2 decimal places.

        latest_price = df['Adj Close'][-1]
        pe_ratio = float(si.get_quote_table(ticker)['PE Ratio (TTM)'])  # Trailing 12 Months (TTM)
        # To add your own criteria use print(si.get_quote_table(ticker)) which will lead to a dictionary for all the available parameters.

        peg_ratio = float(si.get_stats_valuation(ticker)[1][4]) 
        # To add your own criteria use print(si.get_stats_valuation(ticker)) which will lead to all the available parameters.

        moving_average_150 = df['SMA_150'][-1]
        moving_average_200 = df['SMA_200'][-1]
        low_52week = round(min(df['Low'][-(52*5):]), 2)         # 5 days in a week for 52 weeks, so get the lowest out of all.
        high_52week = round(max(df['High'][-(52*5):]), 2)
        score = round(best_performers[best_performers['Ticker'] == ticker]['Score'].tolist()[0])        
        # get instance where the ticker symbol is ticker get the score value and then turn it to a list and pick the first value

        condition_1 = latest_price > moving_average_150 > moving_average_200
        condition_2 = latest_price >= (1.1 * low_52week)        # Latest Price has to be atleast 30% more than 52 week low
        condition_3 = latest_price >= (0.6 * high_52week)      # Latest Price has to be atleast 75% of 52 week high
        condition_4 = pe_ratio < 50
        condition_5 = peg_ratio < 5

        if condition_1 and condition_2 and condition_3 and condition_4 and condition_5:         # All Conditions
            final_df = final_df.append({'Ticker': ticker,
                                        'Latest_Price': latest_price,
                                        'Score': score,
                                        'PE_Ratio': pe_ratio,
                                        'PEG_Ratio': peg_ratio,
                                        'SMA_150': moving_average_150,
                                        'SMA_200': moving_average_200,
                                        '52_Week_Low': low_52week,
                                        '52_Week_High': high_52week}, ignore_index=True)

        """ if condition_4 and condition_5:                                         # Some Condtions, modify as per your needs
            final_df = final_df.append({'Ticker': ticker,
                                        'Latest_Price': latest_price,
                                        'Score': score,
                                        'PE_Ratio': pe_ratio,
                                        'PEG_Ratio': peg_ratio,
                                        'SMA_150': moving_average_150,
                                        'SMA_200': moving_average_200,
                                        '52_Week_Low': low_52week,
                                        '52_Week_High': high_52week}, ignore_index=True) """
    except Exception as e:
        print(f"{e} for {ticker}")

final_df.sort_values(by = 'Score', ascending=False)
pd.set_option('display.max_columns', 10)            # Display all columns and not ....

print('Selected Stocks as per the parameters: \n')
print(final_df)

final_df.to_csv('final.csv')