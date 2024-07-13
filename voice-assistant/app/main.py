import streamlit as st
from dotenv import load_dotenv
import os
from auth import login, logout, get_user, is_authenticated
from tts import text_to_speech
from ui import render_main_interface, render_sidebar
from utils import load_language_config, load_user_settings, get_default_language

# Load environment variables
load_dotenv()

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

if 'language' not in st.session_state:
    st.session_state.language = get_default_language()

def main():
    st.set_page_config(page_title="Voice Assistant", layout="wide")

    # Load language configuration
    lang = load_language_config(st.session_state.language)

    # Language selector (before login)
    if not is_authenticated():
        languages = ["Español","English"]  # Add more languages as needed
        selected_lang = st.selectbox("Seleccione el idioma/ Select Language", languages)
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.experimental_rerun()

    # Check authentication
    if not is_authenticated():
        st.title(lang["welcome_title"])
        login(lang)
        return

    # User is authenticated
    user = get_user()
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