import pandas as pd
import numpy as np

# Load the CSV
df = pd.read_csv('testing_data/cube_data_1000000.csv')

# Keep only rows 0 to 1,000,000 (i.e., first 1,000,001 rows)
df = df.iloc[1:1000001]

# Compute total points and label sum
total_points = len(df)
label_sum = df['Label'].sum()

# Estimate value of pi
pi_estimate = (2 * total_points / label_sum) / np.sqrt(3)

# Output the results
print(f"Sum of 'Label' column: {label_sum}")
print(f"Total usable points: {total_points}")
print(f"Estimated value of π: {pi_estimate}")
