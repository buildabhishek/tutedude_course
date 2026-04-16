# Task 3: User Menu

orders = []

while True:
    print("\nMenu:")
    print("1 - Add Order")
    print("2 - Show Orders")
    print("q - Quit")

    choice = input("Enter choice: ")

    if choice == "1":
        value = input("Enter order amount: ")

        if not value.isdigit():
            print("Invalid input!")
            continue

        orders.append(int(value))
        print("Order added!")

    elif choice == "2":
        total = 0

        print("\nOrders Summary:")
        for order in orders:

            if order >= 2000:
                discount = 0.15
            elif order >= 1500:
                discount = 0.10
            elif order >= 1000:
                discount = 0.07
            else:
                discount = 0

            final = order - (order * discount)
            total += final

            print(f"{order} -> {final}")

        print("Total:", total)

    elif choice == "q":
        print("Exiting...")
        break

    else:
        print("Invalid choice!")
        continue
