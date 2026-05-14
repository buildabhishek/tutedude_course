# Demonstrates: safe file handling using try-except (no external libraries)
filename = input("Enter filename: ")

try:
    file = open(filename, "r")
    print(file.read())
    file.close()
except FileNotFoundError:
    print("File not found. Please check the filename.")


# Demonstrates: safe file handling using os.path
import os

filename = input("Enter filename: ")

if os.path.exists(filename):
    file = open(filename, "r")
    print(file.read())
    file.close()
else:
    print("File not found. Please check the filename.")
