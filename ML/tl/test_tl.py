import tensorlayer as tl


for _ in range(1000):
    print(tl.rein.choice_action_by_probs(probs=[0.999, 0.001], action_list=['a', 'b']))