# This program demonstrates a mini sales analysis using NumPy

import numpy as np

sales = np.array([1200, 1500, 900, 2000, 1800, 1700, 1600])

print("Sales Data:")
print(sales)

print("\nTotal Weekly Sales:")
print(np.sum(sales))

print("\nAverage Daily Sales:")
print(np.mean(sales))

print("\nHighest and Lowest Sales:")
print("Highest:", np.max(sales))
print("Lowest:", np.min(sales))

print("\nStandard Deviation:")
print(np.std(sales))

average_sales = np.mean(sales)

above_average_days = sales[sales > average_sales]

print("\nDays with Sales Above Average:")
print(above_average_days)
