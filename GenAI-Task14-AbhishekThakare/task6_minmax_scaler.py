# This file demonstrates MinMaxScaler in sklearn

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Sample dataset
product_data = {
    "Price": [100, 200, 300, 400],
    "Quantity": [1, 2, 3, 4]
}

# Create DataFrame
_df = pd.DataFrame(product_data)

# Create scaler
scaler = MinMaxScaler()

# Scale data
scaled_data = scaler.fit_transform(_df)

print("MinMax Scaled Data:\n")
print(scaled_data)
