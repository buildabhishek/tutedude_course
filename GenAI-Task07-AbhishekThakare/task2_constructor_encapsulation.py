# This program demonstrates constructor and encapsulation

class Product:
    def __init__(self, name, price):
        self.name = name
        self.__price = price

    def get_price(self):
        return self.__price

    def set_price(self, new_price):
        if new_price > 0:
            self.__price = new_price
            print("Price updated successfully")
        else:
            print("Invalid price")

    def display(self):
        print("Product:", self.name)
        print("Price:", self.__price)


product = Product("Tablet", 15000)

product.display()

product.set_price(18000)

print("Updated Price:", product.get_price())
