# CALL Option: Right but not obligation to BUY a certain asset up to a certain date. 
# PUT Option: Right but not obligation to SELL a certain asset up to a certain date.

from yahoo_fin import options
import pandas as pd

stock = 'MSFT'          # Selected Stock Ticker

print(f'All Expiration Dates for {stock}: ')
print(options.get_expiration_dates(stock))          # Get all possible expiration dates
print('\n')

pd.set_option('display.max_columns', None)      # View all columns
chain = options.get_options_chain(stock, 'August 20, 2021')         # Give all options that expire before a particular date
#print(chain)                # All Options
#print('\n')
print('CALL Options: \n')
print(chain['calls'])       # CALL Options
print('\n')
print('PUT Options: \n')
print(chain['puts'])        # PUT Options
print('\n')

# Another way to get call and put options directly
chain = options.get_calls(stock, 'August 20, 2021')
#print(chain)

# Strike value depends on Stock's price, so modify as per requirement.
print('CALL Options: Strike <=150 \n')
print(chain[chain['Strike'] <= 150])           # Get all rows where strike price is less than 150
print('\n')

chain = options.get_puts(stock, 'August 20, 2021')
#print(chain)
print('PUT Options: Strike <=150 \n')
print(chain[chain['Strike'] <= 150])           # Get all rows where strike price is less than 150
print('\n')