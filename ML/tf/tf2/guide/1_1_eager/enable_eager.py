import tensorflow as tf

x1 = tf.constant([1.0, 2.0])
y1 = tf.constant([2.0, 3.0])
add = x1 + y1

#实时运行，tf.Tensor([3. 5.], shape=(2,), dtype=float32)
print(add)
