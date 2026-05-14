# This program demonstrates percentiles and sorting using NumPy

import numpy as np

marks = np.array([78, 85, 90, 66, 72, 88, 95, 60])

sorted_marks = np.sort(marks)

average_marks = np.mean(marks)

above_average = marks[marks > average_marks]

print("Sorted Marks:")
print(sorted_marks)

print("\n25th Percentile:")
print(np.percentile(marks, 25))

print("\n50th Percentile:")
print(np.percentile(marks, 50))

print("\n75th Percentile:")
print(np.percentile(marks, 75))

print("\nStudents Scoring Above Average:")
print(len(above_average))
