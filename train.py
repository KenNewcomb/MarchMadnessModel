import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models, optimizers
from tensorflow.keras.layers import Dense, Dropout
from tqdm import tqdm
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
import sys
import matplotlib.pyplot as plt

# Load data.
with open('vectors/X_data', 'rb') as f:
    X_data = np.asarray(pickle.load(f))
with open('vectors/y_data', 'rb') as f:
    y_data = np.asarray(pickle.load(f))

# Since I'm using both representations of each game (T1:T2, T2:T1), I want to keep pairs together. model.fit(shuffle=True) will shuffle.
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, shuffle=False)

from tensorflow.keras.utils import to_categorical
y_train = to_categorical(y_train)
y_test  = to_categorical(y_test)


model = models.Sequential()
model.add(Dense(150, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(150, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

es = tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=100, restore_best_weights=True)
adam = optimizers.Adam(lr=0.0001)
model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, batch_size=None, epochs=1000, callbacks=[es], validation_data=(X_test, y_test), shuffle=True)

model.save("model.h5")

if len(sys.argv) > 1 and sys.argv[1] == 'p':
    print("Plotting...")
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.legend(['training error', 'validation error'], loc='upper left')
    plt.show()
