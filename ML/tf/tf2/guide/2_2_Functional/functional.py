import os
import numpy as np
import tensorflow as tf
from tensorflow import keras

input = keras.Input(shape=(784))

layer1 = keras.layers.Dense(64, activation="relu")
output = layer1(input)

layer2 = keras.layers.Dense(64, activation="relu")
output = layer2(output)

layer3 = keras.layers.Dense(10)
output = layer3(output)

model = keras.Model(inputs=input, outputs=output)

print(model.summary())

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
print("x_tran.shape:" + str(x_train.shape))
print("y_train.shape:" + str(y_train.shape))

x_train = x_train.reshape(60000, 784).astype("float32") / 255
x_test = x_test.reshape(10000, 784).astype("float32") / 255

model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=keras.optimizers.RMSprop(),
    metrics=["accuracy"],
)

history = model.fit(x_train, y_train, batch_size=64, epochs=2, validation_split=0.2)
test_scores = model.evaluate(x_test, y_test, verbose=2)
print("Test loss:", test_scores[0])
print("Test accuracy:", test_scores[1])


this_path = os.path.split(os.path.realpath(__file__))[0]
save_path = "%s/saved_model_1" % this_path
model.save(save_path)


new_model = keras.models.load_model(save_path)
test_scores = new_model.evaluate(x_test, y_test, verbose=2)
print("Test loss:", test_scores[0])
print("Test accuracy:", test_scores[1])

