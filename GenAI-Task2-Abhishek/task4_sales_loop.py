# Task 4: Loop Control with Conditions

sales = [200, 150, 0, 400, 50, -1, 300]

total_sales = 0

for day in sales:

    if day == -1:
        print("Corrupted data found. Stopping...")
        break

    if day == 0:
        print("No sales today. Skipping...")
        continue

    total_sales += day
    print("Added:", day, "| Running Total:", total_sales)

print("Final Total Sales:", total_sales)
