import csv

# Define the keywords for categorization
keywords = ["excellent", "good", "ok", "bad"]

# Function to categorize a line of text based on keywords and write to CSV
def categorize_and_write_to_csv(input_file, output_file):
    # Open input and output files
    with open(input_file, 'r') as infile, open(output_file, 'a', newline='') as csvfile:  # Use 'a' for append mode
        # Initialize CSV writer with extended fieldnames
        fieldnames = ['Category', 'Item', 'Attribute', 'Value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the output file is empty; write header if so
        csvfile.seek(0, 2)  # Move to end of file to check if empty
        if csvfile.tell() == 0:  # Check if file is empty
            writer.writeheader()

        # Read each line from input file
        for line in infile:
            words = line.lower().split()
            # Iterate through words in the line
            for i in range(len(words)):
                word = words[i]
                # Check if word is one of the keywords
                if word in keywords:
                    if i > 0:
                        category = words[i - 1]  # Word before the keyword
                        item = ""  # Placeholder for item (customize as needed)
                        attribute = ""  # Placeholder for attribute (customize as needed)
                        value = word  # The keyword itself
                        # Write to CSV
                        writer.writerow({'Category': category, 'Item': item, 'Attribute': attribute, 'Value': value})

    print(f"Content categorized and appended to '{output_file}'.")

# Input and output file paths
input_file = 'App01/voice_commands.txt'
output_file = 'App01/categorized_commands.csv'

# Call function to categorize and append to CSV
categorize_and_write_to_csv(input_file, output_file)
