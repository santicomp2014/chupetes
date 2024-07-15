import streamlit as st
from tts import text_to_speech
from auth import logout
from utils import load_user_settings, save_user_settings

def render_sidebar(user, lang):
    st.sidebar.title(f"{lang['welcome']}, {user['name']}!")
    if st.sidebar.button(lang["logout_button"]):
        logout()
        st.experimental_rerun()

    # Language selection
    languages = ["English", "Español"]  # Add more languages as needed
    selected_lang = st.sidebar.selectbox(lang["language_select"], languages, index=languages.index(st.session_state.language))
    if selected_lang != st.session_state.language:
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
    if st.sidebar.checkbox(lang["show_api_settings"]):
        render_api_settings(lang)

    return selected_voice, stability, similarity_boost

def render_api_settings(lang):
    st.sidebar.subheader(lang["api_settings"])
    settings = load_user_settings()
    
    new_settings = {}
    new_settings['elevenlabs_api_key'] = st.sidebar.text_input(lang["elevenlabs_api_key"], value=settings['elevenlabs_api_key'], type="password")
    new_settings['openai_api_key'] = st.sidebar.text_input(lang["openai_api_key"], value=settings['openai_api_key'], type="password")
    new_settings['anthropic_api_key'] = st.sidebar.text_input(lang["anthropic_api_key"], value=settings['anthropic_api_key'], type="password")

    if st.sidebar.button(lang["save_api_settings"]):
        save_user_settings(new_settings)
        st.sidebar.success(lang["api_settings_saved"])

def render_main_interface(lang, user_settings):
    st.title(lang["title"])
    user_input = st.text_area(lang["input_text"])

    if st.button(lang["speak_button"]):
        if user_input:
            audio = text_to_speech(user_input, st.session_state.get('selected_voice'), {
                "stability": st.session_state.get('stability'),
                "similarity_boost": st.session_state.get('similarity_boost'),
                "api_key": user_settings['elevenlabs_api_key']
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
                audio = text_to_speech(item, st.session_state.get('selected_voice'), {
                    "stability": st.session_state.get('stability'),
                    "similarity_boost": st.session_state.get('similarity_boost'),
                    "api_key": user_settings['elevenlabs_api_key']
                })
                st.audio(audio, format="audio/mp3")