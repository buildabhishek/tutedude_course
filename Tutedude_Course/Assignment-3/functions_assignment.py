# Task 1: Basic Function

def apply_discount(price, discount_percent=5):
    final_price = price - (price * discount_percent / 100)
    return final_price
print("--- Task 1 ---")
print(apply_discount(1000, 10))
print(apply_discount(500))

# Task 2: Recursive Function

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)
print("\n--- Task 2 ---")
print(factorial(5))
print(factorial(0))
print(factorial(3))

# Task 3: Lambda Function

gst_calculator = lambda price: price + (price * 0.18)
print("\n--- Task 3 ---")
print(gst_calculator(100))

# Task 4: Map Function

prices = [100, 150, 300, 500, 50]
final_prices = list(map(lambda x: x - (x * 0.05), prices))
print("\n--- Task 4 ---")
print("Original:", prices)
print("Discounted:", final_prices)

# Task 5: Filter Function

product_prices = [100, 250, 400, 1200, 50, 2000, 350]
expensive = list(filter(lambda x: x > 500, product_prices))
budget = list(filter(lambda x: x <= 500, product_prices))
print("\n--- Task 5 ---")
print("Expensive:", expensive)
print("Budget:", budget)

# Task 6: Combined Utility

def process_prices(price_list):
    discounted = list(map(lambda x: x * 0.85, price_list))
    filtered = list(filter(lambda x: x > 100, discounted))
    return filtered
print("\n--- Task 6 ---")
test_prices = [100, 500, 200, 50, 150]
print(process_prices(test_prices))

# Task 7: Mini Project

all_prices = []
def add_price(p):
    all_prices.append(p)
def get_average():
    if not all_prices: return 0
    return sum(all_prices) / len(all_prices)
def get_highest():
    if not all_prices: return 0
    return max(all_prices)
print("\n--- Task 7 (Menu) ---")
while True:
    print("\n1. Add Price, 2. Average, 3. Highest, 4. Exit")
    choice = input("Select option: ")
    if choice == "1":
        val = float(input("Enter price: "))
        add_price(val)
    elif choice == "2":
        print("Average:", get_average())
    elif choice == "3":
        print("Highest:", get_highest())
    elif choice == "4":
        print("Exiting...")
        break
    else:
        print("Invalid choice.")
