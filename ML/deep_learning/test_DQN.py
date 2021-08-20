"""
Deep Q-Network Q(a, s)
-----------------------
TD Learning, Off-Policy, e-Greedy Exploration (GLIE).
Q(S, A) <- Q(S, A) + alpha * (R + lambda * Q(newS, newA) - Q(S, A))
delta_w = R + lambda * Q(newS, newA)
See David Silver RL Tutorial Lecture 5 - Q-Learning for more details.
Reference
----------
original paper: https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf
EN: https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-0-q-learning-with-tables-and-neural-networks-d195264329d0#.5m3361vlw
CN: https://zhuanlan.zhihu.com/p/25710327
Note: Policy Network has been proved to be better than Q-Learning, see tutorial_atari_pong.py
Environment
-----------
# The FrozenLake v0 environment
https://gym.openai.com/envs/FrozenLake-v0
The agent controls the movement of a character in a grid world. Some tiles of
the grid are walkable, and others lead to the agent falling into the water.
Additionally, the movement direction of the agent is uncertain and only partially
depends on the chosen direction. The agent is rewarded for finding a walkable
path to a goal tile.
SFFF       (S: starting point, safe)
FHFH       (F: frozen surface, safe)
FFFH       (H: hole, fall to your doom)
HFFG       (G: goal, where the frisbee is located)
The episode ends when you reach the goal or fall in a hole. You receive a reward
of 1 if you reach the goal, and zero otherwise.
Prerequisites
--------------
tensorflow>=2.0.0a0
tensorlayer>=2.0.0
To run
-------
python tutorial_DQN.py --train/test
"""
import os
import argparse
import time
import gym
import numpy as np
import tensorflow as tf
from tensorflow import keras


#####################  hyper parameters  ####################
lambd = .99             # 折扣率(decay factor)
e = 0.5                 # epsilon-greedy算法参数，越大随机性越大，越倾向于探索行为。
num_episodes = 5000    # 迭代次数
render = False          # 是否渲染游戏
running_reward = None
is_training = False


env = gym.make('FrozenLake-v0')  #定义环境

##################### DQN ##########################

## 把分类的数字表示，变成onehot表示。
# 例如有4类，那么第三类变为：[0,0,1,0]的表示。
def to_one_hot(i, n_classes=None):
    a = np.zeros(n_classes, 'uint8')    # 这里先按照分类数量构建一个全0向量
    a[i] = 1                            # 然后点亮需要onehot的位数。
    return a


## Define Q-network q(a,s) that ouput the rewards of 4 actions by given state, i.e. Action-Value Function.
# encoding for state: 4x4 grid can be represented by one-hot vector with 16 integers.
def get_model(inputs_shape):
    '''
    定义Q网络模型：
    1. 注意输入的shape和输出的shape
    2. W_init和b_init是模型在初始化的时候，控制初始化参数的随机。该代码中用正态分布，均值0，方差0.01的方式初始化参数。
    '''

    """
    ni = tl.layers.Input(inputs_shape, name='observation')
    nn = tl.layers.Dense(4, act=None, W_init=tf.random_uniform_initializer(0, 0.01), b_init=None, name='q_a_s')(ni)
    return tl.models.Model(inputs=ni, outputs=nn, name="Q-Network")
    """
    return keras.models.Sequential([
        keras.layers.Input(inputs_shape, name='observation'),
        keras.layers.Dense(128, activation=tf.nn.leaky_relu, name='q_a_s'),
        keras.layers.Dense(4, activation=tf.nn.leaky_relu, name="Q-Network")
    ])

def get_save_path():
    this_path = os.path.split(os.path.realpath(__file__))[0]
    return os.path.abspath("%s/../../dqn_model" % this_path)

def save_ckpt(model):  # save trained weights
    '''
    保存参数
    '''
    model.save(get_save_path())


def load_ckpt():  # load trained weights
    '''
    加载参数
    '''
    return keras.models.load_model(get_save_path())

