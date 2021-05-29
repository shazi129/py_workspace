import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow import keras

class TrainingCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('loss') < 0.5:
            print("=======================================")
            self.model.stop_training = True

if __name__ == "__main__":

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

    training_cb = TrainingCallback()
    model.fit(training_images, training_labels, epochs=5, callbacks=[training_cb])

    model.evaluate(test_images, test_labels)

    classifications = model.predict(test_images)
    print(classifications[0])

    print(test_labels[0])

