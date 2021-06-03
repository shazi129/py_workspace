import tensorflow as tf

x = tf.constant(2)
y = tf.constant(4)

op_1 = x + y
op_2 = x - y

fetches = {"op_1": op_1, "op_2": op_2}

with tf.Session() as sess:
    print(sess.run([op_1, op_2]))
    print(sess.run(fetches))