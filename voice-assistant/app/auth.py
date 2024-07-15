import streamlit as st
import hashlib
import os
from utils import load_user_settings

# User data now includes all user-specific settings, with API keys being optional
USERS = {
    "santi": {
        "password": hashlib.sha256("test".encode()).hexdigest(),
        "user_id": "001",
        "name": "Santiago",
        "lastname": "Regusci",
        "email": "santi.doe@gmail.com",
        "voice_id": "21m00Tcm4TlvDq8ikWAM",
        "stability": 0.5,
        "similarity_boost": 0.75,
        "speaker_boost": True,
    },
    "chupete": {
        "password": hashlib.sha256("chupete".encode()).hexdigest(),
        "user_id": "002",
        "name": "Chupete",
        "lastname": "Chupete",
        "email": "chupete@gmail.com",
        "voice_id": "EXAVITQu4vr4xnSDxMaL",
        "stability": 0.8,
        "similarity_boost": 0.6,
        "speaker_boost": False,
    }
}

def get_user():
    username = st.session_state.get('user')
    if username:
        user_data = USERS[username].copy()
        # Load API keys from user settings or environment variables
        user_settings = load_user_settings()
        user_data['elevenlabs_api_key'] = user_settings.get('elevenlabs_api_key', os.getenv("ELEVEN_LABS_API_KEY", ""))
        user_data['openai_api_key'] = user_settings.get('openai_api_key', os.getenv("OPENAI_API_KEY", ""))
        user_data['anthropic_api_key'] = user_settings.get('anthropic_api_key', os.getenv("ANTHROPIC_API_KEY", ""))
        return user_data
    return None

def is_authenticated():
    return st.session_state.get('authenticated', False)

def login(username, password):
    if username in USERS and USERS[username]["password"] == hashlib.sha256(password.encode()).hexdigest():
        st.session_state.user = username
        st.session_state.authenticated = True
        user_data = get_user()  # This now includes the API keys
        # Set session state with user data
        st.session_state.update(user_data)
        return True
    return False

def logout():
    st.session_state.clear()

def update_user_settings(username, settings):
    if username in USERS:
        USERS[username].update(settings)
        # Update session state
        st.session_state.update(settings)
        # Save API keys to user settings
        user_settings = load_user_settings()
        for key in ['elevenlabs_api_key', 'openai_api_key', 'anthropic_api_key']:
            if key in settings:
                user_settings[key] = settings[key]
        st.session_state.user_settings = user_settings

def save_session_settings():
    username = st.session_state.get('user')
    if username:
        settings_to_save = {
            'voice_id': st.session_state.get('voice_id'),
            'stability': st.session_state.get('stability'),
            'similarity_boost': st.session_state.get('similarity_boost'),
            'speaker_boost': st.session_state.get('speaker_boost'),
        }
        update_user_settings(username, settings_to_save)