import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout

df = pd.read_csv('D:\College\BTech\SEM 7\Data Mining\DataSet\dataset.csv')



df = df['Open'].values
df = df.reshape(-1, 1)

# df.dropna()
print(df)
print(df.shape[0])

print("................")
dataset_train = np.array(df[:int(df.shape[0]*0.8)])

dataset_test = np.array(df[int(df.shape[0]*0.8):])

print(dataset_train.shape)

print(dataset_test.shape)

# scaling data
scaler = MinMaxScaler(feature_range=(0,1))
dataset_train = scaler.fit_transform(dataset_train)

print(dataset_train[:5])

dataset_test = scaler.transform(dataset_test)

print(dataset_test[:5])

def create_dataset(df):
    x = []
    y = []
    for i in range(50, df.shape[0]):
        x.append(df[i-50:i, 0])
        y.append(df[i, 0])
    x = np.array(x)
    y = np.array(y)
    return x,y 

x_train, y_train = create_dataset(dataset_train)

x_test, y_test = create_dataset(dataset_test)

model = Sequential()
model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=96, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=96, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=96))
model.add(Dropout(0.2))
model.add(Dense(units=1))

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# model.compile(loss='mean_squared_error', optimizer='adam')


# history = model.fit(x_train, y_train, epochs=50, batch_size=32)

# model.save('stock_prediction.h5')

# loss = history.history['loss']
# epoch_count = range(1, len(loss) + 1)
# plt.figure(figsize=(12,8))
# plt.plot(epoch_count, loss, 'r--')
# plt.legend(['Training Loss'])
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.show()


model = load_model('D:\College\BTech\SEM 7\Data Mining\Assignment9\stock_prediction.h5')

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)
y_test_scaled = scaler.inverse_transform(y_test.reshape(-1, 1))
print('predictions',predictions)
fig, ax = plt.subplots(figsize=(16,8))
plt.plot(y_test_scaled, color='red', label='Original price')
plt.plot(predictions, color='cyan', label='Predicted price')
plt.legend()
plt.show()