import streamlit as st
from supabase import create_client, Client
import re

# Supabase config
SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
SUPABASE_KEY = "YOUR_PUBLIC_ANON_KEY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

def is_valid_password(password: str) -> bool:
    return len(password) >= 8 and re.search(r"[^a-zA-Z0-9]", password)

def sign_up():
    st.subheader("Sign Up")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    
    if st.button("Sign Up"):
        if not is_valid_password(password):
            st.error("Password must be at least 8 characters and include a special character.")
            return
        
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if res.user:
            st.success("Check your email to confirm your address before logging in.")
        else:
            st.error("Sign-up failed. You may already have an account.")

def login():
    st.subheader("Log In")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Log In"):
        try:
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if res.user:
                st.session_state.user = res.user
                st.success("Logged in!")
        except Exception as e:
            st.error("Login failed: make sure your email is confirmed.")

def main_app():
    st.subheader("Welcome!")
    st.write(f"Hello, {st.session_state.user['email']}")
    if st.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()

st.title("Secure App with Supabase Auth")

# Routing logic
if st.session_state.user:
    main_app()
else:
    page = st.radio("Choose an action", ["Log In", "Sign Up"])
    if page == "Log In":
        login()
    else:
        sign_up()
