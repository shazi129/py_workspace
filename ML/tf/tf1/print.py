import tensorflow as tf

def build_graph():
    x=tf.constant([[2.0,3.0,4.0,5.0, -1000.0, 1000.0]])
    x=tf.Print(x,[x,x.shape,'test', x],message='Debug message:',summarize=100)
    softmax = tf.nn.softmax(x)
    c = tf.random.categorical(x, 1)
    return c

with tf.Session() as sess:
    print(sess.run(build_graph()))