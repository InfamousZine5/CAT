import streamlit as st
import pandas as pd

def main():
    st.title("Defect Severity")
    
    # File upload and reading CSV
    uploaded_file = 'inspection_scores_precedence.csv'
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Sort the DataFrame first by score (ascending), then by precedence (ascending)
        df.sort_values(by=['Score', 'Precedence'], ascending=[True, True], inplace=True)
        
        # Create a list to store output lines
        output_lines = []
        priority_counter = 1  # Initialize priority counter
        last_score = None
        last_precedence = None
        combined_message = ""
        
        for index, row in df.iterrows():
            category = row['Category']
            item = row['Item']
            attribute = row['Attribute']
            value = row['Value']
            score = row['Score']
            precedence = row['Precedence']
            
            # Determine message based on attribute and value
            if attribute == 'pressure':
                message = f"{item.capitalize()} pressure must be increased to 34"
            elif attribute == 'fluid_level' and value == 'bad':
                message = f"Brake fluid needs to be changed"
            elif attribute in ['condition', 'emergency'] and value == 'bad':
                message = f"{item.capitalize()} needs replacement"
            else:
                continue
            
            # Check if the score and precedence are the same as the previous row
            if score == last_score and precedence == last_precedence:
                combined_message += f". {category.capitalize()} - {message}"
            else:
                if combined_message:
                    priority_line = f"{priority_counter}. {combined_message}"
                    output_lines.append(priority_line)
                    priority_counter += 1
                combined_message = f"{category.capitalize()} - {message}"
            
            last_score = score
            last_precedence = precedence
        
        # Add the final combined message
        if combined_message:
            priority_line = f"{priority_counter}. {combined_message}"
            output_lines.append(priority_line)
        
        for line in output_lines:
            st.write(line)

if __name__ == "__main__":
    main()
