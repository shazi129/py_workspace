import tensorflow as tf
import os

import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


sess = tf.compat.v1.InteractiveSession()

"""
v_1 = tf.constant([1, 2, 3, 4])
v_2 = tf.constant([2, 1, 5, 3])
v_add = tf.add(v_1, v_2)
print(v_add.eval())
"""

matrix = tf.ones([2, 3], tf.int32)

range_t = tf.linspace(2.0,5.0,5)

range = tf.range(10)

I_matrix = tf.eye(5)

X = tf.Variable(I_matrix)
X.initializer.run()

A_matrix = tf.constant([[1, 2]])
B_matrix = tf.constant([[4], [5]])
m_mul = tf.matmul(A_matrix, B_matrix)
print(m_mul.eval())

writer = tf.summary.FileWriter('summary_dir', sess.graph)

sess.close()