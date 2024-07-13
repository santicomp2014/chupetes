import streamlit as st
from tts import text_to_speech
from auth import logout
from utils import load_user_settings, save_user_settings

def render_sidebar(user, lang):
    st.sidebar.title(f"Welcome, {user['name']}!")
    if st.sidebar.button("Logout"):
        logout()
        st.experimental_rerun()

    # Language selection
    languages = ["English", "Español"]  # Add more languages as needed
    selected_lang = st.sidebar.selectbox("Select Language", languages)
    if selected_lang != st.session_state.get('language'):
        st.session_state.language = selected_lang
        st.experimental_rerun()

    # Voice selection (you'd need to implement this based on ElevenLabs API)
    voices = ["voice1", "voice2", "voice3"]  # Replace with actual voice IDs
    selected_voice = st.sidebar.selectbox(lang["voice_select"], voices)

    # Voice settings
    st.sidebar.subheader(lang["voice_settings"])
    stability = st.sidebar.slider(lang["stability"], 0.0, 1.0, 0.5)
    similarity_boost = st.sidebar.slider(lang["similarity_boost"], 0.0, 1.0, 0.5)

    # API Settings
    if st.sidebar.checkbox("Show API Settings"):
        render_api_settings()

    return selected_voice, stability, similarity_boost

def render_api_settings():
    st.sidebar.subheader("API Settings")
    settings = load_user_settings()
    
    new_settings = {}
    new_settings['elevenlabs_api_key'] = st.sidebar.text_input("ElevenLabs API Key", value=settings['elevenlabs_api_key'], type="password")
    new_settings['openai_api_key'] = st.sidebar.text_input("OpenAI API Key", value=settings['openai_api_key'], type="password")
    new_settings['anthropic_api_key'] = st.sidebar.text_input("Anthropic API Key", value=settings['anthropic_api_key'], type="password")

    if st.sidebar.button("Save API Settings"):
        save_user_settings(new_settings)
        st.sidebar.success("API settings saved successfully!")

def render_main_interface(lang):
    st.title(lang["title"])
    user_input = st.text_area(lang["input_text"])

    if st.button(lang["speak_button"]):
        if user_input:
            settings = load_user_settings()
            audio = text_to_speech(user_input, st.session_state.get('selected_voice'), {
                "stability": st.session_state.get('stability'),
                "similarity_boost": st.session_state.get('similarity_boost'),
                "api_key": settings['elevenlabs_api_key']
            })
            st.audio(audio, format="audio/mp3")
            
            # Add to chat history
            if 'history' not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append(user_input)

    # Display chat history
    if st.sidebar.checkbox(lang["show_history"]):
        st.subheader(lang["history"])
        for item in st.session_state.get('history', []):
            st.write(item)
            if st.button(f"{lang['repeat']} '{item[:20]}...'"):
                settings = load_user_settings()
                audio = text_to_speech(item, st.session_state.get('selected_voice'), {
                    "stability": st.session_state.get('stability'),
                    "similarity_boost": st.session_state.get('similarity_boost'),
                    "api_key": settings['elevenlabs_api_key']
                })
                st.audio(audio, format="audio/mp3")