import pandas as pd
import matplotlib.pyplot as plt

# Loading And Preparing The Data
confirmed = pd.read_csv('datasets/covid19_confirmed_global.csv')
deaths = pd.read_csv('datasets/covid19_deaths_global.csv')
recovered = pd.read_csv('datasets/covid19_recovered_global.csv')

# print(confirmed.head())

"""Output will look like this:
  Province/State Country/Region       Lat       Long  1/22/20  1/23/20  1/24/20  1/25/20  ...  8/1/21  8/2/21  8/3/21  8/4/21  8/5/21  8/6/21  8/7/21  8/8/21
0            NaN    Afghanistan  33.93911  67.709953        0        0        0        0  ...  146523  147985  148572  148933  149361  149810  149810  149810
1            NaN        Albania  41.15330  20.168300        0        0        0        0  ...  133121  133146  133211  133310  133442  133591  133730  133912
2            NaN        Algeria  28.03390   1.659600        0        0        0        0  ...  172564  173922  175229  176724  178013  179216  180356  181376
3            NaN        Andorra  42.50630   1.521800        0        0        0        0  ...   14678   14747   14766   14797   14809   14836   14836   14836
4            NaN         Angola -11.20270  17.873900        0        0        0        0  ...   42815   42970   43070   43158   43269   43487   43592   43662 
"""

# Drop the ‘Province/State’ column & ‘Lat’ and the ‘Long’ columns, which are the coordinates.
confirmed = confirmed.drop(['Province/State', 'Lat', 'Long'], axis=1)        
deaths = deaths.drop(['Province/State', 'Lat', 'Long'], axis=1)              
recovered = recovered.drop(['Province/State', 'Lat', 'Long'], axis=1)        

# Add up the values of all rows of the same country.
confirmed = confirmed.groupby(confirmed['Country/Region']).aggregate('sum')  
deaths = deaths.groupby(deaths['Country/Region']).aggregate('sum')
recovered = recovered.groupby(recovered['Country/Region']).aggregate('sum')

# Transpose the data frame (dates as rows and the countries as columns.)
confirmed = confirmed.T
deaths = deaths.T
recovered = recovered.T

# print(confirmed.head())

# Calculating Key Statistics
""" .iloc[] is primarily integer position based (from 0 to length-1 of the axis), but may also be used with a boolean array. """

print(len(confirmed))

new_cases = confirmed.copy()        

for day in range(1, len(confirmed)):          # Get data of last 100 days, for 
    new_cases.iloc[day] = confirmed.iloc[day] - confirmed.iloc[day - 1]

growth_rate = confirmed.copy()

for day in range(1, len(confirmed)):
    growth_rate.iloc[day] = (new_cases.iloc[day] / confirmed.iloc[day - 1]) * 100

active_cases = confirmed.copy()

for day in range(1, len(confirmed)):
    active_cases.iloc[day] = confirmed.iloc[day] - deaths.iloc[day] - recovered.iloc[day]

overall_growth_rate = confirmed.copy()

for day in range(1, len(confirmed)):
    overall_growth_rate.iloc[day] = ((active_cases.iloc[day] - active_cases.iloc[day-1]) / active_cases.iloc[day - 1]) * 100

death_rate = confirmed.copy()

for day in range(1, len(confirmed)):
    death_rate.iloc[day] = (deaths.iloc[day] / confirmed.iloc[day]) * 100

# Making Estimations
hospitalization_rate_estimate = 0.05        # Experts say that 5% of coronavirus patients will need a hospital bed, because their infection will be severe.

hospitalization_needed = confirmed.copy()

for day in range(0, len(confirmed)):
    hospitalization_needed.iloc[day] = active_cases.iloc[day] * hospitalization_rate_estimate

estimated_death_rate = 0.013   # assumed a mortality rate of 1.3% for India
print(deaths['India'].tail()[4] / estimated_death_rate)         # Estimated number of people that are actually infected.

# Visualizing The Data

countries = ['US', 'India', 'Brazil', 'Russia', 'France', 'United Kingdom']

ax = plt.subplot()
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.set_title('COVID-19 - Total Confirmed Cases', color='white')
ax.legend(loc="upper left")

for country in countries:
    confirmed[country][0:].plot(label = country)

plt.legend(loc='upper left')
plt.show()

ax = plt.subplot()
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.set_title('COVID-19 - Total Deaths Reported', color='white')
ax.legend(loc="upper left")

for country in countries:
    deaths[country][0:].plot(label = country)

plt.legend(loc='upper left')
plt.show()

ax = plt.subplot()
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.set_title('COVID-19 - Total Recovery Reported', color='white')
ax.legend(loc="upper left")

for country in countries:
    recovered[country][0:].plot(label = country)

plt.legend(loc='upper left')
plt.show()

countries = ['India']

for country in countries:
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title(f'COVID-19 - Overall Active Growth Rate [{country}]', color='white')
    overall_growth_rate[country][10:].plot.bar()
    plt.show()

for country in countries:
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title(f'COVID-19 - Death Rate [{country}]', color='white')
    death_rate[country][10:].plot.bar()
    plt.show()

for country in countries:
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title(f'COVID-19 - New Cases [{country}]', color='white')
    new_cases[country][10:].plot.bar()
    plt.show()

for country in countries:
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title(f'COVID-19 - Active Cases [{country}]', color='white')
    active_cases[country][10:].plot.bar()
    plt.show()

for country in countries:
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title(f'COVID-19 - Growth Rate [{country}]', color='white')
    growth_rate[country][10:].plot.bar()
    plt.show()

for country in countries:
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title(f'COVID-19 - Hospitalization Needed [{country}]', color='white')
    hospitalization_needed[country][10:].plot.bar()
    plt.show()

# Running Simulations
simulation_growth_rate = 0.02            # constant growth rate of 2% for next 40 days.

dates = pd.date_range(start='8/9/2021', periods=40, freq='D')
dates = pd.Series(dates)
dates = dates.dt.strftime('%m/%d/%Y')

simulated = confirmed.copy()
simulated = simulated.append(pd.DataFrame(index=dates))

for day in range(len(confirmed), len(confirmed)+40):
    simulated.iloc[day] = simulated.iloc[day - 1] * (simulation_growth_rate + 1)

ax = simulated['India'][10:].plot(label="India")
ax.set_axisbelow(True)
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.set_title('COVID-19 India (Simulation: constant 2% growth rate)', color='white')
ax.legend(loc="upper left")

plt.show()