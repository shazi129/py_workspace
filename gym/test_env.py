import gym

env = gym.make("FrozenLake-v0", is_slippery=True)
env.reset()
env.render()

print("Action space: ", env.action_space)
print("Observation space: ", env.observation_space)

MAX_ITERATIONS = 10
for i in range(MAX_ITERATIONS):
    random_action = env.action_space.sample()
    new_state, reward, done, info = env.step(random_action)
    env.render()
    if done:
        break