import tensorflow as tf
import numpy as np


action = np.array([[1, 0, 0]])
logits = np.array([[4.,1.,-2.]])

labels = np.argmax(action, axis=-1)
print(labels)

softmax = tf.nn.softmax(logits)
print(softmax)

log_softmax = tf.nn.log_softmax(logits)
print(log_softmax)

result = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels, logits=logits)
print(result)