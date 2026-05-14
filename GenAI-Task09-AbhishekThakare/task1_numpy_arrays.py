# This program demonstrates creating NumPy arrays

import numpy as np

array1 = np.arange(1, 11)

array2 = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

array3 = np.array([10, 20, 30, 40, 50])

print("1D Array:")
print(array1)

print("\n2D Array:")
print(array2)

print("\nNumPy Array from List:")
print(array3)

print("\nShape of array1:", array1.shape)
print("Shape of array2:", array2.shape)
print("Shape of array3:", array3.shape)

print("\nData Type of array1:", array1.dtype)
print("Data Type of array2:", array2.dtype)
print("Data Type of array3:", array3.dtype)
