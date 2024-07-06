import datetime
import geocoder
import cv2
import subprocess
import os
import speech_recognition as sr
import pyttsx3
import csv
import pandas as pd
import streamlit as st
import pyaudio

# Simulate a simple user database
USER_DB = {
    "abc": "x",
    "Inspector2": "password2",
}

class QRCodeProcessor:
    def __init__(self):
        self.qr_code = None

    def scan_qr_code(self):
        st.title("Please enter the Serial Number.")
        inspector_id = st.text_input("Serial Number")

        if st.button("Submit"):
            if inspector_id:
                st.session_state['inspector_id'] = inspector_id
                st.session_state['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                g = geocoder.ip('me')
                st.session_state['location'] = g.latlng
                st.experimental_rerun()

def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_DB and USER_DB[username] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def main_page():
    st.title("Inspection Details:")
    st.write(f"Welcome, {st.session_state['username']}!")

    # Logout button
    if st.button("Logout", key="logout_main"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

    # Display the obtained information
    st.markdown(f"**Serial Number:** {st.session_state.get('inspector_id', '')}")
    st.markdown(f"**Date and Time:** {st.session_state.get('timestamp', '')}")
    st.markdown(f"**Location:** {st.session_state.get('location', '')}")

    # Display images based on inspector ID
    inspector_id = st.session_state.get('inspector_id')
    if inspector_id:
        if inspector_id == "Model 730":
            st.image("images/730.jpg", caption="Model 730")
        elif inspector_id == "Model 730EJ":
            st.image("images/730ej.jpg", caption="Model 730EJ")
        else:
            st.write("No image available for this inspector ID.")

    if st.button("Start Inspection", key="start_inspection"):
        st.session_state['show_inspection_page'] = True

def inspection_page():
    st.title("Inspection Page")
    st.write("This is the Inspection Page. You can start your inspection here.")

    # Logout button
    if st.button("Logout", key="logout_inspection"):
        st.session_state['logged_in'] = False
        st.session_state['show_inspection_page'] = False
        st.experimental_rerun()

    # Define the pages and buttons with named categories
    pages = [
        ["Tyres", "Engine", "Battery", "Brakes", "External", "Feedback"]
    ]
    
    # Determine which page to display
    current_page = st.session_state.get('current_page', 0)
    current_buttons = pages[current_page]

    # Display the buttons for the current page
    for i, category in enumerate(current_buttons):
        if i % 2 == 0:
            col1, col2 = st.columns(2)
        with col1 if i % 2 == 0 else col2:
            if st.button(category, key=f"button_{i}"):
                # Perform action based on button click (if needed)
                st.write(f"You clicked {category}")

    # Button to switch between pages
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous Page"):
            st.session_state['current_page'] = max(0, current_page - 1)
    with col2:
        if st.button("Next Page"):
            st.session_state['current_page'] = min(len(pages) - 1, current_page + 1)

    # Start Inspection Script button
    if st.session_state['show_inspection_page']:
        start_inspection_script()

def start_inspection_script():
    st.title("Start Inspection")
    st.write("Click the button below to start the inspection.")

    if st.button("Run Inspection"):
        st.write("Starting the inspection...")
        process = subprocess.Popen(['python3', 'inp.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        if stderr:
            st.error(f"Error running script: {stderr.decode()}")
        else:
            st.write("Script executed successfully.")
            st.code(stdout.decode())

def record_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        st.write("Listening...")
        audio = r.listen(source)
        try:
            st.write("Recognizing...")
            text = r.recognize_google(audio)
            
            # Write to voice_commands.txt
            with open('App01/voice_commands.txt', 'a') as file:
                file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {text}\n")
            
            return text
        except sr.RequestError as e:
            st.write(f"Could not request results; {e}")
        except sr.UnknownValueError:
            st.write("Unknown error occurred")
        return ""

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def parse_command(command):
    words = command.lower().split()
    if len(words) < 3:
        return None
    
    position = words[0] + ' ' + words[1]
    keyword = words[2]

    value_map = {
        'excellent': 2,
        'good': 1,
        'bad': 0
    }

    if keyword in value_map:
        return (position, value_map[keyword])
    else:
        return None

def save_inspection_data_to_csv(inspection_data):
    csv_columns = ['Category', 'Item', 'Attribute', 'Value']
    csv_file = "App01/inspection_data.csv"

    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)

        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for category, items in inspection_data.items():
                for item, attributes in items.items():
                    for attribute, value in attributes.items():
                        writer.writerow({'Category': category, 'Item': item, 'Attribute': attribute, 'Value': value})
        st.write("Inspection data saved to inspection_data.csv")
        
        # Call categorize_and_write_to_csv to append to categorized_commands.csv
        input_file = 'App01/voice_commands.txt'
        output_file = 'App01/categorized_commands.csv'
        categorize_and_write_to_csv(input_file, output_file)
        
        # After text_csv.py completes, read Main.csv and categorized_commands.csv, merge, and save to merged_output.csv
        generate_merged_output()
        
    except IOError as e:
        st.error(f"I/O error occurred: {str(e)}")

def generate_merged_output():
    try:
        csv_file = "App01/categorized_commands.csv"
        
        # Check if the file exists
        if not os.path.exists(csv_file):
            st.error(f"Error generating merged output: {csv_file} does not exist.")
            return
        
        # Read the CSV file
        categorized_commands = pd.read_csv(csv_file)
        
        # Check if there are columns to parse
        if categorized_commands.empty or not {'Category', 'Value'}.issubset(categorized_commands.columns):
            st.error(f"Error generating merged output: No valid columns found in {csv_file}.")
            return
        
        # Read inspection_data.csv and select specific columns
        inspection_data = pd.read_csv('App01/inspection_data.csv', usecols=['Category', 'Item', 'Attribute'])

        # Merge DataFrames on 'Category'
        merged_df = pd.merge(inspection_data, categorized_commands[['Category', 'Value']], on='Category', how='outer')

        # Display the merged DataFrame
        st.write("Merged DataFrame:")
        st.write(merged_df)

        # Output the merged DataFrame to a new CSV file
        merged_df.to_csv('App01/merged_output.csv', index=False)
        st.write("Merged DataFrame saved to 'merged_output.csv'")
        
    except Exception as e:
        st.error(f"Error generating merged output: {str(e)}")

def categorize_and_write_to_csv(input_file, output_file):
    # Define the keywords for categorization
    keywords = ["excellent", "good", "ok", "bad"]

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

    st.write(f"Content categorized and appended to '{output_file}'.")

def main():
    st.title("Voice-Enabled Vehicle Inspection")

    if 'inspection_data' not in st.session_state:
        st.session_state.inspection_data = {
            'tyres': {
                'leftFront': {'pressure': '', 'condition': ''},
                'rightFront': {'pressure': '', 'condition': ''},
                'leftRear': {'pressure': '', 'condition': ''},
                'rightRear': {'pressure': '', 'condition': ''},
            },
            'battery': {},
            'exterior': {},
            'brakes': {},
            'engine': {},
            'voice_of_customer': {},
        }

    # Start Inspection Button
    if st.button("Start Inspection"):
        st.session_state['listening'] = True
        st.write("Listening for voice commands...")

    # End Inspection Button
    if st.button("End Inspection"):
        st.session_state['listening'] = False
        save_inspection_data_to_csv(st.session_state.inspection_data)
        st.write("Stopped listening and saved inspection data.")
    
    # Display Inspection Data
    st.write("Current Inspection Data:")
    st.write(st.session_state.inspection_data)

    # Voice Command Recording
    if st.session_state.get('listening', False):
        command = record_text()
        if command:
            st.write(f"Recorded Command: {command}")
            speak_text(f"Recorded: {command}")
            parsed_command = parse_command(command)
            if parsed_command:
                st.write(f"Parsed Command: {parsed_command}")
                position, value = parsed_command
                response = f"Command '{command}' received and parsed."
                st.write(response)
                
                category, item = position.split()
                if category in st.session_state.inspection_data:
                    if item not in st.session_state.inspection_data[category]:
                        st.session_state.inspection_data[category][item] = {'condition': value}
                    else:
                        st.session_state.inspection_data[category][item]['condition'] = value
            else:
                st.write("Invalid command format or keyword not recognized. Please try again.")
        else:
            st.write("No command recorded. Please speak clearly.")
    else:
        st.write("Start Inspection to enable voice command recording.")

    # Integrate this with your existing inspection page logic
    if st.session_state['show_inspection_page']:
        inspection_page()

if __name__ == '__main__':
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'inspector_id' not in st.session_state:
        st.session_state['inspector_id'] = None
    if 'timestamp' not in st.session_state:
        st.session_state['timestamp'] = None
    if 'location' not in st.session_state:
        st.session_state['location'] = None
    if 'show_inspection_page' not in st.session_state:
        st.session_state['show_inspection_page'] = False
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 0
    if 'listening' not in st.session_state:
        st.session_state['listening'] = False

    if not st.session_state['logged_in']:
        login()
    elif st.session_state['inspector_id'] is None:
        qr_processor = QRCodeProcessor()
        qr_processor.scan_qr_code()
    elif st.session_state['show_inspection_page']:
        main()
    else:
        main_page()
