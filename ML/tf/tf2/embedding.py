import tensorflow as tf 
import numpy as np

hero_embedding_layer = tf.keras.layers.Embedding(input_dim=40000, output_dim=5)
equip_embedding_layer = tf.keras.layers.Embedding(input_dim=5000, output_dim=5)

num = 4

ground_state = tf.convert_to_tensor(np.array([11002, 21002, 21003, 22006, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                  1002, 2102, 2003, 2006, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                  1002, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=int))

hero_id = tf.convert_to_tensor(np.array([11002, 21002, 21003, 22006, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=int))
equip1_id = tf.convert_to_tensor(np.array([1002, 2102, 2003, 2006, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=int))
equip2_id = tf.convert_to_tensor(np.array([1002, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=int))
equip3_id = tf.convert_to_tensor(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=int))


hero_id = tf.reshape(hero_id, (4, 4))
equip1_id = tf.reshape(equip1_id, (4, 4))
equip2_id = tf.reshape(equip2_id, (4, 4))
equip3_id = tf.reshape(equip3_id, (4, 4))

print("hero_id ==========> " + str(hero_id))

embedding_hero_id = hero_embedding_layer(hero_id)
embedding_equip1_id = equip_embedding_layer(equip1_id)
embedding_equip2_id = equip_embedding_layer(equip2_id)
eembedding_quip3_id = equip_embedding_layer(equip3_id)

print("embedding_hero_id ==========> " + str(embedding_hero_id))



embedding_ground_state = tf.concat([embedding_hero_id, embedding_equip1_id, embedding_equip2_id, eembedding_quip3_id], axis=-1)
print("embedding_ground_state =====> " + str(embedding_ground_state))

embedding_ground_state = tf.expand_dims(embedding_ground_state, axis=0)# tf.reshape(embedding_ground_state, (-1, 4, 4, 20))
print("reshape embedding_ground_state =====> " + str(embedding_ground_state))


ground_cnn_layer = tf.keras.layers.Conv2D(filters=3, kernel_size=3, strides=(1,1), padding="same", activation=tf.nn.relu)
ground_cnn_tensor = ground_cnn_layer(embedding_ground_state)
print("ground_cnn_tensor =====> " + str(ground_cnn_tensor))
