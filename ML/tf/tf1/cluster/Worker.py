import tensorflow as tf

# Configuration of cluster 

worker_hosts = [ "localhost:8001", "localhost:8002", "localhost:8003" ]
cluster = tf.train.ClusterSpec({"worker": worker_hosts})

server = tf.compat.v1.train.Server(cluster,  job_name="worker", task_index=0)
server.join()