# Demonstrates: functions with map and filter

def process_prices(prices):
    # 10% discount
    discounted = list(map(lambda p: p * 0.9, prices))

    # filter > 300
    filtered = list(filter(lambda p: p > 300, discounted))

    return prices, discounted, filtered


result = process_prices([100, 500, 900, 50, 750])

print("Original:", result[0])
print("Discounted:", result[1])
print("Filtered (>300):", result[2])