def training_batch():

    global lambd
    global e
    global num_episodes
    global render
    global running_reward
    global env #定义环境

    qnetwork = get_model((16,))            #定义inputshape[None,16]。16是state数量
    qnetwork.compile()
    train_weights = qnetwork.trainable_weights  #模型的参数
    optimizer = tf.optimizers.SGD(learning_rate=0.1)   #定义优化器

    t0 = time.time()
    for i in range(num_episodes):
        ## 重置环境初始状态
        s = env.reset()
        rAll = 0

        s_batch = []
        a_batch = []
        q_batch = []
        r_batch = []

        for j in range(99):             # 最多探索99步。因为环境状态比较少，99步一般也够探索到最终状态了。
            if render: env.render()

            s_hot = np.asarray([to_one_hot(s, 16)], dtype=np.float32)
            s_batch.append(s_hot[0])

            ## 把state放入network，计算Q值。
            ## 注意，这里先把state进行onehote处理，这里注意解释下什么是onehot
            ## 输出，这个状态下，所有动作的Q值，也就是说，是一个[None,4]大小的矩阵
            Q = qnetwork(s_hot).numpy()
            q_batch.append(Q[0])

            # 在矩阵中找最大的Q值的动作
            a = np.argmax(Q, 1)
            # e-Greedy：如果小于epsilon，就智能体随机探索。否则，就用最大Q值的动作。
            if np.random.rand(1) < e:
                a[0] = env.action_space.sample()
            a_batch.append(a)

            # 输入到环境，获得下一步的state，reward，done
            s1, r, d, _ = env.step(a[0])
            r_batch.append(r)

            #更新epsilon，让epsilon随着迭代次数增加而减少。
            #目的就是智能体越来越少进行“探索”
            if d ==True:
                break
            s = s1

        target_qvalues = np.array(r_batch, dtype=np.float32)

        total_reward = np.sum(target_qvalues)

        for index in range(len(target_qvalues)):
            target_qvalues[index] = np.sum(target_qvalues[index:])

        target_qvalues_batch = []
        for index in range(len(q_batch)):
            q = q_batch[index]
            a = a_batch[index][0]
            q[a] = target_qvalues[index]
            target_qvalues_batch.append(q)
        target_qvalues_batch = np.asarray(target_qvalues_batch, dtype=np.float32)

        with tf.GradientTape() as tape:
            _qvalues = qnetwork(np.asarray(s_batch, dtype=np.float32))  #把s放入到Q网络，计算_qvalues。
            _loss = tf.losses.mean_squared_error(target_qvalues_batch, _qvalues)

        grad = tape.gradient(_loss, train_weights)
            # 应用梯度到网络参数求导 
        optimizer.apply_gradients(zip(grad, train_weights))

        # 累计reward，并且把s更新为newstate
        rAll = np.sum(r_batch)
           
        ## 这里的running_reward用于记载每一次更新的总和。为了能够更加看清变化，所以大部分是前面的。只有一部分是后面的。
        running_reward = rAll if running_reward is None else running_reward * 0.99 + rAll * 0.01
        # print("Episode [%d/%d] sum reward: %f running reward: %f took: %.5fs " % \
        #     (i, num_episodes, rAll, running_reward, time.time() - episode_time))
        print('Episode: {}/{}  | Episode Reward: {:.4f} | Running Average Reward: {:.4f}  | Running Time: {:.4f} | step:{}'\
        .format(i, num_episodes, rAll, running_reward,  time.time()-t0, len(a_batch) ))
    save_ckpt(qnetwork)  # save model

def predict():

    global lambd
    global num_episodes
    global render
    global running_reward
    global env #定义环境

    t0 = time.time()
    qnetwork = load_ckpt()  # load model
    for i in range(num_episodes):
        ## Reset environment and get first new observation
        episode_time = time.time()
        s = env.reset()  # observation is state, integer 0 ~ 15
        rAll = 0
        for j in range(99):  # step index, maximum step is 99
            if render: env.render()
            
            ## Choose an action by greedily (with e chance of random action) from the Q-network
            allQ = qnetwork(np.asarray([to_one_hot(s, 16)], dtype=np.float32)).numpy()
            a = np.argmax(allQ, 1)  # no epsilon, only greedy for testing

            ## Get new state and reward from environment
            s1, r, d, _ = env.step(a[0])
            rAll += r
            s = s1
            ## Reduce chance of random action if an episode is done.
            if d ==True:
                break

        ## Note that, the rewards here with random action
        running_reward = rAll if running_reward is None else running_reward * 0.99 + rAll * 0.01
        # print("Episode [%d/%d] sum reward: %f running reward: %f took: %.5fs " % \
        #     (i, num_episodes, rAll, running_reward, time.time() - episode_time))
        print('Episode: {}/{}  | Episode Reward: {:.4f} | Running Average Reward: {:.4f}  | Running Time: {:.4f}'\
        .format(i, num_episodes, rAll, running_reward,  time.time()-t0 ))

if __name__ == '__main__':

    print("is_training:%s, taining_batch:%s" % (is_training, taining_batch))

    if is_training:
        training_batch()
    else:
        predict()