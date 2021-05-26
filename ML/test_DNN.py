import tensorflow as tf
import tensorlayer as tl

from tensorflow import keras


(train_images, train_labels), (test_images, test_labels) = keras.datasets.fashion_mnist.load_data()
print(train_images.shape)
print(train_labels.shape)
print(test_images.shape)
print(test_labels.shape)

def get_model(input_shape):
    input = tl.layers.input(input_shape)
    cnn = tl.layers.Conv2d(n_filter=32, filter_size=(3, 3), strides=(1, 1), act='relu', padding='SAME')(inputs)
    flatten = tl.layers.Flatten()(cnn)

    fc = tl.layers.Dense(n_units=128, act='relu')(flatten)
    outputs = tl.layers.Dense(n_units=10,act=tf.nn.softmax)(fc)
    return tl.models.Model(inputs=inputs, outputs=outputs)

with tf.GradientTape() as tape:
    logits = network(images)
    loss = tf.losses.sparse_categorical_crossentropy(labels,logits)

    grads = tape.gradient(loss, network.trainable_weights)
    optimizer.apply_gradients(zip(grads,network.trainable_weights))

    optimizer = tf.optimizers.Adam()

def predict():
    acc = 0
    for i in range(test_lables.shape[0]):
        if np.argmax(predictions[i])==test_lables[i]:
            acc += 1
    print('accurcy:%f'%(acc/test_lables.shape[0]))