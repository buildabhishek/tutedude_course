# This file demonstrates ColumnTransformer in sklearn

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Sample dataset
employee_data = {
    "Age": [22, 25, 30, 28],
    "Salary": [25000, 40000, 50000, 45000],
    "Department": ["HR", "IT", "Finance", "IT"]
}

# Create DataFrame
_df = pd.DataFrame(employee_data)

# Separate columns
numerical_columns = ["Age", "Salary"]
categorical_columns = ["Department"]

# Create ColumnTransformer
transformer = ColumnTransformer(
    transformers=[
        (
            "category",
            OneHotEncoder(),
            categorical_columns
        )
    ],
    remainder="passthrough"
)

# Transform data
transformed_data = transformer.fit_transform(_df)

print("Transformed Data:\n")
print(transformed_data)
