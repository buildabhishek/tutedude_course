# Task 4: Combined Operations

# 1. Create catalog
catalog = [
    ("Laptop", 50000, "Electronics"),
    ("Mouse", 500, "Accessories"),
    ("Keyboard", 1500, "Accessories"),
    ("Monitor", 10000, "Electronics"),
    ("Printer", 7000, "Electronics")
]

print("Catalog:", catalog)

# 2. Create category → products dictionary
category_dict = {}

for name, price, category in catalog:
    if category not in category_dict:
        category_dict[category] = []
    category_dict[category].append(name)

print("Category Mapping:", category_dict)

# 3. Category with max products
max_category = max(category_dict, key=lambda x: len(category_dict[x]))

print("Category with most products:", max_category)
print("Products in that category:", category_dict[max_category])
