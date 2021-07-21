import numpy as np

logits = np.random.randn(10, 5)
print(logits)

import tensorflow as tf
logits = tf.convert_to_tensor(logits)

print(tf.random.categorical(logits, 1))