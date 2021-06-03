import tensorflow as tf
import numpy as np

print("======================张量的维度==================")

#0维张量， 数值
rank_0_tensor = tf.constant(4)
print("rank 0 tensor:   " + str(rank_0_tensor))

#一维张量， 向量
rank_1_tensor = tf.constant([2.0, 3.0, 4.0])
print("rank 1 tensor:   " + str(rank_1_tensor))

#二维张量，矩阵
rank_2_tensor = tf.constant([[1, 2],
                             [3, 4],
                             [5, 6]], dtype=tf.float16)
print("rank 2 tensor:" + str(rank_2_tensor))

#三维张量
rank_3_tensor = tf.constant([
  [[0, 1, 2, 3, 4],
   [5, 6, 7, 8, 9]],
  [[10, 11, 12, 13, 14],
   [15, 16, 17, 18, 19]],
  [[20, 21, 22, 23, 24],
   [25, 26, 27, 28, 29]],])

print("rank 3 tensor:   " + str(rank_3_tensor))

#张量 to numpy
print("rank 2 tensor to numpy:" + str(np.array(rank_2_tensor)))
print("rank 2 tensor to numpy:" + str(rank_2_tensor.numpy()))

print("======================张量的四则运算==================")

a = tf.constant([[1, 2],
                 [3, 4]])

b = tf.constant([[1, 1],
                 [1, 1]]) # Could have also said `tf.ones([2,2])`

print(tf.add(a, b), "\n")
print(tf.multiply(a, b), "\n")
print(tf.matmul(a, b), "\n")

print(a + b, "\n") # element-wise addition
print(a * b, "\n") # element-wise multiplication
print(a @ b, "\n") # matrix multiplication


c = tf.constant([[4.0, 5.0], [10.0, 1.0]])

# Find the largest value
print(tf.reduce_max(c))
# Find the index of the largest value
print(tf.argmax(c))
# Compute the softmax
print(tf.nn.softmax(c))