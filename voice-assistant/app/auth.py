import streamlit as st
import hashlib

# Hardcoded user data (for demonstration purposes only)
USERS = {
    "santi": {
        "password": hashlib.sha256("test".encode()).hexdigest(),
        "user_id": "001",
        "name": "Santiago",
        "lastname": "Regusci",
        "email": "santi.doe@gmail.com",
    },
    "chupete": {
        "password": hashlib.sha256("chupete".encode()).hexdigest(),
        "user_id": "002",
        "name": "Chupete",
        "lastname": "Chupete",
        "email": "chupete@gmail.com"
    }
}

def get_user():
    user = st.session_state.get('user')
    if user:
        return {
            "username": user,
            "user_id": USERS[user]["user_id"],
            "name": USERS[user]["name"],
            "lastname": USERS[user]["lastname"],
            "email": USERS[user]["email"]
        }
    return None

def is_authenticated():
    return st.session_state.get('authenticated', False)

def login(username, password):
    if username in USERS and USERS[username]["password"] == hashlib.sha256(password.encode()).hexdigest():
        st.session_state.user = username
        st.session_state.authenticated = True
        return True
    return False

def logout():
    st.session_state.user = None
    st.session_state.authenticated = False
    if 'user_settings' in st.session_state:
        del st.session_state.user_settings