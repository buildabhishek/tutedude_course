# This program demonstrates aggregation operations using NumPy

import numpy as np

data = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])

print("Data Array:")
print(data)

print("\nRow-wise Sum:")
print(np.sum(data, axis=1))

print("\nColumn-wise Sum:")
print(np.sum(data, axis=0))

print("\nMinimum Value:")
print(np.min(data))

print("\nMaximum Value:")
print(np.max(data))

print("\nOverall Mean:")
print(np.mean(data))
