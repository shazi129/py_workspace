import time
import tensorflow.compat.v1 as tf

# Configuration of cluster 

worker_hosts = [ "9.134.80.230:9501",  "9.134.189.246:9501"]
ps_hosts = ["9.134.189.246:9500"]
cluster = tf.train.ClusterSpec({"worker": worker_hosts, "ps":ps_hosts})

server=tf.train.Server(cluster,job_name='worker',task_index=0)#找到‘worker’名字下的，task0，也就是机器A
with tf.device(tf.train.replica_device_setter(cluster=cluster)):
    w = tf.get_variable('w',(1),tf.float32,initializer=tf.constant_initializer(2))
    add = tf.add(w, 1)
    update = tf.assign(w, add)

with tf.Session(server.target) as sess:
    sess.run(tf.global_variables_initializer())
    for _ in range(100):
        print("==============================")
        print(sess.run(w))
        print(sess.run(update))
        time.sleep(1)
