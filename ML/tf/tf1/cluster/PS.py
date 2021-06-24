import tensorflow as tf

# Configuration of cluster 

worker_hosts = [ "9.134.80.230:9501"]
ps_hosts = ["9.134.189.246:9500"]
cluster = tf.train.ClusterSpec({"worker": worker_hosts, "ps":ps_hosts})

server=tf.train.Server(cluster,job_name='ps',task_index=0)#找到‘worker’名字下的，task0，也就是机器A
server.join()