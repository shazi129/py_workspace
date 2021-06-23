import tensorflow as tf

# Configuration of cluster 

worker_hosts = [ "9.134.80.230:8001"]
ps_hosts = ["9.134.189.246:8002"]
cluster = tf.train.ClusterSpec({"worker": worker_hosts, "ps":ps_hosts})

server=tf.train.Server(cluster,job_name='worker',task_index=0)#找到‘worker’名字下的，task0，也就是机器A
with tf.device(tf.train.replica_device_setter(worker_device='/job:worker/task:0',cluster=cluster)):
    w=tf.get_variable('w',(2,2),tf.float32,initializer=tf.constant_initializer(2))
    b=tf.get_variable('b',(2,2),tf.float32,initializer=tf.constant_initializer(5))
    addwb=w+b
    mutwb=w*b
    divwb=w/b
 
saver = tf.train.Saver()
summary_op = tf.merge_all_summaries()
init_op = tf.initialize_all_variables()
sv = tf.train.Supervisor(init_op=init_op, summary_op=summary_op, saver=saver)
with sv.managed_session(server.target) as sess:
    while 1:
        print(sess.run([addwb,mutwb,divwb]))
