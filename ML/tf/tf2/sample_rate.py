import numpy as np

#样本概率
logits = np.random.randn(1, 100)
logits[0, 0] = 15
logits[0, 1] = -5

#logits = np.array([[5, 4, 3, 2, 1, 0, -1, -2, -3, -4]], dtype=float)
vec_len = logits.shape[1]

import tensorflow as tf
logits = tf.convert_to_tensor(logits)
print(logits)

#将样本概率缩放到一个区间
scale = tf.reduce_max(tf.math.abs(logits)) / 1
scale_logits = logits # / scale
print(scale_logits)

for sample_time in range(10):
    print("sample %sth:" % sample_time)
    sample_times = np.zeros(vec_len)
    for i in range(20000):
        index = tf.random.categorical(scale_logits, 1).numpy()[0][0]
        #index = tf.random.categorical(logits, 1).numpy()[0][0]
        sample_times[index] += 1
    print(sample_times)
