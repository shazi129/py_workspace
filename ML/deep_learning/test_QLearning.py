import time
import gym
import numpy as np

env = gym.make("FrozenLake-v0")

render = False
running_reward = None

Q = np.zeros([env.observation_space.n, env.action_space.n])

learnning_rate = 0.85
lamdb = 0.99
num_episodes = 10000
r_list = []

#训练次数
for i in range(num_episodes):
    episode_time = time.time()
    state = env.reset()
    reward_total = 0

    for j in range(99):
        if render: env.render()

        noise = np.random.randn(1, env.action_space.n) * (1/(i+1))
        action = np.argmax(Q[state,:] + noise)
        state_next, reward, done, _ = env.step(action)

        Q[state, action] = Q[state, action] + learnning_rate * (reward + lamdb * np.max(Q[state_next,:]) - Q[state, action])

        #print("state:%s, action:%s, next_state:%s, reward:%s" %  (state, action, state_next, reward))

        reward_total += reward
        state = state_next

        if done:
            break

    r_list.append(reward_total)
    running_reward = reward_total if running_reward is None else running_reward * 0.99 + reward_total * 0.01
    print("Episode [%d/%d] sum reward: %f running reward: %f took: %.5fs " % \
        (i, num_episodes, reward_total, running_reward, time.time() - episode_time))

#最后打印Q表格，看看Q表格的样子吧。
print("Final Q-Table Values:/n %s" % Q)


