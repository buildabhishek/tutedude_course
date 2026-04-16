# Demonstrates: map() with lambda

prices = [100, 250, 400, 1200, 50]

prices_with_gst = list(map(lambda p: p + (0.18 * p), prices))

print("Original:", prices)
print("With GST:", prices_with_gst)
