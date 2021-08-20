import numpy as np

a = np.array([1, 2, 3, 4, 5, 6, 7])
print(np.nonzero(a)[0])
print(np.max(a))

b = np.array([0, 0])

a[3:5] = b

print(a.shape)



mask = np.zeros(5, dtype=bool)

#mask[2] = True

print(mask)
print(np.sum(mask))
print(np.nonzero(mask)[0].shape[0])

