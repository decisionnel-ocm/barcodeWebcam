import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.start_time = None

if 'data_list' not in st.session_state:
    st.session_state.data_list = []

if 'username' not in st.session_state:
    st.session_state.username = ""

def login(username, password):
    if username == "fmoskal" and password == "123moskal456":
        st.session_state.username = username
        st.session_state.authenticated = True
        st.session_state.start_time = datetime.now()

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

        # Logged in date time
        st.write(f"Logged In Since: {st.session_state.start_time.strftime('%a %d of %B %H:%M')}")
        
        if len(st.session_state.data_list) >= 10 or (datetime.now()-st.session_state.start_time).total_seconds() > 60:
            df = pd.DataFrame(st.session_state.data_list, columns=["Value", "Timestamp", "Username"])
            st.dataframe(df)
            st.session_state.data_list = []  # Clear the list
            st.session_state.start_time = datetime.now()

if __name__ == "__main__":
    main()


