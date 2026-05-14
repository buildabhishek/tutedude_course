# This program demonstrates polymorphism using method overriding

class Product:
    def get_info(self):
        print("Product information")


class Laptop(Product):
    def get_info(self):
        print("This is a Laptop")


class Mobile(Product):
    def get_info(self):
        print("This is a Mobile")


products = [Laptop(), Mobile()]

for item in products:
    item.get_info()
