import numpy as np
from keras import Sequential
from keras.layers import Dense

model = Sequential()

model.add(Dense(3, activation='relu', input_dim=2))
model.add(Dense(1))

# создается объектный граф tensorflow
model.compile(optimizer='adam', loss='mae', metrics=['mae'])

x = np.array([[1, 1], [2, 2], [3, 3]], dtype="float32")
y = np.array([2, 4, 6], dtype="float32")

# обучение epochs - кол-во итераций
hist = model.fit(x, y, epochs=300, batch_size=3)

print(hist.history['loss'][-1])

# использование обученной модели
print(model.predict(np.array([[4, 4]], dtype="float32"))) 
print(model.predict(np.array([[1000, 1000]], dtype="float32")))

model.save('my_first_mode.keras')
