import tensorflow as tf 
import numpy as np

# 一些fake参数
BATCH_SIZE = 128
MAP_SIZE = 10
MAX_EQUIP_NUM = 3
MAX_FETTER_NUM = 3
MAX_HERO_NUM = 10
GLOBAL_FEATURE_NUM = 16
HERO_EMBEDDING_SIZE = 32
EQUIP_EMBEDDING_SIZE = 32
FETTER_EMBEDDING_SIZE = 32
GLOBAL_FEATURE_HIDDEN_SIZE = 128
ENCODE_HIDDEN_SIZE = 512
PROCESS_SET_SIZE = 32
NUM_FEATURES = 16


class Encoding(tf.keras.Model):
    def __init__(self):
        super(Encoding, self).__init__()
        self.global_feature_layer = tf.keras.layers.Dense(units=GLOBAL_FEATURE_HIDDEN_SIZE, activation=tf.nn.relu)
        self.hero_id_embeddings_layer = tf.keras.layers.Embedding(input_dim=MAX_HERO_NUM+1, output_dim=HERO_EMBEDDING_SIZE)
        self.equip_id_embeddings_layer = tf.keras.layers.Embedding(input_dim=MAX_EQUIP_NUM+1, output_dim=EQUIP_EMBEDDING_SIZE)
        self.equip_process_set_layer = ProcessSet(units=PROCESS_SET_SIZE)
        self.fetter_id_embeddings_layer = tf.keras.layers.Embedding(input_dim=MAX_FETTER_NUM+1, output_dim=FETTER_EMBEDDING_SIZE)
        self.fetter_process_set_layer = ProcessSet(units=PROCESS_SET_SIZE)
        self.grid_cnn_layer1 = tf.keras.layers.Conv2D(filters=32, kernel_size=3, strides=(1,1), padding="same", activation=tf.nn.relu)
        self.grid_cnn_layer2 = tf.keras.layers.Conv2D(filters=32, kernel_size=3, strides=(1,1), padding="same", activation=tf.nn.relu)
        self.flattern_layer = tf.keras.layers.Flatten()
        self.encode_layer = tf.keras.layers.Dense(units=ENCODE_HIDDEN_SIZE, activation=tf.nn.relu)
    
    def call(self, inputs):
        self.get_hero_state(inputs["hero_id"])
        print("embedding hero_state =======> " + str(self.hero_state.shape))

        self.get_equip_state(inputs["equip_id"])
        #print("embedding equip_state =======> " + str(self.equip_state))

        self.get_fetter_state(inputs["fetter_id"])
        #print("embedding fetter_state =======> " + str(self.fetter_state))
        
        self.battle_grid = tf.concat([self.hero_state, self.equip_state, self.fetter_state], axis=-1)
        print("battle_grid =======> " + str(self.battle_grid.shape))

        battle_state = self.grid_cnn_layer1(self.battle_grid)
        battle_state = self.grid_cnn_layer2(battle_state)
        self.battle_state = self.flattern_layer(battle_state)
        self.get_global_state(inputs["global_feature"])
        encode_state_raw = tf.concat([self.global_state, self.battle_state], axis=-1)
        # 最终encode得到state
        self.encode_state = self.encode_layer(encode_state_raw)

    def get_hero_state(self, hero_id):
        self.hero_state = self.hero_id_embeddings_layer(hero_id)
        return self.hero_state
    
    def get_equip_state(self, equip_id):
        equip_id_embeddings_raw = self.equip_id_embeddings_layer(equip_id)
        self.equip_state = self.equip_process_set_layer(equip_id_embeddings_raw)
        return self.equip_state

    def get_fetter_state(self, fetter_id):
        fetter_id_embeddings_raw = self.fetter_id_embeddings_layer(fetter_id)
        self.fetter_state = self.fetter_process_set_layer(fetter_id_embeddings_raw)
        return self.fetter_state

    def get_global_state(self, global_feature):
        self.global_state = self.global_feature_layer(global_feature)
        return self.global_state


class ProcessSet(tf.keras.layers.Layer):
    def __init__(self, units):
        super(ProcessSet, self).__init__()
        self.process_set_layer = tf.keras.layers.Dense(units=PROCESS_SET_SIZE, activation=tf.nn.relu)
        self.process_set = tf.keras.layers.Dense(units=units)

    def call(self, inputs):
        hidden = self.process_set_layer(inputs)
        hidden = self.process_set(hidden)
        process_res = tf.reduce_max(hidden, axis=-2)
        return process_res



if __name__ == "__main__":
    # fake 输入的维度
    inputs = {}
    inputs["hero_id"] = np.random.randint(low=0, high=MAX_HERO_NUM+1, size=[BATCH_SIZE, MAP_SIZE, MAP_SIZE])
    print("hero_id =======> " + str(inputs["hero_id"].shape))

    inputs["equip_id"] = np.random.randint(low=0, high=MAX_EQUIP_NUM+1, size=[BATCH_SIZE, MAP_SIZE, MAP_SIZE, MAX_EQUIP_NUM])
    #print("equip_id =======> " + str(inputs["equip_id"]))

    inputs["fetter_id"] = np.random.randint(low=0, high=MAX_FETTER_NUM+1, size=[BATCH_SIZE, MAP_SIZE, MAP_SIZE, MAX_FETTER_NUM])
    #print("fetter_id =======> " + str(inputs["fetter_id"]))

    inputs["global_feature"] = np.random.uniform(size=[BATCH_SIZE, GLOBAL_FEATURE_NUM])
    test_model = Encoding()
    test_model(inputs)
