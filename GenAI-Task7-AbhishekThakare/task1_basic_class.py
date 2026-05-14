# This program demonstrates basic class and object creation

class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def get_info(self):
        print("Product Name:", self.name)
        print("Price:", self.price)
        print("Category:", self.category)

    def apply_discount(self, percent):
        discount = (self.price * percent) / 100
        final_price = self.price - discount
        return final_price


product1 = Product("Laptop", 50000, "Electronics")
product2 = Product("Phone", 20000, "Mobiles")

product1.get_info()
print()

product2.get_info()
print()

print("Discounted Price:", product1.apply_discount(10))
