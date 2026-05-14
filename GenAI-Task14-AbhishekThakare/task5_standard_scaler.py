# This file demonstrates StandardScaler in sklearn

import pandas as pd
from sklearn.preprocessing import StandardScaler

# Sample dataset
marks_data = {
    "Math": [50, 60, 70, 80],
    "Science": [55, 65, 75, 85]
}

# Create DataFrame
_df = pd.DataFrame(marks_data)

# Create scaler
scaler = StandardScaler()

# Scale data
scaled_data = scaler.fit_transform(_df)

print("Standard Scaled Data:\n")
print(scaled_data)
