import streamlit as st
import pandas as pd
from gtts import gTTS
import os
import time

def load_inspection_status(csv_file):
    # Load inspection status from CSV file
    df = pd.read_csv(csv_file)
    return df

def main():
    st.title("Inspector's Tire Inspection")

    # Load inspection status from CSV
    csv_file = 'inspection_status.csv'  # Adjust the file path as necessary
    try:
        inspection_data = load_inspection_status(csv_file)
    except FileNotFoundError as e:
        st.error(f"Error: {e}")
        return

    # Categories not yet inspected
    not_inspected = inspection_data[inspection_data['Inspected'] == 'No']['Category'].tolist()

    # Display the categories not yet inspected in boxes
    st.subheader("Categories Not Yet Inspected:")
    for category in not_inspected:
        st.info(category)

    # Text to speech conversion and automatic playback
    for category in not_inspected:
        speech_text = f"Inspector, please inspect {category}"
        language = 'en'
        tts = gTTS(text=speech_text, lang=language, slow=False)

        # Save audio file and play with pauses
        tts.save("temp_audio.mp3")
        st.audio("temp_audio.mp3", format='audio/mp3', start_time=0)
        time.sleep(5)  # Adjust pause duration (in seconds) as needed

if __name__ == '__main__':
    main()
