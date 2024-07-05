import streamlit as st
import datetime
import geocoder
import cv2
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, ClientSettings
import av
import os

# Simulate a simple user database
USER_DB = {
    "1": "x",
    "Inspector2": "password2",
}

class QRCodeProcessor(VideoProcessorBase):
    def __init__(self):
        self.qr_code = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        if bbox is not None:
            if data:
                self.qr_code = data
                st.session_state['inspector_id'] = data
                st.session_state['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                g = geocoder.ip('me')
                st.session_state['location'] = g.latlng
                st.experimental_rerun()

        return av.VideoFrame.from_ndarray(img, format="bgr24")

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

def scan_qr_code():
    st.title("Inspector ID Input")
    st.write("Please enter your Inspector ID.")
    inspector_id = st.text_input("Inspector ID")

    if st.button("Submit"):
        if inspector_id:
            st.session_state['inspector_id'] = inspector_id
            st.session_state['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            g = geocoder.ip('me')
            st.session_state['location'] = g.latlng
            st.experimental_rerun()

def main_page():
    st.title("Main Page")
    st.write(f"Welcome, {st.session_state['username']}!")

    # Logout button
    if st.button("Logout", key="logout_main"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

    # Display the obtained information
    st.markdown(f"**Inspector ID:** {st.session_state.get('inspector_id', '')}")
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
        inspection_page()

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

if __name__ == "__main__":
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

    if not st.session_state['logged_in']:
        login()
    elif st.session_state['inspector_id'] is None:
        scan_qr_code()
    elif st.session_state['show_inspection_page']:
        inspection_page()
    else:
        main_page()
