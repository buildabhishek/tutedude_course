# Task 2: Categories (Sets)

products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Printer"]

# Create categories (parallel list)
categories = ["Electronics", "Accessories", "Accessories", "Electronics", "Electronics"]

# 1. Create set
categories_set = set(categories)
print("Unique Categories:", categories_set)

# 2. Add new category
categories_set.add("Office")
print("After Adding:", categories_set)

# 3. Check existence
print("Is 'Electronics' present?", "Electronics" in categories_set)

# Extra: Count unique categories
print("Total Unique Categories:", len(categories_set))
