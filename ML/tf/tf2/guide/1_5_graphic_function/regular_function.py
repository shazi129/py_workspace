import tensorflow as tf
import timeit

def a_regular_function(x, y, b):
    x = tf.matmul(x, y)
    x = x + b
    return x
a_function_that_uses_a_graph = tf.function(a_regular_function)

@tf.function
def a_decorator_function(x, y, b):
    x = tf.matmul(x, y)
    x = x + b
    return x


x1 = tf.constant([[1.0, 2.0]])
y1 = tf.constant([[2.0], [3.0]])
b1 = tf.constant(4.0)


orig_value = a_regular_function(x1, y1, b1)
print(orig_value)
print("1000 regulat function cost:", timeit.timeit(lambda: a_regular_function(x1, y1, b1), number=1000))

tf_function_value_1 = a_function_that_uses_a_graph(x1, y1, b1)
print(tf_function_value_1)
print("1000 tf_function_value_1 cost:", timeit.timeit(lambda: a_function_that_uses_a_graph(x1, y1, b1), number=1000))

tf_function_value_2 = a_decorator_function(x1, y1, b1)
print(tf_function_value_2)
print("1000 tf_function_value_2 cost:", timeit.timeit(lambda: a_decorator_function(x1, y1, b1), number=1000))


x = tf.random.uniform(shape=[10, 10], minval=-1, maxval=2, dtype=tf.dtypes.int32)

def power(x, y):
    result = tf.eye(10, dtype=tf.dtypes.int32)
    for _ in range(y):
        result = tf.matmul(x, result)
    return result

print("Eager execution:", timeit.timeit(lambda: power(x, 100), number=1000))
power_as_graph = tf.function(power)
print("Graph execution:", timeit.timeit(lambda: power_as_graph(x, 100), number=1000))

#对内部有循环的function有正优化，对于普通function有负优化