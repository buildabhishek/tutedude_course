# Demonstrates: reading + calculations

file = open("sales_data.txt", "r")
lines = file.readlines()
file.close()

sales = []

for line in lines:
    sales.append(int(line.strip()))

total = sum(sales)
highest = max(sales)
lowest = min(sales)
average = total / len(sales)

print("Total:", total)
print("Highest:", highest)
print("Lowest:", lowest)
print("Average:", average)
