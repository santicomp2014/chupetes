import streamlit as st
import os
from authlib.integrations.requests_client import OAuth2Session
import requests

AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

def get_token():
    return st.session_state.get('token')

def set_token(token):
    st.session_state.token = token

def login():
    client = OAuth2Session(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET,
                           scope='openid profile email',
                           redirect_uri=AUTH0_CALLBACK_URL)
    uri, state = client.create_authorization_url(f'https://{AUTH0_DOMAIN}/authorize')
    st.session_state.oauth_state = state
    st.markdown(f'<a href="{uri}" target="_self">Login</a>', unsafe_allow_html=True)

def callback():
    client = OAuth2Session(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET,
                           state=st.session_state.oauth_state,
                           redirect_uri=AUTH0_CALLBACK_URL)
    token = client.fetch_token(f'https://{AUTH0_DOMAIN}/oauth/token',
                               authorization_response=st.experimental_get_query_params())
    set_token(token)
    user_info = client.get(f'https://{AUTH0_DOMAIN}/userinfo').json()
    st.session_state.user = user_info
    return user_info

def logout():
    st.session_state.user = None
    st.session_state.token = None
    # Clear user settings on logout
    if 'user_settings' in st.session_state:
        del st.session_state.user_settings

def get_user():
    return st.session_state.user

def is_authenticated():
    return st.session_state.user is not None