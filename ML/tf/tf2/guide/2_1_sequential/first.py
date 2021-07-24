import tensorflow as tf
from tensorflow import keras

model = keras.Sequential(
    [
        keras.Input(shape=(None, 2)),
        keras.layers.Dense(2, activation="relu", name="layer1"),
        keras.layers.Dense(3, activation="relu", name="layer2"),
        keras.layers.Dense(4, name="layer3")
    ]
)

print(model.summary())

#keras.utils.plot_model(model, "my_first_model_with_shape_info.png", show_shapes=True)