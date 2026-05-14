# This program demonstrates a simple inventory system using OOP

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __add__(self, other):
        return self.price + other.price

    def display(self):
        print("Product Name:", self.name)
        print("Price:", self.price)


class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, name):
        for product in self.products:
            if product.name == name:
                self.products.remove(product)
                print(name, "removed successfully")
                return

        print("Product not found")

    def get_total_value(self):
        total = 0

        for product in self.products:
            total = total + product.price

        return total

    def show_all_products(self):
        for product in self.products:
            product.display()
            print()


class Store:
    def __init__(self, store_name):
        self.store_name = store_name
        self.inventory = Inventory()

    def add_new_product(self, product):
        self.inventory.add_product(product)

    def show_summary(self):
        print("Store Name:", self.store_name)
        print("Products in Inventory:")
        print()

        self.inventory.show_all_products()

        print("Total Inventory Value:", self.inventory.get_total_value())


product1 = Product("Laptop", 50000)
product2 = Product("Mobile", 20000)
product3 = Product("Headphones", 3000)

store = Store("Tech Store")

store.add_new_product(product1)
store.add_new_product(product2)
store.add_new_product(product3)

store.show_summary()

print()
print("Combined Price of Two Products:", product1 + product2)
