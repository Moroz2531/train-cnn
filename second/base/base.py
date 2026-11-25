import os
import numpy as np
import matplotlib.pyplot as plt
from keras import Sequential
from keras.layers import Conv2D, MaxPool2D, GlobalMaxPool2D, Dense
from load_images import load_images_from_path


def model_compile():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        MaxPool2D(),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPool2D(),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPool2D(),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPool2D(),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPool2D(),
        GlobalMaxPool2D(),
        Dense(1024, activation='relu'),
        Dense(10, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    model.summary(line_length=80)
    return model


model = model_compile()

base_dir = '/home/admin/graduate-work/data/spectrograms/voice-data-minist'
x_train, y_train = [], []
x_test, y_test = [], []

# Загружаем по 500 картинок каждого класса и делим без пересечений:
# первые 400 -> train, оставшиеся 100 -> test
for label in range(10):
    folder = os.path.join(base_dir, str(label))
    imgs, lbls = load_images_from_path(folder, label, 100)
    
    x_train.extend(imgs[:50])
    y_train.extend(lbls[:50])
    x_test.extend(imgs[50:])
    y_test.extend(lbls[50:])

x_train = np.array(x_train, dtype='float32') / 255.0
y_train = np.array(y_train)
x_test = np.array(x_test, dtype='float32') / 255.0
y_test = np.array(y_test)

hist = model.fit(
    x_train,
    y_train,
    validation_data=(x_test, y_test),
    batch_size=32,
    epochs=20
)

acc = hist.history['accuracy']
val_acc = hist.history['val_accuracy']
epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, '-', label='Точность обучения')
plt.plot(epochs, val_acc, ':', label='Точность валидации')
plt.title('Точность обучения и валидации')
plt.xlabel('Эпоха')
plt.ylabel('Точность')
plt.grid(True)
plt.legend(loc='lower right')
plt.show()
