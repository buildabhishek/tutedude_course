# This program demonstrates different types of plots using Matplotlib

import matplotlib.pyplot as plt


# Task 1: Line Plot (Sales Trend)

months = ["Jan", "Feb", "Mar", "Apr", "May"]
sales = [1000, 1500, 1300, 1800, 2000]

plt.figure()

plt.plot(months, sales)

plt.title("Monthly Sales Trend")
plt.xlabel("Months")
plt.ylabel("Sales")

plt.show()


# Task 2: Scatter Plot

study_hours = [1, 2, 3, 4, 5, 6]
marks = [45, 50, 60, 65, 70, 85]

plt.figure()

plt.scatter(study_hours, marks)

plt.title("Study Hours vs Marks")
plt.xlabel("Study Hours")
plt.ylabel("Marks")

plt.show()


# Task 3: Bar Plot

products = ["Laptop", "Mobile", "Tablet", "Headphones"]
quantity = [10, 25, 15, 20]

plt.figure()

plt.bar(products, quantity)

plt.title("Product Quantity")
plt.xlabel("Products")
plt.ylabel("Quantity")

plt.show()


# Horizontal Bar Plot

plt.figure()

plt.barh(products, quantity)

plt.title("Horizontal Product Quantity")
plt.xlabel("Quantity")
plt.ylabel("Products")

plt.show()


# Task 4: Multiple Bar Plot

years = ["2022", "2023", "2024"]

sales_a = [100, 150, 200]
sales_b = [120, 170, 220]

x = [0, 1, 2]

width = 0.3

plt.figure()

plt.bar(x, sales_a, width=width, label="Product A")

plt.bar(
    [i + width for i in x],
    sales_b,
    width=width,
    label="Product B"
)

plt.title("Yearly Sales Comparison")
plt.xlabel("Years")
plt.ylabel("Sales")

plt.xticks(
    [i + width / 2 for i in x],
    years
)

plt.legend()

plt.show()


# Task 5: Stacked Bar Chart

boys = [40, 35, 30]
girls = [30, 25, 20]

classes = ["Class A", "Class B", "Class C"]

plt.figure()

plt.bar(classes, boys, label="Boys")

plt.bar(
    classes,
    girls,
    bottom=boys,
    label="Girls"
)

plt.title("Student Distribution")
plt.xlabel("Classes")
plt.ylabel("Number of Students")

plt.legend()

plt.show()


# Task 6: Histogram

ages = [18, 20, 21, 22, 20, 19, 18, 21, 22, 23, 24, 25]

plt.figure()

plt.hist(ages, bins=5)

plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")

plt.show()


# Task 7: Pie Chart

companies = ["Company A", "Company B", "Company C", "Company D"]

market_share = [35, 25, 20, 20]

plt.figure()

plt.pie(
    market_share,
    labels=companies,
    autopct="%1.1f%%"
)

plt.title("Market Share Distribution")

plt.show()
