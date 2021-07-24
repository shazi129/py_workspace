import tensorflow as tf
 
labels = [0]
logits = [[4.,1.,-2.]]
 
result = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels, logits=logits)

print(result)