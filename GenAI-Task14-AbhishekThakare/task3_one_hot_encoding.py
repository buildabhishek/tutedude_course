# This file demonstrates one hot encoding using pandas

import pandas as pd

# Sample dataset
student_data = {
    "Name": ["Amit", "Rahul", "Sneha", "Priya"],
    "City": ["Pune", "Mumbai", "Pune", "Delhi"]
}

# Create DataFrame
_df = pd.DataFrame(student_data)

print("Original Data:\n")
print(_df)

# Apply one hot encoding
encoded_df = pd.get_dummies(_df, columns=["City"])

print("\nEncoded Data:\n")
print(encoded_df)
