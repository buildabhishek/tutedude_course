# This file demonstrates feature engineering using pandas

import pandas as pd

# Sample dataset
sales_data = {
    "Quantity": [2, 5, 3, 4],
    "Price": [100, 200, 150, 300],
    "Age": [20, 25, 30, 35]
}

# Create DataFrame
_df = pd.DataFrame(sales_data)

# Create new features
_df["Total_Value"] = _df["Quantity"] * _df["Price"]
_df["Age_Group"] = [
    "Young" if age < 25 else "Adult"
    for age in _df["Age"]
]

print("Feature Engineered Data:\n")
print(_df)
