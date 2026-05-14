# Demonstrates: append mode

file = open("sales_data.txt", "a")

new_sales = [2000, 2500, 1700]

for s in new_sales:
    file.write(str(s) + "\n")

file.close()

# Print full file
file = open("sales_data.txt", "r")
content = file.readlines()

print("Updated File:")
for line in content:
    print(line.strip())

print("Total lines:", len(content))

file.close()
