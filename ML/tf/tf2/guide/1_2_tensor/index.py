import tensorflow as tf
import numpy as np


rank_2_tensor = tf.constant([[1, 2],
                               [3, 4],
                               [5, 6]], dtype=tf.float16)

print("Second row:", rank_2_tensor[1, :].numpy())
print("Second column:", rank_2_tensor[:, 1].numpy())
print("Last row:", rank_2_tensor[-1, :].numpy())
print("First item in last column:", rank_2_tensor[0, -1].numpy())
print("Skip the first row:")
print(rank_2_tensor[1:, :], "\n")

#二维张量切片
print("rank_2_tensor[1, :]: " + str(rank_2_tensor[1, :]))
print("rank_2_tensor[:, 1]: " + str(rank_2_tensor[:, 1]))

print("\n")


#三维张量
rank_3_tensor = tf.constant([
  [[0, 1, 2, 3, 4],
   [5, 6, 7, 8, 9]],
  [[10, 11, 12, 13, 14],
   [15, 16, 17, 18, 19]],
  [[20, 21, 22, 23, 24],
   [25, 26, 27, 28, 29]],])

#三维张量切片
print("rank_3_tensor[1, :, :]: " + str(rank_3_tensor[1, :, :]))
print("rank_3_tensor[:, 1, :]: " + str(rank_3_tensor[:, 1, :]))
print("rank_3_tensor[:, :, 1]: " + str(rank_3_tensor[:, :, 1]))