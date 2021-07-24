import numpy as np
import tensorflow as tf

logits = np.random.randn(10, 5)
print(logits)

logits = tf.convert_to_tensor(logits)
print(tf.shape(logits))
print(tf.shape(logits)[:-1])
print(tf.shape(logits)[:1])

categorical = tf.random.categorical(logits, 1)
max = tf.math.argmax(logits, axis=-1)



print(categorical)
print(max)

print(tf.squeeze(categorical))