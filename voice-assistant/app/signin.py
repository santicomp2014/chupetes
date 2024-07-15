import streamlit as st
from auth import login, get_user

def render_signin_page(lang):
    st.title(lang["signin_title"])
    
    username = st.text_input(lang["username_label"])
    password = st.text_input(lang["password_label"], type="password")
    
    if st.button(lang["signin_button"]):
        if login(username, password):
            user = get_user()
            st.success(f"{lang['signin_success']} {user['name']} {user['lastname']}!")
            st.experimental_rerun()
        else:
            st.error(lang["signin_error"])

    # Language selector
    languages = ["Español", "English"]  # Add more languages as needed
    selected_lang = st.selectbox(lang["language_select"], languages, index=languages.index(st.session_state.language))
    
    # Check if language has changed
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.experimental_rerun()

    # Add a small text to show the current language (for debugging)
    #st.text(f"Current language: {st.session_state.language}")