import tensorflow as tf
import os
from sequential_module import SequentialModule

my_model = SequentialModule(name="the_model")

#save checkpoint
this_path = os.path.split(os.path.realpath(__file__))[0]
chkp_path = "%s/checkpoint/my_checkpoint" % this_path
checkpoint = tf.train.Checkpoint(model=my_model)
checkpoint.write(chkp_path)
print(tf.train.list_variables(chkp_path))

#load checkpoint
new_model = SequentialModule()
new_checkpoint = tf.train.Checkpoint(model=new_model)
new_checkpoint.restore(chkp_path)
print(new_model(tf.constant([[2.0, 2.0, 2.0]])))