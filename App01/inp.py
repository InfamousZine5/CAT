import streamlit as st
import datetime
import geocoder
import cv2
import speech_recognition as sr
import pyttsx3
import csv
import os

# Function to record voice command and write to voice_commands.txt
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
            with open('voice_commands.txt', 'a') as file:
                file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {text}\n")
            
            return text
        except sr.RequestError as e:
            st.write(f"Could not request results; {e}")
        except sr.UnknownValueError:
            st.write("Unknown error occurred")
        return ""

# Function to handle voice output
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to parse the voice command and categorize
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

# Function to save inspection data to CSV
def save_inspection_data_to_csv(inspection_data):
    csv_columns = ['Category', 'Item', 'Attribute', 'Value']
    csv_file = "inspection_data.csv"

    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for category, items in inspection_data.items():
                for item, attributes in items.items():
                    for attribute, value in attributes.items():
                        writer.writerow({'Category': category, 'Item': item, 'Attribute': attribute, 'Value': value})
        st.write("Inspection data saved to inspection_data.csv")
    except IOError:
        st.write("I/O error")

# Main Streamlit application
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
        st.session_state.listening = True
        st.write("Listening for voice commands...")

    # End Inspection Button
    if st.button("End Inspection"):
        st.session_state.listening = False
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

# Check if voice_commands.txt exists; if not, create it
if not os.path.exists('voice_commands.txt'):
    with open('voice_commands.txt', 'w'): pass

if __name__ == '__main__':
    main()
