# Demonstrates: importing modules and package

import math_utils
from math_utils import square

import string_utils

from shop_package.discount import apply_discount
from shop_package.billing import calculate_total

# math_utils
print(math_utils.add(10, 5))
print(math_utils.subtract(10, 5))
print(square(4))

# string_utils
print(string_utils.capitalize_words("hello world"))
print(string_utils.reverse_string("python"))
print(string_utils.word_count("this is a test"))

# package usage
print(apply_discount(1000, 10))
print(calculate_total([100, 200, 300]))
