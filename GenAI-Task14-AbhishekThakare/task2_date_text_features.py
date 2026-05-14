# This file demonstrates date and text feature extraction

import pandas as pd

# Sample dataset
sample_data = {
    "Date": [
        "2024-01-10",
        "2024-02-15",
        "2024-03-20"
    ],
    "Text": [
        "Machine Learning",
        "Python Programming",
        "Data Science"
    ]
}

# Create DataFrame
_df = pd.DataFrame(sample_data)

# Convert Date column
_df["Date"] = pd.to_datetime(_df["Date"])

# Extract features from date
_df["Year"] = _df["Date"].dt.year
_df["Month"] = _df["Date"].dt.month
_df["Day"] = _df["Date"].dt.day

# Text feature
_df["Text_Length"] = _df["Text"].apply(len)

print("Date and Text Features:\n")
print(_df)
