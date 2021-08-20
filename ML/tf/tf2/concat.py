import tensorflow as tf
import numpy as np

a = tf.constant([[[1, 2, 3, 4], [4, 5, 6, 7], [8, 9, 0, -1]],
                [[11, 12, 13, 14], [14, 15, 16, 17], [18, 19, 10, -11]]], dtype=float)

print(a)

a1, a2 = tf.split(a, 2)
a1 = tf.squeeze(a1)
a2 = tf.squeeze(a2)
print("a1======>" + str(a1))
print("a2======>" + str(a2))


print(tf.concat([a1, a2], axis=-1))


