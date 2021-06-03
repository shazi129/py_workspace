import numpy as np

A_matrix = np.array([[1, 2]])
B_matrix = np.array([[4], [5]])

print(A_matrix * B_matrix)
print(np.dot(A_matrix, B_matrix))


for i in range(1, 3):
    print(i)