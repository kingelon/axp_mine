import pandas as pd

# Define input and output paths
input_path = r'C:\Users\vippa\OneDrive\Documents\git_KE\axp_mine\python_scripting\data\output\dependencies.csv'
output_path = r'C:\Users\vippa\OneDrive\Documents\git_KE\axp_mine\python_scripting\data\output\output_groupedfile.csv'

# Load the CSV file
df = pd.read_csv(input_path)

# Group by 'groupid' and 'artifactid' to get distinct rows
distinct_df = df.groupby(['groupId', 'artifactId']).first().reset_index()

# Save the distinct DataFrame to a new CSV file
distinct_df.to_csv(output_path, index=False)

print(f"Distinct grouped data saved to {output_path}")
