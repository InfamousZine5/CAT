import pandas as pd

# Read inspection_data.csv and select specific columns
inspection_data = pd.read_csv('App01/Main.csv', usecols=['Category', 'Item', 'Attribute'])

# Read categorized_commands.csv and select specific columns
categorized_commands = pd.read_csv('App01/categorized_commands.csv', usecols=['Category', 'Value'])

merged_df = pd.merge(inspection_data, categorized_commands, on='Category', how='outer')

# Display the merged DataFrame (optional)
print("Merged DataFrame:")
print(merged_df)

# Output the merged DataFrame to a new CSV file (optional)
merged_df.to_csv('App01/merged_output.csv', index=False)
print("Merged DataFrame saved to 'merged_output.csv'")
