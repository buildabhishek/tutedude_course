# Task 3: Product Pricing (Dictionaries)

# 1. Create dictionary
price_dict = {
    "Laptop": 50000,
    "Mouse": 500,
    "Keyboard": 1500,
    "Monitor": 10000,
    "Printer": 7000
}

print("Initial Prices:", price_dict)

# 2. Add new product
price_dict["Tablet"] = 20000

# Update price
price_dict["Mouse"] = 600

# Remove product safely
product_to_remove = "Camera"
if product_to_remove in price_dict:
    del price_dict[product_to_remove]
else:
    print(f"{product_to_remove} not found")

print("Updated Prices:", price_dict)

# 3. Average price
total = sum(price_dict.values())
avg = total / len(price_dict)
print("Average Price:", avg)

# Extra: Max & Min
max_product = max(price_dict, key=price_dict.get)
min_product = min(price_dict, key=price_dict.get)

print("Most Expensive:", max_product)
print("Least Expensive:", min_product)
