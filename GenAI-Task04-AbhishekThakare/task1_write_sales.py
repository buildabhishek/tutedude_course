# Demonstrates: writing to file using write mode

sales = [1200, 450, 980, 1500, 3000]

file = open("sales_data.txt", "w")

for s in sales:
    file.write(str(s) + "\n")

file.close()

# Read and print
file = open("sales_data.txt", "r")
print(file.read())
file.close()
