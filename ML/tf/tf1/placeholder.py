from numpy.core.fromnumeric import shape
import tensorflow as tf
from tensorflow import keras

#input_tensor = tf.placeholder(tf.float32, shape=(1, 3), name="input_tensor")
#input_tensor = keras.Input(shape=(1, 3))
input_tensor = tf.constant([[1, 2, 3]], dtype=tf.float32)

def build_network():
    layer = keras.layers.Dense(2, activation=tf.tanh)
    return layer(input_tensor)

with tf.Session() as sess:

    nn = build_network()
    for i in range(3):
        #print(sess.run(nn, feed_dict={input_tensor:[[[1, 2, 3]]]}))
        print(sess.run(nn))