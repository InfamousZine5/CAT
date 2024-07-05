import streamlit as st
import os

# Simulate a simple user database
USER_DB = {
    "Inspector1": "password1",
    "Inspector2": "password2",
}

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
    st.title("Main Page")
    st.write(f"Welcome, {st.session_state['username']}!")

    categories = {
        "Model 730": "images/730.jpg",
        "Model 730EJ": "images/730ej.jpg",
        "Model 735": "images/444.jpg",
        "Model AP 655": "images/AP655.jpg"
    }
    selected_category = st.selectbox("Select a category", list(categories.keys()))

    # Display the selected category image
    image_path = categories[selected_category]
    if os.path.exists(image_path):
        st.image(image_path, caption=selected_category)
    st.write(f"You selected: {selected_category}")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()
else:
    main_page()
