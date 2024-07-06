import csv
import os
import streamlit as st
import datetime

# Function to initialize or update CSV file with headers
def initialize_csv(csv_file):
    csv_columns = ['Category', 'Item', 'Attribute', 'Value']
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()

# Example function to save inspection data to CSV
def save_inspection_data_to_csv(inspection_data):
    csv_file = 'inspection_data.csv'
    initialize_csv(csv_file)

    try:
        with open(csv_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Category', 'Item', 'Attribute', 'Value'])
            for category, items in inspection_data.items():
                for item, attributes in items.items():
                    for attribute, value in attributes.items():
                        writer.writerow({'Category': category, 'Item': item, 'Attribute': attribute, 'Value': value})
        st.write("Inspection data saved to inspection_data.csv")
    except IOError:
        st.error("I/O error occurred while saving inspection data.")

# Example usage within Streamlit
def main():
    st.title("Streamlit App for Inspection")

    # Simulated inspection data
    inspection_data = {
        'tyres': {
            'leftfront': {'pressure': '', 'condition': ''},
            'rightfront': {'pressure': '', 'condition': ''},
            'leftback': {'pressure': '', 'condition': ''},
            'rightback': {'pressure': '', 'condition': ''},
        },
        'battery': {
            'battery': {'condition': ''}
        },
        'engine': {
            'engine': {'condition': ''}
        },
        'brakes': {
            'front': {'condition': ''},
            'back': {'condition': '', 'fluid': ''}
        },
        'exterior': {
            'exterior': {'condition': ''}
        }
    }

    # Start inspection and save data example
    if st.button("Start Inspection"):
        for category, items in inspection_data.items():
            for item, attributes in items.items():
                for attribute in attributes.keys():
                    value = st.text_input(f"{category}/{item}/{attribute}")
                    inspection_data[category][item][attribute] = value
        
        save_inspection_data_to_csv(inspection_data)

# Run the main function
if __name__ == "__main__":
    main()
