import tensorflow as tf
import matplotlib.pyplot as plt

from my_model import MyModel, train

TRUE_W = 3.0
TRUE_B = 2.0

NUM_EXAMPLE = 1000

x = tf.random.normal(shape=[NUM_EXAMPLE])
noise = tf.random.normal(shape=[NUM_EXAMPLE])
y = x * TRUE_W + TRUE_B + noise


model = MyModel()

epochs = range(10)

w, b = train(model, x, y, 0.1, epochs)
predict_y = model(x)

plt.scatter(x, y, c="b")
plt.scatter(x, predict_y, c="r")

#plt.plot(epochs, w, "r", epochs, b, "b")

#plt.plot([TRUE_W] * len(epochs), "r--", [TRUE_B] * len(epochs), "b--")

plt.show()