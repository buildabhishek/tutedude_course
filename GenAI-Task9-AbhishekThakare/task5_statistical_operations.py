# This program demonstrates statistical operations using NumPy

import numpy as np

marks = np.array([78, 85, 90, 66, 72, 88, 95, 60])

print("Marks:")
print(marks)

print("\nMean:")
print(np.mean(marks))

print("\nMedian:")
print(np.median(marks))

print("\nVariance:")
print(np.var(marks))

print("\nStandard Deviation:")
print(np.std(marks))

print("\nMinimum and Maximum:")
print("Minimum:", np.min(marks))
print("Maximum:", np.max(marks))

print("\nRange:")
print(np.max(marks) - np.min(marks))
