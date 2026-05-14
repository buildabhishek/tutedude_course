# This program demonstrates a safe shopping cart using exception handling

cart = []
total_bill = 0

while True:
    user_input = input("Enter price or 'q' to quit: ")

    if user_input == 'q':
        break

    try:
        price = float(user_input)

        if price < 0:
            raise ValueError("Price cannot be negative")

        cart.append(price)
        total_bill = total_bill + price

    except ValueError as error:
        print("Invalid input:", error)

print("Total items:", len(cart))
print("Total bill:", total_bill)
