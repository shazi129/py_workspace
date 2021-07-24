import os
import numpy as np
import tensorflow as tf
from tensorflow import keras

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_test = x_test.reshape(10000, 784).astype("float32") / 255

this_path = os.path.split(os.path.realpath(__file__))[0]
save_path = "%s/saved_model_1" % this_path

new_model = keras.models.load_model(save_path)
test_scores = new_model.evaluate(x_test, y_test, verbose=2)
print("Test loss:", test_scores[0])
print("Test accuracy:", test_scores[1])