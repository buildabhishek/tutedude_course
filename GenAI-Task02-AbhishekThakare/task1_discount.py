# Task 1: Discount Rules

user_input = input("Enter order amount: ")

# Handle non-numeric input
if not user_input.isdigit():
    print("Invalid input! Please enter a number.")
else:
    order_amount = int(user_input)

    # Apply discount
    if order_amount >= 2000:
        discount = 0.15
    elif order_amount >= 1500:
        discount = 0.10
    elif order_amount >= 1000:
        discount = 0.07
    else:
        discount = 0

    discount_amount = order_amount * discount
    final_amount = order_amount - discount_amount

    # Extra: tax 5%
    tax = final_amount * 0.05
    total = final_amount + tax

    print("Original:", order_amount)
    print("Discount:", discount_amount)
    print("After Discount:", final_amount)
    print("Tax (5%):", tax)
    print("Final Total:", total)
