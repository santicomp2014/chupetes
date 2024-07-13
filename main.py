import streamlit as st
from dotenv import load_dotenv
import os
from auth import login, logout, callback, get_user, is_authenticated
from tts import text_to_speech
from ui import render_main_interface, render_sidebar
from utils import load_language_config, load_user_settings

# Load environment variables
load_dotenv()

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

def main():
    st.set_page_config(page_title="Voice Assistant", layout="wide")

    # Handle Auth0 callback
    params = st.experimental_get_query_params()
    if 'code' in params and 'state' in params:
        callback()
        st.experimental_set_query_params()
        st.experimental_rerun()

    # Check authentication
    if not is_authenticated():
        st.title("Welcome to Voice Assistant")
        login()
        return

    # User is authenticated
    user = get_user()
    lang = load_language_config(st.session_state.get('language', 'English'))
    user_settings = load_user_settings()

    selected_voice, stability, similarity_boost = render_sidebar(user, lang)
    
    # Update session state with current settings
    st.session_state.update({
        'selected_voice': selected_voice,
        'stability': stability,
        'similarity_boost': similarity_boost
    })

    render_main_interface(lang, user_settings)

    # You can add more components or features here in the future

if __name__ == "__main__":
    main()