# https://ratesapi.io is a free API for current and historical foreign exchange rates published by European Central Bank.
# The rates are updated daily 3PM CET.

# Bitcoin prices calculated every minute. For more information visit [CoinDesk API](http://www.coindesk.com/api/)

# Installation: pip install forex-python

from forex_python.converter import CurrencyRates, CurrencyCodes
from forex_python.bitcoin import BtcConverter
import datetime

c = CurrencyRates()
date_obj = datetime.datetime(2021, 1, 1, 18, 36, 28, 151012)        #(‘year’, ‘month’, ‘date’, ‘hour’, ‘minute’, ‘seconds’, ‘microseconds’)

#Get the data
amount = float(input('Enter the Amount you want to Convert: '))
from_currency = input('From : ').upper()
to_currency = input('To : ').upper()

print('\n' + from_currency + " To " + to_currency, amount)
print('The current conversion rate for {} to {} is {}'.format(from_currency, to_currency, c.get_rate(from_currency, to_currency)))    #Get conversion rate from USD to INR
result = c.convert(from_currency, to_currency, amount)   #Convert the amount
print('Latest Conversion: ',result)

#Get conversion rate as of 2021-01-01
print('\nThe conversion rate from {} to {} as per 1st Jan 2021 is {}'.format(from_currency, to_currency, c.get_rate(from_currency, to_currency, date_obj)))
print('The conversion as per 1st Jan 2021: ', c.convert(from_currency, to_currency, amount, date_obj))

b = BtcConverter()
print('\n\nBitcoin Symbol: ', b.get_symbol())  # get_btc_symbol()
print('Bitcoin Latest Price in USD : ', b.get_latest_price('USD'))     #Get latest Bitcoin price.
print('Convert 10 Million USD to Bitcoin', b.convert_to_btc(10000000, 'USD'))     #Convert Amount to Bitcoins based on latest exchange price.
print('The Equivalent of 10.99 Bitcoin in USD: ',b.convert_btc_to_cur(10.99, 'USD'))         #Convert Bitcoins to valid currency amount based on lates price

print('\nBitcoin price as per 1st Jan 2021: ',b.get_previous_price('USD', date_obj)) #Get price of Bitcoin based on prevois date
print('The conversion of 10 Million Dollars to Bitcoin as of 1st Jan 2021',b.convert_to_btc_on(10000000, 'USD', date_obj))      #Convert Amount to bitcoins based on previous date prices
print('The conversion of 10.99 Bitcoin in USD as of 1st Jan 2021: ',b.convert_btc_to_cur_on(10.99, 'USD', date_obj))       #Convert Bitcoins to valid currency amount based on previous date price

start_date = datetime.datetime(2021, 2, 1, 19, 39, 36, 815417)
end_date = datetime.datetime(2021, 2, 7, 19, 39, 36, 815417)
print('\nBitcoin rates over the week in USD: ',b.get_previous_price_list('USD', start_date, end_date))         #Get list of prices list for given date range

d = CurrencyCodes()
print('\nUS Dollar Symbol:', d.get_symbol('USD'))          #Get currency symbol using currency code
print(d.get_currency_name('USD'))          #Get Currency Name using currency code

print('\nThe latest rate of USD for various currencies\n', c.get_rates('USD'))          #list all latest currency rates for "USD"
print('\nThe rate of USD for various currencies as per 1st Jan 2021\n',c.get_rates('USD', date_obj))             #List all Currency rates for “USD” on 2021-01-01
