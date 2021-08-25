import numpy as np

a = np.random.randn(3, 2)
print(a)

a = np.reshape(a, -1)
print(a)

print(a.shape)

b = np.zeros(6)
print(b.shape)
