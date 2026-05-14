# Demonstrates: read(), readline(), readlines()

file = open("sales_data.txt", "r")

# read()
print("Full content:")
print(file.read())

file.close()

file = open("sales_data.txt", "r")

# readline()
print("First line:", file.readline())

file.close()

file = open("sales_data.txt", "r")

# readlines()
lines = file.readlines()
numbers = []

for line in lines:
    numbers.append(int(line.strip()))

print("As list:", numbers)

file.close()
