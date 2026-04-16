# Demonstrates: recursive function

def factorial(n):
    if n < 0:
        return "Invalid input"
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)


print(factorial(5))
print(factorial(0))
print(factorial(-3))
