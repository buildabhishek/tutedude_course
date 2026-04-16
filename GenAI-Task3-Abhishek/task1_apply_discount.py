# Demonstrates: user-defined function with default argument

def apply_discount(price, discount_percent=5):
    if discount_percent > 60:
        discount_percent = 60

    discount_amount = price * (discount_percent / 100)
    return price - discount_amount


print(apply_discount(1000, 10))
print(apply_discount(500))  # default discount
