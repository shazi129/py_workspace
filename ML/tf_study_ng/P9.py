import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow import keras

(training_images, training_labels), (test_images, test_labels) = keras.datasets.fashion_mnist.load_data()

plt.imshow(training_images[0])

training_images = training_images / 255
test_images = test_images / 255

model = keras.models.Sequential([
    keras.layers.Flatten(),
    keras.layers.Dense(1024, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])

model.compile(optimizer=tf.optimizers.Adam(), loss="sparse_categorical_crossentropy")
model.fit(training_images, training_labels, epochs=5)

model.evaluate(test_images, test_labels)

classifications = model.predict(test_images)
print(classifications[0])

print(test_labels[0])

