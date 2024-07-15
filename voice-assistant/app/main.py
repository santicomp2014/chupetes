import streamlit as st
from dotenv import load_dotenv
import os
from auth import logout, get_user, is_authenticated, save_session_settings
from tts import text_to_speech
from ui import render_main_interface, render_sidebar
from utils import load_language_config, load_user_settings, get_default_language
from signin import render_signin_page

# Load environment variables
load_dotenv()

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

if 'language' not in st.session_state:
    st.session_state.language = get_default_language()

def main():
    st.set_page_config(page_title="Chupetes Voice Assistant", layout="wide")

    # Ensure language is always a string (in case it's not set properly)
    if not isinstance(st.session_state.language, str):
        st.session_state.language = get_default_language()

    # Load language configuration
    lang = load_language_config(st.session_state.language)

    # Check authentication
    if not is_authenticated():
        render_signin_page(lang)
        return

    # User is authenticated
    user = get_user()

    selected_voice, stability, similarity_boost, speaker_boost = render_sidebar(user, lang)
    
    # Update session state with current settings
    st.session_state.update({
        'selected_voice': selected_voice,
        'stability': stability,
        'similarity_boost': similarity_boost,
        'speaker_boost': speaker_boost
    })

    # Save session settings to user data
    save_session_settings()

    render_main_interface(lang, st.session_state)

    # You can add more components or features here in the future

if __name__ == "__main__":
    main()