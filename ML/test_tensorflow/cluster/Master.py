import tensorflow.compat.v1 as tf
import numpy as np

tf.disable_eager_execution()

train_X = np.random.rand(100).astype(np.float32)
train_Y = train_X * 0.1 + 0.3

# 选择变量存储位置和op执行位置，这里全部放在worker的第1个task上
with tf.device("/job:worker/replica:0/task:0"):
    X = tf.placeholder(tf.float32)
    Y = tf.placeholder(tf.float32)
    w = tf.Variable(0.0, name="weight")
    b = tf.Variable(0.0, name="reminder")
    y = w * X + b
    loss = tf.reduce_mean(tf.square(y - Y))

    init_op = tf.global_variables_initializer()
    train_op = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

# 选择创建session使用的master
with tf.Session("grpc://localhost:8001") as sess:
    sess.run(init_op)
    for i in range(500):
        sess.run(train_op, feed_dict={X: train_Y, Y: train_Y})
        if i % 50 == 0:
            print("%s, %s, %s" % (i, str(sess.run(w)), str(sess.run(b))))

    print(sess.run(w))
    print(sess.run(b))
