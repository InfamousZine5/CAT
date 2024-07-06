import streamlit as st
import pandas as pd

def load_inspection_status(csv_file):
    # Load inspection status from CSV file
    df = pd.read_csv(csv_file)
    return df

def calculate_score(value, attribute, threshold=34):
    # Calculate score based on attribute type
    if pd.isna(value):
        return None
    if attribute.lower() == 'pressure':
        try:
            pressure_value = float(value)
            score = (pressure_value / threshold) * 10
            return min(max(score, 0), 10)  # Ensure score is between 0 and 10
        except ValueError:
            return None
    elif attribute.lower() == 'condition':
        condition_scores = {'excellent': 10, 'good': 6, 'bad': 2}
        return condition_scores.get(value.lower(), None)
    elif attribute.lower() == 'emergency':
        emergency_scores = {'good': 8, 'bad': 2}  # Custom logic for emergency
        return emergency_scores.get(value.lower(), None)
    elif attribute.lower() == 'fluid_level':
        fluid_scores = {'good': 7, 'bad': 3}  # Custom logic for fluid level
        return fluid_scores.get(value.lower(), None)
    return None

def assign_precedence(category, attribute):
    # Assign precedence based on category and attribute
    if category.lower() == 'brake':
        return 1
    elif category.lower() == 'tyres' and attribute.lower() == 'condition':
        return 2
    elif category.lower() == 'tyres' and attribute.lower() == 'pressure':
        return 3
    return None

def main():
    st.title("Inspection Score and Precedence Calculator")

    # Fixed CSV file path
    csv_file = 'inspection_status.csv'

    # Load CSV file
    inspection_data = load_inspection_status(csv_file)

    # Calculate scores for each row
    inspection_data['Score'] = inspection_data.apply(
        lambda row: calculate_score(row['Value'], row['Attribute']), axis=1
    )

    # Assign precedence for each row
    inspection_data['Precedence'] = inspection_data.apply(
        lambda row: assign_precedence(row['Category'], row['Attribute']), axis=1
    )

    # Filter columns for output
    output_data = inspection_data[['Category', 'Item', 'Attribute', 'Value', 'Score', 'Precedence']]

    # Show data with scores and precedence
    st.subheader("Inspection Data with Scores and Precedence")
    st.dataframe(output_data)

    # Download button for the new CSV file with scores and precedence
    output_csv = output_data.to_csv(index=False)
    st.download_button(
        label="Download CSV with Scores and Precedence",
        data=output_csv,
        file_name='inspection_scores_precedence.csv',
        mime='text/csv'
    )

if __name__ == '__main__':
    main()
