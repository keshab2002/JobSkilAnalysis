import pandas as pd

# Load the dataset with 1 million data points
df = pd.read_csv('AI\skillsSplitData.csv')

# Sample 500 random data points from the dataset
sampled_df = df.sample(n=3000, random_state=42)

# Save the sampled data to a new CSV file
sampled_df.to_csv('skillsSplitData1.csv', index=False)

print("500 data points sampled and saved as 'skillsSplitData1.csv'")
