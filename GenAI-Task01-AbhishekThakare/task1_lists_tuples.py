# Task 1: Product Collections (Lists & Tuples)

# 1. Create a list of product names
products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Printer"]
print("Original Products:", products)

# 2. Create a tuple (name, price, category)
sample_product = ("Laptop", 50000, "Electronics")
print("Sample Product Tuple:", sample_product)

# 3. Print 2nd and last product
print("Second product:", products[1])
print("Last product:", products[-1])

# 4. Add two new products
products.append("Tablet")
products.append("Headphones")
print("Updated Products:", products)

# Extra: Modify tuple (convert → modify → convert back)
temp_list = list(sample_product)
temp_list[1] = 55000  # change price
sample_product = tuple(temp_list)

print("Updated Tuple:", sample_product)
