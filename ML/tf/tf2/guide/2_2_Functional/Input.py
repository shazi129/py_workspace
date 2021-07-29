import numpy as np
import tensorflow as tf
from tensorflow import keras

model = keras.models.Sequential([
        keras.layers.Input((2,), name='observation'),
        keras.layers.Dense(128, activation=tf.nn.leaky_relu, name='q_a_s'),
        keras.layers.Dense(4, activation=tf.nn.leaky_relu, name="Q-Network")
    ])


input = []
input.append([1.0, 2.0])
input.append([2.0, 3.0])

input = np.asarray(input, dtype=np.float32)
print(model(input))