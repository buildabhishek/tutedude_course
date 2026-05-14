# This file demonstrates preprocessing pipeline using sklearn

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

# Sample dataset
customer_data = {
    "Age": [21, 25, 30, 35],
    "Income": [20000, 30000, 40000, 50000],
    "City": ["Pune", "Mumbai", "Delhi", "Pune"]
}

# Create DataFrame
_df = pd.DataFrame(customer_data)

# Separate columns
numerical_columns = ["Age", "Income"]
categorical_columns = ["City"]

# Numerical pipeline
numerical_pipeline = Pipeline([
    ("scaler", StandardScaler())
])

# Categorical pipeline
categorical_pipeline = Pipeline([
    ("encoder", OneHotEncoder())
])

# Combine pipelines
preprocessor = ColumnTransformer([
    ("num", numerical_pipeline, numerical_columns),
    ("cat", categorical_pipeline, categorical_columns)
])

# Fit and transform
processed_data = preprocessor.fit_transform(_df)

print("Processed Data:\n")
print(processed_data)
