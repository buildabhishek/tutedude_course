from pathlib import Path
import zipfile
from textwrap import dedent

base = Path("/mnt/data/GenAI-Task10-Abhishek")
base.mkdir(exist_ok=True)

main_code = dedent("""
import pandas as pd

print("="*60)
print("TASK 1: Pandas Series Basics")
print("="*60)

marks = pd.Series([78, 85, 90, 66, 72])

print("Series Values:")
print(marks)

print("\\nIndex:")
print(marks.index)

print("\\nData Type:")
print(marks.dtype)

print("\\nFirst Element:")
print(marks.iloc[0])

print("\\nLast Two Elements:")
print(marks.iloc[-2:])

print("\\n" + "="*60)
print("TASK 2: Mathematical Operations on Series")
print("="*60)

print("\\nAdd 5:")
print(marks + 5)

print("\\nSubtract 2:")
print(marks - 2)

print("\\nMultiply by 1.05:")
print(marks * 1.05)

print("\\nDivide by 2:")
print(marks / 2)

print("\\n" + "="*60)
print("TASK 3: Python Functionalities on Series")
print("="*60)

print("\\nMaximum Marks:", marks.max())
print("Minimum Marks:", marks.min())
print("Sum of Marks:", marks.sum())
print("Mean of Marks:", marks.mean())

passed = marks.apply(lambda x: x >= 70)

print("\\nPass Status:")
print(passed)

print("\\nNumber of Students Passed:", passed.sum())

print("\\n" + "="*60)
print("TASK 4: Create a DataFrame")
print("="*60)

students = {
    "Name": ["Amit", "Neha", "Rahul", "Sneha", "Pooja"],
    "Marks": [78, 85, 90, 66, 72],
    "Subject": ["Math", "Math", "Science", "Science", "Math"]
}

df = pd.DataFrame(students)

print("\\nFirst 3 Rows:")
print(df.head(3))

print("\\nLast 2 Rows:")
print(df.tail(2))

print("\\nShape of DataFrame:")
print(df.shape)

print("\\nColumn Names:")
print(df.columns.tolist())

print("\\n" + "="*60)
print("TASK 5: Important DataFrame Functions")
print("="*60)

print("\\nData Types:")
print(df.dtypes)

print("\\nDescribe:")
print(df.describe())

print("\\nHead:")
print(df.head())

print("\\nTail:")
print(df.tail())

sorted_df = df.sort_values(by="Marks", ascending=False)

print("\\nSorted by Marks (Descending):")
print(sorted_df)

reset_df = sorted_df.reset_index(drop=True)

print("\\nReset Index:")
print(reset_df)

print("\\n" + "="*60)
print("TASK 6: Filtering & Conditional Selection")
print("="*60)

print("\\nStudents with Marks > 75:")
print(df[df["Marks"] > 75])

print("\\nStudents Belonging to Math:")
print(df[df["Subject"] == "Math"])

average_marks = df["Marks"].mean()

print("\\nStudents Scoring Above Average:")
print(df[df["Marks"] > average_marks])

print("\\nStudents Who Failed (Marks < 70):")
print(df[df["Marks"] < 70])

print("\\n" + "="*60)
print("TASK 7: Grouping & Basic Analysis")
print("="*60)

print("\\nAverage Marks Per Subject:")
print(df.groupby("Subject")["Marks"].mean())

print("\\nCount of Students Per Subject:")
print(df.groupby("Subject")["Name"].count())

print("\\nMaximum Marks Per Subject:")
print(df.groupby("Subject")["Marks"].max())

print("\\n" + "="*60)
print("TASK 8: Pandas Plotting")
print("="*60)

import matplotlib.pyplot as plt

df.plot(x="Name", y="Marks", kind="bar", title="Student Marks")
plt.show()

df.plot(x="Name", y="Marks", kind="line", title="Marks Line Graph")
plt.show()

df["Marks"].plot(kind="hist", title="Histogram of Marks")
plt.show()

print("\\n" + "="*60)
print("TASK 9: Mini Use Case - Sales Data Analysis")
print("="*60)

sales = {
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "Revenue": [1200, 1500, 900, 2000, 1800]
}

sales_df = pd.DataFrame(sales)

print("\\nSales Data:")
print(sales_df)

print("\\nTotal Revenue:")
print(sales_df["Revenue"].sum())

print("\\nAverage Daily Revenue:")
print(sales_df["Revenue"].mean())

highest_day = sales_df.loc[sales_df["Revenue"].idxmax()]

print("\\nDay with Highest Revenue:")
print(highest_day)

average_revenue = sales_df["Revenue"].mean()

print("\\nDays Where Revenue > Average:")
print(sales_df[sales_df["Revenue"] > average_revenue])

sales_df.plot(x="Day", y="Revenue", kind="bar", title="Revenue vs Day")
plt.show()
""")

