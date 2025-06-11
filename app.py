import streamlit as st
from supabase import create_client, Client
import re


# Load Supabase credentials from Streamlit secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

if "user" not in st.session_state:
    st.session_state.user = None

# Password rules: 8+ chars, at least 1 special character
def is_valid_password(password: str) -> bool:
    return len(password) >= 8 and re.search(r"[^a-zA-Z0-9]", password)

# Sign up page
def sign_up():
    st.subheader("🆕 Sign Up")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Create Account"):
        if not is_valid_password(password):
            st.error("Password must be at least 8 characters and contain a special character.")
            return
        try:
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            if res.user:
                st.success("Check your email to confirm before logging in.")
        except Exception as e:
            st.error(f"Sign-up failed: {e}")

# Login page
def login():
    st.subheader("🔐 Log In")
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
                st.experimental_rerun()
        except Exception as e:
            st.error("Login failed. Confirm your email or reset your password.")

# Forgot password page
def forgot_password_page():
    st.subheader("🔑 Forgot Password?")
    email = st.text_input("Enter your email")

    if st.button("Send Reset Email"):
        if not email:
            st.error("Please enter your email.")
            return
        try:
            supabase.auth.reset_password_email(email)
            st.success("📬 Check your email. Supabase will let you set a new password.")
        except Exception as e:
            st.error(f"Failed to send reset email: {e}")

# Main app (after login)
def main_app():
    st.subheader("🏠 Welcome!")
    st.write(f"You are logged in as: **{st.session_state.user['email']}**")

    with st.expander("🔒 Change Password"):
        new_pw = st.text_input("New Password", type="password", key="new_pw")
        confirm_pw = st.text_input("Confirm Password", type="password", key="confirm_pw")

        if st.button("Change Password"):
            if new_pw != confirm_pw:
                st.error("Passwords do not match.")
            elif not is_valid_password(new_pw):
                st.error("Password must be at least 8 characters and include a special character.")
            else:
                try:
                    supabase.auth.update_user({"password": new_pw})
                    st.success("Password updated successfully.")
                except Exception as e:
                    st.error(f"Error updating password: {e}")

    if st.button("Log Out"):
        st.session_state.user = None
        st.experimental_rerun()

# App router
st.set_page_config(page_title="Secure App", page_icon="🔐")
st.title("🔐 Streamlit + Supabase Auth")

if st.session_state.user:
    main_app()
else:
    page = st.radio("Choose an option:", ["Log In", "Sign Up", "Forgot Password"])
    if page == "Log In":
        login()
    elif page == "Sign Up":
        sign_up()
    elif page == "Forgot Password":
        forgot_password_page()
