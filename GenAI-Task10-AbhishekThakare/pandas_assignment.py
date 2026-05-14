# This program demonstrates basic Pandas operations

import pandas as pd


# Task 1: Pandas Series Basics

print("===== Task 1: Pandas Series Basics =====")

marks = pd.Series([78, 85, 90, 66, 72])

print("\nSeries Values:")
print(marks)

print("\nIndex:")
print(marks.index)

print("\nData Type:")
print(marks.dtype)

print("\nFirst Element:")
print(marks.iloc[0])

print("\nLast Two Elements:")
print(marks.iloc[-2:])


# Task 2: Mathematical Operations on Series

print("\n===== Task 2: Mathematical Operations on Series =====")

print("\nAdd 5:")
print(marks + 5)

print("\nSubtract 2:")
print(marks - 2)

print("\nMultiply by 1.05:")
print(marks * 1.05)

print("\nDivide by 2:")
print(marks / 2)


# Task 3: Python Functionalities on Series

print("\n===== Task 3: Python Functionalities on Series =====")

print("\nMaximum Marks:")
print(marks.max())

print("\nMinimum Marks:")
print(marks.min())

print("\nSum of Marks:")
print(marks.sum())

print("\nMean Marks:")
print(marks.mean())

passed_students = marks.apply(lambda x: x >= 70)

print("\nPassed Students:")
print(passed_students)

print("\nNumber of Students Passed:")
print(passed_students.sum())


# Task 4: Create a DataFrame

print("\n===== Task 4: Create a DataFrame =====")

students = {
    "Name": ["Amit", "Neha", "Rahul", "Sneha", "Pooja"],
    "Marks": [78, 85, 90, 66, 72],
    "Subject": ["Math", "Math", "Science", "Science", "Math"]
}

df = pd.DataFrame(students)

print("\nFirst 3 Rows:")
print(df.head(3))

print("\nLast 2 Rows:")
print(df.tail(2))

print("\nDataFrame Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)


# Task 5: Important DataFrame Functions

print("\n===== Task 5: Important DataFrame Functions =====")

print("\nData Types:")
print(df.info())

print("\nDescribe:")
print(df.describe())

print("\nHead:")
print(df.head())

print("\nTail:")
print(df.tail())

sorted_df = df.sort_values(by="Marks", ascending=False)

print("\nSorted DataFrame:")
print(sorted_df)

reset_df = sorted_df.reset_index(drop=True)

print("\nReset Index DataFrame:")
print(reset_df)


# Task 6: Filtering & Conditional Selection

print("\n===== Task 6: Filtering & Conditional Selection =====")

print("\nStudents with Marks > 75:")
print(df[df["Marks"] > 75])

print("\nStudents belonging to Math:")
print(df[df["Subject"] == "Math"])

average_marks = df["Marks"].mean()

print("\nStudents with Marks Above Average:")
print(df[df["Marks"] > average_marks])

print("\nStudents who Failed:")
print(df[df["Marks"] < 70])


# Task 7: Grouping & Basic Analysis

print("\n===== Task 7: Grouping & Basic Analysis =====")

print("\nAverage Marks Per Subject:")
print(df.groupby("Subject")["Marks"].mean())

print("\nCount of Students Per Subject:")
print(df.groupby("Subject")["Name"].count())

print("\nMaximum Marks Per Subject:")
print(df.groupby("Subject")["Marks"].max())


# Task 8: Pandas Plotting

print("\n===== Task 8: Pandas Plotting =====")

df.plot(x="Name", y="Marks", kind="bar", title="Student Marks")

df.plot(x="Name", y="Marks", kind="line", title="Line Graph of Marks")

df["Marks"].plot(kind="hist", title="Histogram of Marks")


# Task 9: Mini Use Case - Sales Data Analysis

print("\n===== Task 9: Sales Data Analysis =====")

sales = {
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "Revenue": [1200, 1500, 900, 2000, 1800]
}

sales_df = pd.DataFrame(sales)

print("\nSales Data:")
print(sales_df)

print("\nTotal Revenue:")
print(sales_df["Revenue"].sum())

print("\nAverage Daily Revenue:")
print(sales_df["Revenue"].mean())

highest_day = sales_df.loc[sales_df["Revenue"].idxmax()]

print("\nDay with Highest Revenue:")
print(highest_day)

print("\nDays with Revenue Above Average:")
print(
    sales_df[
        sales_df["Revenue"] > sales_df["Revenue"].mean()
    ]
)

sales_df.plot(
    x="Day",
    y="Revenue",
    kind="bar",
    title="Revenue vs Day"
)
