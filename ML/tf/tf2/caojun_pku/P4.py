import tensorflow as tf
import numpy as np

#数据转换
a = np.arange(0, 5)
b = tf.convert_to_tensor(a, dtype=tf.int64)
print("========a======\n" + str(a))
print("========b======\n" + str(b))

#初始化
c = tf.zeros([2, 3])
d = tf.ones(4)
e = tf.fill([2, 3], 9)
print("========c======\n" + str(c))
print("========d======\n" + str(d))
print("========e======\n" + str(e))

#随机生成
#1. 正态分布
f = tf.random.normal([2, 2], mean=0.5, stddev=1)
print("========f======\n" + str(f))
#2. 正态分布， 范围在（mean-2*stddev, mean+2*stddev）
g = tf.random.truncated_normal([2, 2], mean=0.5, stddev=1)
print("========g======\n" + str(g))
#3. 纯随机
h = tf.random.uniform([2, 2], minval=0, maxval=1)
print("========h======\n" + str(h))

#最大最小值
i = tf.constant([[1, 2, 3], [7, 8, 9]], dtype=tf.int64)
print("=======min======\n" + str(tf.reduce_min(i)))
print("=======max======\n" + str(tf.reduce_max(i)))

#平均值
print("=======col mean======\n" + str(tf.reduce_mean(i, axis=0)))
print("=======row mean======\n" + str(tf.reduce_mean(i, axis=1)))

print("=======col sum======\n" + str(tf.reduce_sum(i, axis=0)))
print("=======row sum======\n" + str(tf.reduce_sum(i, axis=1)))