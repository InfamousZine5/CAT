import streamlit as st
import pandas as pd
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play
import time  # Import the time module for pausing execution

def load_inspection_status(csv_file):
    # Load inspection status from CSV file
    df = pd.read_csv(csv_file)
    return df

def main():
    st.title("Inspector's Inspection")

    # Load inspection status from CSV
    csv_file = 'merged_output.csv'  # Adjust the file path as necessary
    try:
        inspection_data = load_inspection_status(csv_file)
    except FileNotFoundError as e:
        st.error(f"Error: {e}")
        return

    # Identify unique categories, items, and attributes with null (uninspected) values
    uninspected_entries = inspection_data[inspection_data['Value'].isnull()].drop_duplicates(subset=['Category', 'Item', 'Attribute'])

    # Display the categories, items, and attributes not yet inspected
    st.subheader("Categories, Items, and Attributes Not Yet Inspected:")
    for index, row in uninspected_entries.iterrows():
        st.info(f"{row['Category']} - {row['Item']} - {row['Attribute']}")

    # Text to speech conversion and automatic playback using pydub
    processed_entries = set()  # To keep track of processed entries
    for index, row in uninspected_entries.iterrows():
        category = row['Category']
        item = row['Item']
        attribute = row['Attribute']
        entry = (category, item, attribute)
        
        # Ensure each unique entry is processed only once
        if entry not in processed_entries:
            processed_entries.add(entry)
            
            speech_text = f"Inspector, please inspect {category} {item} {attribute}"
            language = 'en'
            tts = gTTS(text=speech_text, lang=language, slow=False)

            # Save audio file
            audio_file = f"{category}_{item.replace(' ', '_').lower()}_{attribute.replace(' ', '_').lower()}.mp3"
            tts.save(audio_file)

            # Play audio using pydub
            audio = AudioSegment.from_file(audio_file, format="mp3")
            play(audio)

            # Pause between audio playback (adjust as needed)
            st.text(f"Playing: {category} - {item} - {attribute}")
            st.text("Please wait for the next prompt...")
            st.empty()  # Clear output to prepare for the next prompt
            time.sleep(2)  # Reduced pause duration to 2 seconds (adjust as needed)

if __name__ == '__main__':
    main()
