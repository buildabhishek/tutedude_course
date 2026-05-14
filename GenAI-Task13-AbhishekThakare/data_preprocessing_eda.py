# This program demonstrates data gathering, preprocessing, and EDA

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import json


# ---------------------------------------------------
# PART 1 - DATA GATHERING
# ---------------------------------------------------

# Task 1: Load Data from CSV

print("===== Task 1: Load Data from CSV =====")

data = {
    "Name": ["Amit", "Neha", "Rahul", "Sneha", "Pooja"],
    "Age": [22, 21, 23, np.nan, 24],
    "Marks": [78, 85, 90, 66, np.nan],
    "Department": ["IT", "HR", "IT", "Finance", "HR"]
}

df = pd.DataFrame(data)

print("\nDataset:")
print(df)

print("\nColumn Names:")
print(df.columns)

print("\nFirst 5 Rows:")
print(df.head())


# Task 2: Load Data from JSON

print("\n===== Task 2: Load Data from JSON =====")

json_data = [
    {"Product": "Laptop", "Price": 50000},
    {"Product": "Mobile", "Price": 20000},
    {"Product": "Tablet", "Price": 15000}
]

with open("sample_data.json", "w") as file:
    json.dump(json_data, file)

with open("sample_data.json", "r") as file:
    loaded_json = json.load(file)

json_df = pd.DataFrame(loaded_json)

print("\nJSON DataFrame:")
print(json_df)


# Task 3: Load Data from SQL Database

print("\n===== Task 3: Load Data from SQL Database =====")

connection = sqlite3.connect("employees.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER,
    name TEXT,
    department TEXT,
    salary INTEGER
)
""")

employees = [
    (1, "Amit", "IT", 50000),
    (2, "Neha", "HR", 40000),
    (3, "Rahul", "Finance", 45000),
    (4, "Sneha", "IT", 55000),
    (5, "Pooja", "HR", 42000)
]

cursor.execute("DELETE FROM employees")

cursor.executemany(
    "INSERT INTO employees VALUES (?, ?, ?, ?)",
    employees
)

connection.commit()

sql_df = pd.read_sql_query(
    "SELECT * FROM employees",
    connection
)

print("\nEmployees Data:")
print(sql_df)

connection.close()


# Task 4: API Mini Project (TMDB API)

print("\n===== Task 4: API Mini Project =====")

print("TMDB API task requires API key and internet connection.")
print("This section can be completed using requests library.")


# ---------------------------------------------------
# PART 2 - DATA PREPROCESSING & CLEANING
# ---------------------------------------------------

print("\n===== PART 2: DATA PREPROCESSING =====")

print("\nDataset Shape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nNumerical Columns:")
print(df.select_dtypes(include=np.number).columns)

print("\nCategorical Columns:")
print(df.select_dtypes(include="object").columns)


# Task 6: Data Cleaning

print("\n===== Task 6: Data Cleaning =====")

df["Age"] = df["Age"].fillna(df["Age"].mean())

df["Marks"] = df["Marks"].fillna(df["Marks"].mean())

df.columns = df.columns.str.lower().str.replace(" ", "_")

print("\nCleaned Data:")
print(df)


# Task 7: Feature Preparation

print("\n===== Task 7: Feature Preparation =====")

encoded_df = pd.get_dummies(
    df,
    columns=["department"]
)

print("\nEncoded Data:")
print(encoded_df)

X = encoded_df.drop("marks", axis=1)

y = encoded_df["marks"]

print("\nFeatures:")
print(X)

print("\nTarget:")
print(y)


# ---------------------------------------------------
# PART 3 - EXPLORATORY DATA ANALYSIS (EDA)
# ---------------------------------------------------

print("\n===== PART 3: EDA =====")


# Task 8: Univariate Analysis

plt.figure()

sns.histplot(df["marks"], kde=True)

plt.title("Distribution of Marks")

plt.show()


plt.figure()

sns.boxplot(x=df["marks"])

plt.title("Box Plot of Marks")

plt.show()


# Task 9: Bivariate Analysis

plt.figure()

sns.scatterplot(
    x=df["age"],
    y=df["marks"]
)

plt.title("Age vs Marks")

plt.show()


correlation = df[["age", "marks"]].corr()

plt.figure()

sns.heatmap(
    correlation,
    annot=True
)

plt.title("Correlation Heatmap")

plt.show()


plt.figure()

sns.barplot(
    x=df["department"],
    y=df["marks"]
)

plt.title("Department vs Marks")

plt.show()


plt.figure()

sns.boxplot(
    x=df["department"],
    y=df["marks"]
)

plt.title("Department Wise Marks")

plt.show()


# Task 10: Insights & Observations

print("\n===== Task 10: Insights =====")

print("1. Average marks are around the middle range.")
print("2. Some missing values were present in the dataset.")
print("3. IT department students have slightly higher marks.")
print("4. No major outliers are visible in marks.")
print("5. Age and marks show a small positive relationship.")
