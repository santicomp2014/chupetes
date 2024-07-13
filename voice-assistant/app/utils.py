import json
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

def load_language_config(language):
    config_path = os.path.join('config', 'languages.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        languages = json.load(f)
    return languages.get(language, languages['English'])  # Default to English if language not found

def load_user_settings():
    if 'user_settings' not in st.session_state:
        st.session_state.user_settings = {
            'elevenlabs_api_key': os.getenv("ELEVEN_LABS_API_KEY", ""),
            'openai_api_key': os.getenv("OPENAI_API_KEY", ""),
            'anthropic_api_key': os.getenv("ANTHROPIC_API_KEY", "")
        }
    return st.session_state.user_settings

def save_user_settings(settings):
    st.session_state.user_settings = settings

def get_default_language():
    # You can implement logic here to determine the default language
    # For now, we'll just return 'English'
    return 'Spanish'

# Add more utility functions as needed