# This program demonstrates bill calculation with error handling

prices = [120, 350, "abc", 500, -200, 800]

total = 0

for item in prices:
    try:
        if type(item) != int and type(item) != float:
            raise TypeError("Invalid data type")

        if item < 0:
            raise ValueError("Negative price not allowed")

        total = total + item
        print("Added:", item)

    except TypeError:
        print("TypeError: Invalid value ->", item)

    except ValueError as error:
        print("ValueError:", error)

print("Total Bill:", total)
