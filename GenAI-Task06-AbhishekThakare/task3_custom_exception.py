# This program demonstrates custom exception handling for age validation

def check_age(age):
    if age < 1 or age > 120:
        raise ValueError("Age must be between 1 and 120")

    print("Valid age entered")


try:
    user_age = int(input("Enter your age: "))

    check_age(user_age)

except ValueError as error:
    print("Error:", error)
