import os
import tensorflow as tf
import cProfile

tf.executing_eagerly()

w = tf.Variable([[1.0]])
with tf.GradientTape() as tape:
  loss = w * w * w

grad = tape.gradient(loss, w)
print(grad)