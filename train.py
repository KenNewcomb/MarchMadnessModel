import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models, optimizers
from tensorflow.keras.layers import Dense, Dropout
from tqdm import tqdm
import pickle
import numpy as np
from sklearn.model_selection import train_test_split

# Load data.
with open('vectors/X_data', 'rb') as f:
    X_data = np.asarray(pickle.load(f))
with open('vectors/y_data', 'rb') as f:
    y_data = np.asarray(pickle.load(f))

X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=420)

from tensorflow.keras.utils import to_categorical
y_train = to_categorical(y_train)
y_test  = to_categorical(y_test)


model = models.Sequential()
model.add(Dense(100, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))
#opt = tf.keras.optimizers.Adam(0.0001)

es = tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=50)
adam = optimizers.Adam(lr=0.0001)
model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, batch_size=None, epochs=5000, callbacks=[es], validation_data=(X_test, y_test))
#history = model.fit(X_train, y_train, batch_size=1, epochs=5000)

model.save("model.h5")
