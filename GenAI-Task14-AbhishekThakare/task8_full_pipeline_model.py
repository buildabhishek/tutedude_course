# This file demonstrates full sklearn pipeline with model

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression

# Sample dataset
student_data = {
    "Hours": [1, 2, 3, 4, 5, 6],
    "Attendance": [60, 65, 70, 75, 80, 90],
    "Department": [
        "IT",
        "IT",
        "HR",
        "HR",
        "Finance",
        "Finance"
    ],
    "Result": [0, 0, 0, 1, 1, 1]
}

# Create DataFrame
_df = pd.DataFrame(student_data)

# Features and target
X = _df.drop("Result", axis=1)
y = _df["Result"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Column names
numerical_columns = ["Hours", "Attendance"]
categorical_columns = ["Department"]

# Preprocessing
preprocessor = ColumnTransformer([
    (
        "num",
        StandardScaler(),
        numerical_columns
    ),
    (
        "cat",
        OneHotEncoder(),
        categorical_columns
    )
])

# Full pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression())
])

# Train model
pipeline.fit(X_train, y_train)

# Test accuracy
accuracy = pipeline.score(X_test, y_test)

print("Model Accuracy:")
print(accuracy)
