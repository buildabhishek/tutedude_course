# Demonstrates: writing user input to file

file = open("products.txt", "w")

for i in range(3):
    name = input("Enter product name: ")
    price = input("Enter price: ")

    file.write(name + "," + price + "\n")

file.close()

# Read and display
file = open("products.txt", "r")

print("\nProducts List:")
for line in file:
    name, price = line.strip().split(",")
    print("Product:", name, "| Price:", price)

file.close()
