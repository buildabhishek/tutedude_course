# Demonstrates: file writing + calculations

products = {
    "Mouse": 500,
    "Keyboard": 800,
    "Monitor": 7000,
    "Pendrive": 400,
    "Camera": 5000
}

discount = float(input("Enter discount %: "))

file = open("discounted_products.txt", "w")

total = 0
count = 0

for name, price in products.items():
    discounted_price = price - (price * discount / 100)
    file.write(f"{name} | {price} | {discounted_price}\n")

    total += discounted_price
    count += 1

average = total / count

file.write(f"\nTotal: {total}")
file.write(f"\nAverage Discounted Price: {average}")

file.close()

# Print file
file = open("discounted_products.txt", "r")
print(file.read())
file.close()
