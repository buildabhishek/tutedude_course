# Task 2: Process Multiple Orders

orders = [1200, 2500, 800, 1750, 3000]

total_revenue = 0
discount_count = 0

print("Order Summary:")
print("---------------------------")

for order in orders:

    if order >= 2000:
        discount = 0.15
    elif order >= 1500:
        discount = 0.10
    elif order >= 1000:
        discount = 0.07
    else:
        discount = 0

    discount_amount = order * discount
    final_amount = order - discount_amount

    if discount > 0:
        discount_count += 1

    total_revenue += final_amount

    print(f"{order} -> {discount_amount} -> {final_amount}")

print("---------------------------")
print("Total Revenue:", total_revenue)
print("Orders with Discount:", discount_count)
