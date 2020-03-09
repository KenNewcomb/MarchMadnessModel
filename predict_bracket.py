import tensorflow as tf
import numpy as np

year = 2020
team1 = 'Sacred Heart'
team2 = 'St. Francis (PA)'
seed1 = 3
seed2 = 2
model = tf.keras.models.load_model('model.h5')
x = np.asarray(x)
x = np.reshape(x, (1, 40))
print(x)
print(model.predict([np.asarray(x)]))
