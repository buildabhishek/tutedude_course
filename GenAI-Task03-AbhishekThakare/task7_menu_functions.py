# Demonstrates: functions + menu with loops

prices = []

def add_price(prices_list, price):
    prices_list.append(price)

def get_average(prices_list):
    if len(prices_list) == 0:
        return 0
    return sum(prices_list) / len(prices_list)

def get_max_price(prices_list):
    if len(prices_list) == 0:
        return 0
    return max(prices_list)


while True:
    print("\nMenu:")
    print("1 - Add price")
    print("2 - Show average price")
    print("3 - Show max price")
    print("q - Quit")

    choice = input("Enter choice: ")

    if choice == "1":
        val = input("Enter price: ")
        if not val.isdigit():
            print("Invalid input")
            continue
        add_price(prices, int(val))

    elif choice == "2":
        print("Average:", get_average(prices))

    elif choice == "3":
        print("Max:", get_max_price(prices))

    elif choice == "q":
        break

    else:
        print("Invalid choice")
