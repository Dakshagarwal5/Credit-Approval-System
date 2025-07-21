# Let's analyze the customer data to understand the data structure and statistics
import pandas as pd
import numpy as np

# Load customer data
customer_data = pd.read_excel('customer_data.xlsx')
print("Customer Data Overview:")
print("=" * 50)
print(f"Total customers: {len(customer_data)}")
print(f"Columns: {list(customer_data.columns)}")
print("\nFirst 5 rows:")
print(customer_data.head())
print("\nData types:")
print(customer_data.dtypes)
print("\nBasic statistics:")
print(customer_data.describe())