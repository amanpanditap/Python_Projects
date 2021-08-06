# API: https://financialmodelingprep.com/developer/docs#Company-Financial-Statements
# For Demo: AAPL is used, for other tickers a premium subscription is required.
import requests
import matplotlib.pyplot as plt

api_key = open('api_key', 'r').read()

company = input('Enter the Company Ticker on which you wish to perform balance sheet analysis: ')
years = 5

balance_sheet = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?limit={years}&apikey={api_key}')
# print(balance_sheet.json())

balance_sheet = balance_sheet.json()
# print(balance_sheet[0].keys())

total_current_assets = balance_sheet[0]['totalCurrentAssets'] 
print(f'Total Current Assets of {company}: {total_current_assets:,}')
print('\n')

total_current_liabilities = balance_sheet[0]['totalCurrentLiabilities'] 
print(f'Total Current Liabilities of {company}: {total_current_liabilities:,}')
print('\n')

total_debt = balance_sheet[0]['totalDebt']
cash_and_equivalents = balance_sheet[0]['cashAndCashEquivalents']
cash_debt_difference = cash_and_equivalents - total_debt
print(f'Cash Debt Difference: {cash_debt_difference:,}')
print('\n')

goodwill_and_intangibles = balance_sheet[0]['goodwillAndIntangibleAssets']
total_assets = balance_sheet[0]['totalAssets']
pct_intangible = goodwill_and_intangibles / total_assets

print(f'Percentage of goodwill_and_intangible assets: {pct_intangible * 100:.2f}')
print('\n')

# Quarterly
balance_sheet = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?period=quarter&limit={years}&apikey={api_key}')
balance_sheet = balance_sheet.json()

assets_q1 = balance_sheet[4]['totalAssets']
assets_q2 = balance_sheet[3]['totalAssets']
assets_q3 = balance_sheet[2]['totalAssets']
assets_q4 = balance_sheet[1]['totalAssets']

assets_data = [assets_q1, assets_q2, assets_q3, assets_q4]
assets_data = [x / 1000000000 for x in assets_data]

plt.bar([1,2,3,4], assets_data)
plt.title(f"Quarterly Assets of {company}")
plt.xlabel("Quarters")
plt.ylabel("Total Assets (in Billion USD)")
plt.xticks([1,2,3,4], ['Q1', 'Q2', 'Q3', 'Q4'])
plt.show()
