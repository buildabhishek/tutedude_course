# Demonstrates: lambda function

gst = lambda price: price + (0.18 * price)

print(gst(100))

# Extra: GST + discount
final_price = lambda price: (price * 0.9) + (0.18 * price * 0.9)

print(final_price(100))
