import tensorflow as tf
import os
import sys

from dense import Dense

class SequentialModule(tf.Module):
    def __init__(self, name=None):
        super().__init__(name=name)

        self.dense_1 = Dense(in_features=3, out_features=3)
        self.dense_2 = Dense(in_features=3, out_features=2)

    @tf.function
    def __call__(self, x):
        x = self.dense_1(x)
        return self.dense_2(x)

if __name__ == "__main__":
    # You have made a model!
    my_model = SequentialModule(name="the_model")

    # Call it, with random results
    print("Model results:", my_model(tf.constant([[2.0, 2.0, 2.0]])))

    for var in my_model.variables:
        print(var, "\n")


