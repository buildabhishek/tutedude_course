# Task 1

products = ["Laptop","Phone","Shoes","Watch","Book","Headphones"]
sample_product = ("Tablet",15000,"Electronics")
print(products[1])
print(products[-1])
products.append("Camera")
products.append("Bag")
print(products)
temp = list(sample_product)
temp[1] = 14000
sample_product = tuple(temp)
print(sample_product)

# Task 2

categories = ["Electronics","Electronics","Fashion","Accessories","Education","Electronics"]
categories_set = set(categories)
print(categories_set)
categories_set.add("Home")
print(categories_set)
print("Fashion" in categories_set)
print(len(categories_set))

# Task 3

price_dict = {
    "Laptop":75000,
    "Phone":40000,
    "Shoes":3000,
    "Watch":2500,
    "Book":500
}
price_dict["Headphones"] = 2000
price_dict["Book"] = 600
p = "Watch"
if p in price_dict:
    del price_dict[p]
print(price_dict)
avg = sum(price_dict.values())/len(price_dict)
print(avg)
max_p = max(price_dict,key=price_dict.get)
min_p = min(price_dict,key=price_dict.get)
print(max_p)
print(min_p)

# Task 4

catalog = [
("Laptop",75000,"Electronics"),
("Phone",40000,"Electronics"),
("Shoes",3000,"Fashion"),
("Watch",2500,"Accessories"),
("Book",600,"Education"),
("Headphones",2000,"Electronics")
]
category_products = {}
for p in catalog:
    name,price,cat = p
    if cat not in category_products:
        category_products[cat] = []
    category_products[cat].append(name)
print(category_products)
max_cat = max(category_products,key=lambda x: len(category_products[x]))
print(max_cat)
print(category_products[max_cat])
