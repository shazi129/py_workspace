import tensorflow as tf
from tensorflow import keras

#tf.compat.v1.disable_eager_execution()

tensor = tf.constant([[1, 2, 3]], dtype=tf.float32)

layer = keras.layers.Dense(2, activation=tf.tanh)
tensor = layer(tensor)

print(tensor)