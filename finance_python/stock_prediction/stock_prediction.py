import numpy as np
import pandas as pd
import pandas_datareader as web
import datetime as dt
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

# Load Data
start = dt.datetime(2016,1,1) 
end = dt.datetime(2021,1,1)
currency = input('Enter the currency unit(Eg: INR, USD): ')
crypto = input('Enter the Crypto Ticker which you wish to Predict: ')

# ticker_symbol = input('Enter the Stock Ticker which you wish to Predict: ')

# data = web.DataReader(ticker_symbol, 'yahoo', start, end)               # Stock Prediction
data = web.DataReader(f'{crypto}-{currency}', 'yahoo', start, end)        # Crypto Prediction

# Prepare Data
scaler = MinMaxScaler(feature_range=(0,1))  # Fit the data value within 0-1 range
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))           # Selected Closing Price for prediction

prediction_days = 60             # Select the date range for past values on which basis you wish to predict future price.
# future_day = 30                # Predict future values after 30 days

x_train = []
y_train = []

for x in range(prediction_days, len(scaled_data)):      # From 60th Index to the last index of scaled data
    x_train.append(scaled_data[x-prediction_days:x, 0]) # Append 60 values From 61st data to predict 
    y_train.append(scaled_data[x, 0])   # 61st

""" Future Prediction
for x in range(prediction_days, len(scaled_data)-future_day):      # From 60th Index to the last index of scaled data
    x_train.append(scaled_data[x-prediction_days:x, 0]) # Append 60 values From 61st data to predict 
    y_train.append(scaled_data[x+future_day, 0])   # 90th """

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# Build the Model
model = Sequential()

model.add(LSTM(units = 50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units = 50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units = 50))
model.add(Dropout(0.2))
model.add(Dense(units = 1))          # Prediction of the next closing price

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=25, batch_size=32)     # Model views same data 24 times & 32 units at once all the time

# Test the Model accuracy on existing data
test_start = dt.datetime(2021, 1, 1)
test_end = dt.datetime.now()
# test_data = web.DataReader(ticker_symbol, 'yahoo', test_start, test_end)
test_data = web.DataReader(f'{crypto}-{currency}', 'yahoo', test_start, test_end)
actual_prices = test_data['Close'].values

total_dataset = pd.concat((data['Close'], test_data['Close']), axis = 0)

model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.transform(model_inputs)  # Scaling

# Make Predictions on Test Data
x_test = []
for x in range(prediction_days, len(model_inputs)):
    x_test.append(model_inputs[x-prediction_days:x, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predicted_prices = model.predict(x_test)     # Predict
predicted_prices = scaler.inverse_transform(predicted_prices)     # Reverse Scaling as predicted_prices are scaled

# Plot the Test Prediction(Stock)
# plt.plot(actual_prices, color = 'black', label = f"Actual {ticker_symbol} Price")
# plt.plot(predicted_prices, color = 'green', label = f"Predicted {ticker_symbol} Price")
# plt.title(f"{ticker_symbol} Share Price")
# plt.xlabel('Time')
# plt.ylabel(f"{ticker_symbol} Share Price")
# plt.legend()
# plt.show()

# Plot the Test Prediction(Crypto)
plt.plot(actual_prices, color = 'black', label = f"Actual {crypto} Price")
plt.plot(predicted_prices, color = 'green', label = f"Predicted {crypto} Price")
plt.title(f"{crypto} Price")
plt.xlabel('Time')
plt.ylabel(f"{crypto} Price")
plt.legend()
plt.show()

# Predict Next Day
real_data = [model_inputs[len(model_inputs) + 1 - prediction_days: len(model_inputs+1), 0]]
real_data = np.array(real_data)
real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
print(scaler.inverse_transform(real_data[-1]))    # Print Real Data

prediction = model.predict(real_data)
prediction = scaler.inverse_transform(prediction)
print(f"Prediciton: {prediction}")       # Final Predicted Value of next day's closing price