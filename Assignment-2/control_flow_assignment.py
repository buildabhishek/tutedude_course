# Task 1

try:
    order_amount = int(input("Enter order amount: "))
    if order_amount >= 2000:
        discount_rate = 0.15
    elif order_amount >= 1500:
        discount_rate = 0.10
    elif order_amount >= 1000:
        discount_rate = 0.07
    else:
        discount_rate = 0
    discount = order_amount * discount_rate
    final_amount = order_amount - discount
    print(f"Order: {order_amount} -> Discount: {discount} -> Final: {final_amount}")
except ValueError:
    print("Error: Please enter a numeric value.")

# Task 2

orders = [1200, 2500, 800, 1750, 3000]
total_revenue = 0
print("Order | Discount | Final Amount")
print("-" * 30)
for order in orders:
    if order >= 2000:
        discount = order * 0.15
    elif order >= 1500:
        discount = order * 0.10
    elif order >= 1000:
        discount = order * 0.07
    else:
        discount = 0
    final = order - discount
    print(f"{order} | {discount} | {final}")
    total_revenue += final
print("-" * 30)
print("Total revenue:", total_revenue)

# Task 3

orders_list = []
while True:
    print("\n--- Menu ---")
    print("1 - Add order amount")
    print("2 - Show all orders and totals")
    print("q - Quit")
    choice = input("Enter choice: ").lower()
    if choice == "1":
        try:
            amount = int(input("Enter amount: "))
            orders_list.append(amount)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
    elif choice == "2":
        running_total = 0
        print("\nOrder Summary:")
        for order in orders_list:
            if order >= 2000:
                discount = order * 0.15
            elif order >= 1500:
                discount = order * 0.10
            elif order >= 1000:
                discount = order * 0.07
            else:
                discount = 0
            final = order - discount
            print(f"Original: {order}, Final: {final}")
            running_total += final
        print(f"Grand Total: {running_total}")
    elif choice == "q":
        print("Exiting...")
        break
    else:
        print("Invalid choice, try again.")
        continue

# Task 4

sales = [200, 150, 0, 400, 50, -1, 300]
total_sales = 0
for day in sales:
    if day == -1:
        print("Corrupted data found (-1). Stopping process.")
        break
    if day == 0:
        continue
    if day > 0:
        total_sales += day
        print(f"Added {day}. Running total: {total_sales}")
print("Final total sales:", total_sales)
