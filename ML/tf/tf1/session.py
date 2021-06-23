import tensorflow as tf
import numpy as np

message = tf.constant('Welcome to the exciting world of Deep Neural Networks!')

def build_add():
    v_1 = tf.constant([1, 2, 3])
    v_2 = tf.constant([3, 4, 5])
    return tf.add(v_1, v_2)

with tf.Session() as sess:
    tensor = build_add()
    print(sess.run(tensor))