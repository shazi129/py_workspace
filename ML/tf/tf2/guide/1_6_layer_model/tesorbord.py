import tensorflow as tf
from sequential_module import SequentialModule
from datetime import datetime
import os

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
this_path = os.path.split(os.path.realpath(__file__))[0]

logdir = "%s/logs/func/%s" % (this_path, stamp)

writer = tf.summary.create_file_writer(logdir)
new_model = SequentialModule()

tf.summary.trace_on(graph=True, profiler=True)


z = print(new_model(tf.constant([[2.0, 2.0, 2.0]])))
with writer.as_default():
    tf.summary.trace_export( name="my_func_trace", step=0, profiler_outdir=logdir)