import tensorflow as tf

class MyModel(tf.Module):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.w = tf.Variable(5.0)
        self.b = tf.Variable(0.0)

    def __call__(self, x):
        return self.w * x + self.b

def loss(target_y, predicted_y):
    return tf.reduce_mean(tf.pow(target_y - predicted_y, 2))

def train_once(model, x, target_y, learning_rate):

    with tf.GradientTape() as t:
        l = loss(target_y, model(x))

    dw, db = t.gradient(l, [model.w, model.b])
    model.w.assign_sub(learning_rate * dw)
    model.b.assign_sub(learning_rate * db)

def train(model, x, y, learning_rate, epoches):

    w = []
    b = []

    for epoch in epoches:
        train_once(model, x, y, learning_rate)

        w.append(model.w.numpy())
        b.append(model.b.numpy())

        current_loss = loss(y, model(x))

        print("Epoch %2d: W=%1.2f b=%1.2f, loss=%2.5f" % (epoch, w[-1], b[-1], current_loss))

    return w, b

if __name__ == "__main__":
    model = MyModel()
    print(model(3.0))

    print(loss(tf.constant([1.0, 2.0]), tf.constant([0.0, 4.0])))