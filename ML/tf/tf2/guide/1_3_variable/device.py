import tensorflow as tf


# Uncomment to see where your variables get placed (see below)
tf.debugging.set_log_device_placement(True)

with tf.device('CPU:1'):

  # Create some tensors
  a = tf.Variable([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
  b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
  c = tf.matmul(a, b)

print(c)