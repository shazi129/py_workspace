import tensorflow as tf
tf.compat.v1.disable_eager_execution()

x1 = tf.constant([1.0, 2.0])
y1 = tf.constant([2.0, 3.0])
add = x1 + y1

#非实时运行，Tensor("add:0", shape=(2,), dtype=float32)
print(add)

with tf.compat.v1.Session() as sess:
    print(sess.run(add))  #[3. 5.]
