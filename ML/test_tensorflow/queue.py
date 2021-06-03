
import tensorflow as tf  
  
#创建的图:一个先入先出队列,以及初始化,出队,+1,入队操作  
q = tf.FIFOQueue(3, "float")  
init = q.enqueue_many(([0.1, 0.2, 0.3],))  
x = q.dequeue()  
y = x + 1  
q_inc = q.enqueue([y])  
  
#开启一个session,session是会话,会话的潜在含义是状态保持,各种tensor的状态保持  
with tf.Session() as sess:  
    sess.run(init)

    for i in range(2):  
        sess.run(q_inc)  

    quelen =  sess.run(q.size())  
    for i in range(quelen):  
        print (sess.run(q.dequeue())) 
