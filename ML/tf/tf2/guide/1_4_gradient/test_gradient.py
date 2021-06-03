import tensorflow as tf

x = tf.ones((2, 3))

with tf.GradientTape(persistent=True) as t:
    t.watch(x)
    y = tf.reduce_sum(x)
    z = y * y

"""
对于此处：
x = [[x_11, x_12], [x_21, x_22]]
y = x_11 + x_12 + x_21 + x_22

dy / dx = [[dy/dx_11, dy/dx_12], [dy/dx_21, dy/dx_22]]

"""
dy_dx = t.gradient(y, x)
print("dy_dx:  " + str(dy_dx))

dz_dy = t.gradient(z, y)
print("dz_dy:  " + str(dz_dy))

dz_dx = t.gradient(z, x)
print("dz_dx:  " + str(dz_dx))