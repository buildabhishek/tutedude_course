# Demonstrates: filter() usage

prices = [100, 250, 400, 1200, 50, 2000, 850]

greater_than_500 = list(filter(lambda p: p > 500, prices))
less_equal_500 = list(filter(lambda p: p <= 500, prices))

print("Above 500:", greater_than_500)
print("500 or less:", less_equal_500)
