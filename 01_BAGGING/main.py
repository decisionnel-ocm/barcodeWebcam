import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'data_list' not in st.session_state:
    st.session_state.data_list = []

if 'username' not in st.session_state:
    st.session_state.username = ""

def login(username, password):
    if username == "user" and password == "12345":
        st.session_state.username = username
        st.session_state.authenticated = True
    else:
        st.error("Incorrect username or password")

def validate_input():
    input_value = st.session_state.input_value
    if input_value:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.data_list.append((input_value, timestamp, st.session_state.username))
        st.success(f"Input {input_value} validated and stored with timestamp {timestamp} by {st.session_state.username}")
        st.session_state.input_value = ""  # Clear the input field

def main():
    if not st.session_state.authenticated:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login(username, password)
    else:
        st.title("Barcode reader")

        input_value = st.text_input("Please scan your barcode then press ENTER to continue", key='input_value', on_change=validate_input)
        
        if len(st.session_state.data_list) >= 10:
            df = pd.DataFrame(st.session_state.data_list, columns=["Value", "Timestamp", "Username"])
            st.dataframe(df)
            st.session_state.data_list = []  # Clear the list

if __name__ == "__main__":
    main()
