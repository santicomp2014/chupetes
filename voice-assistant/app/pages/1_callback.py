import streamlit as st
from auth import handle_callback

st.set_page_config(page_title="Authentication Callback")

def callback_page():
    st.title("Authenticating...")
    try:
        user_info = handle_callback()
        if user_info:
            st.success("Authentication successful!")
            st.session_state.user = user_info
            st.write("Redirecting to main page...")
            st.experimental_set_query_params()
            st.experimental_rerun()
        else:
            st.error("Authentication failed. Please try again.")
            st.write("Redirecting to login page...")
            st.experimental_set_query_params()
            st.experimental_rerun()
    except Exception as e:
        st.error(f"An error occurred during authentication: {str(e)}")
        st.write("Please try logging in again.")
        st.experimental_set_query_params()

callback_page()