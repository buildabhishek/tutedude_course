# This program demonstrates inheritance and method overriding

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_info(self):
        print("Product Name:", self.name)
        print("Price:", self.price)


class ElectronicProduct(Product):
    def __init__(self, name, price, warranty_years):
        super().__init__(name, price)
        self.warranty_years = warranty_years

    def get_info(self):
        print("Product Name:", self.name)
        print("Price:", self.price)
        print("Warranty:", self.warranty_years, "years")


item = ElectronicProduct("Smart TV", 45000, 2)

item.get_info()
