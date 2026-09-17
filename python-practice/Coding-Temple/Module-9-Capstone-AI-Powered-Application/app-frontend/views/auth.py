import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="LedgeAI - Auth", page_icon="🔐")

st.title("🔐 Authentication")

st.markdown("""
<style>
    /* 1. Labels above input fields */
    div[data-widget="stTextInput"] label,
    div[data-widget="stNumberInput"] label,
    div[data-widget="stSelectbox"] label,
    div[data-testid="stWidgetLabel"] p {
        color: #FFFFFF !important;
    } 
</style>
""", unsafe_allow_html=True)
# Session state initialization
if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state["token"]:
    st.success("You are logged in!")
    if st.button("Log Out"):
        st.session_state["token"]= None
        st.rerun()
else:
    tab1, tab2 = st.tabs(["Sign In", "Register"])

    with tab1:
        st.subheader("Login to LedgeAI")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Sign In"):
            response = requests.post(
                f"{API_URL}/auth/login",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.token = data["access_token"]
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error(response.json().get("detail", "Login failed."))

    with tab2:
        st.subheader("Create an Account")
        reg_username = st.text_input("Username", key="reg_user")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            if not reg_username or not reg_password:
                st.warning("Please enter a username and password.")
            else:
                try:
                    response = requests.post(
                        f"{API_URL}/auth/register",
                        json={"username": reg_username, "email": reg_email, "password": reg_password}, 
                        timeout = 10
                    )
                    if response.status_code in(200,201):
                        data = response.json()
                        raw_token = data.get("access_token", "")
                        if raw_token:
                            st.session_state["token"] = str(raw_token).strip().strip('"')
                            st.success("Account created successfully!")
                        else: 
                            st.success("Account created! Please switch to Sign In to log in.")
                            
                        st.rerun()
                    else:
                        st.error(response.json().get("detail", "Registration failed."))
                except requests.exceptions.RequestException as e:
                    st.error(f"Could not connect to backend server: {e}")