import numpy as np

a = np.array([[0], [127], [240]], dtype=np.uint8)

print(np.unpackbits(a))