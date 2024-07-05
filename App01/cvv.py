import csv

# Example data
inspection_data = [
    {"Category": "Tyres", "Item": "leftFront", "Attribute": "pressure", "Value": ""},
    {"Category": "Tyres", "Item": "leftFront", "Attribute": "condition", "Value": ""},
    {"Category": "Tyres", "Item": "rightFront", "Attribute": "pressure", "Value": ""},
    {"Category": "Tyres", "Item": "rightFront", "Attribute": "condition", "Value": ""},
    {"Category": "Battery", "Item": "battery", "Attribute": "condition", "Value": ""},
    {"Category": "Engine", "Item": "engine", "Attribute": "condition", "Value": ""},
]

# Define CSV file path
csv_file = "inspection_data.csv"

# Function to write inspection data to CSV
def write_inspection_data_to_csv(data, csv_file):
    csv_columns = ['Category', 'Item', 'Attribute', 'Value']

    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for item in data:
                writer.writerow(item)
        print(f"Data successfully written to {csv_file}")
    except IOError:
        print(f"I/O error occurred while writing to {csv_file}")

# Call the function with the example data
write_inspection_data_to_csv(inspection_data, csv_file)
