import streamlit as st
from tts import text_to_speech, get_available_voices
from auth import logout, update_user_settings
from utils import load_user_settings, save_user_settings

def get_voice_name(voice_id, available_voices, lang):
    for vid, name in available_voices:
        if vid == voice_id:
            return name
    return lang["unknown_voice"]

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

    # Voice selection
    user_settings = load_user_settings()
    try:
        available_voices = get_available_voices(user_settings['elevenlabs_api_key'], lang)
        voice_options = [f"{name} ({voice_id})" for voice_id, name in available_voices]
        current_voice = st.session_state.get('selected_voice')
        current_voice_name = get_voice_name(current_voice, available_voices, lang) if current_voice else ""
        current_voice_option = f"{current_voice_name} ({current_voice})" if current_voice else voice_options[0]
        selected_voice = st.sidebar.selectbox(lang["voice_select"], voice_options, index=voice_options.index(current_voice_option) if current_voice else 0)
        selected_voice_id = selected_voice.split('(')[-1].split(')')[0]
    except ValueError as e:
        st.sidebar.error(str(e))
        selected_voice_id = None

    # Voice settings
    st.sidebar.subheader(lang["voice_settings"])
    stability = st.sidebar.slider(lang["stability"], 0.0, 1.0, st.session_state.get('stability', 0.8))
    similarity_boost = st.sidebar.slider(lang["similarity_boost"], 0.0, 1.0, st.session_state.get('similarity_boost', 1.0))
    speaker_boost = st.sidebar.checkbox(lang["speaker_boost"], value=st.session_state.get('speaker_boost', False))

    # API Settings
    if st.sidebar.checkbox(lang["show_api_settings"]):
        render_api_settings(lang)

    return selected_voice_id, stability, similarity_boost, speaker_boost

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
            try:
                audio = text_to_speech(user_input, st.session_state.get('selected_voice'), {
                    "stability": st.session_state.get('stability'),
                    "similarity_boost": st.session_state.get('similarity_boost'),
                    "speaker_boost": st.session_state.get('speaker_boost', False),
                    "api_key": user_settings['elevenlabs_api_key']
                }, lang)
                st.audio(audio, format="audio/mp3")
                
                # Add to chat history
                if 'history' not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.append(user_input)
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"{lang['error_unexpected']}: {str(e)}")

    # Display chat history
    if st.sidebar.checkbox(lang["show_history"]):
        st.subheader(lang["history"])
        for item in st.session_state.get('history', []):
            st.write(item)
            if st.button(f"{lang['repeat']} '{item[:20]}...'"):
                try:
                    audio = text_to_speech(item, st.session_state.get('selected_voice'), {
                        "stability": st.session_state.get('stability'),
                        "similarity_boost": st.session_state.get('similarity_boost'),
                        "speaker_boost": st.session_state.get('speaker_boost', False),
                        "api_key": user_settings['elevenlabs_api_key']
                    }, lang)
                    st.audio(audio, format="audio/mp3")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"{lang['error_unexpected']}: {str(e)}")