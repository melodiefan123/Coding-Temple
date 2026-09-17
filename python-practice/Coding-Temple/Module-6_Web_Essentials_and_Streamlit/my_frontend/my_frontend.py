

import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(page_title="Task Manager", page_icon="✅", layout="wide")

#--Session State Init -- 

if "token" not in st.session_state: 
    st.session_state["token"] = None 
    st.session_state['username'] = None

#--Helper Functions --
def api_get(endpoint, token):
    try: 
        r = requests.get(f"{API}{endpoint}", headers={"Authorization": f"Bearer {token}"})
        if r.status_code == 401: return "unauthorized"
        return r.json() if r.ok else None
    except requests.exceptions.ConnectionError:
        return "connection_error"
    
def api_post(endpoint, token, data=None):
    try: 
        r = requests.post(f"{API}{endpoint}", headers={"Authorization": f"Bearer {token}"}, json=data )
        return r.ok
    except requests.exceptions.ConnectionError:
        return False

# Login/Logout - Login form with username and password, JWT stored in session state, user displayed in sidebar, working logout button
if st.session_state["token"] is None: 
    st.title("Login Page")
    with st.form("login"): 
        user_name = st.text_input("Username", placeholder="admin or student")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted: 
            try: 
                r = requests.post(f"{API}/auth/token", data={"username": user_name, "password": password})
                if r.status_code == 200: 
                    st.session_state['token'] = r.json()["access_token"]
                    st.session_state['username'] = user_name
                    st.rerun()
                else: 
                    st.error("Invalid credentials")
            except requests.exceptions.ConnectionError: 
                st.error("Cannot connect to API. Is the backend running?")
        st.stop()
with st.sidebar: 
    st.write(f"Logged in as **{st.session_state['username']}**")
    if st.button("Logout"): 
        st.session_state["token"] = None
        st.session_state["username"] = None
        st.rerun()
#---Load Data---
token = st.session_state["token"]
stats = api_get("/stats", token)
tasks_list = api_get("/tasks", token)

# Error handling - Show a clear message if the backend is unreachable, and handle 401s by redirecting to login
if stats == "connection_error" or tasks_list == "connection_error":
    st.error("Cannot connect to the API. Is the backend running?")
    st.stop()
if stats == "unauthorized" or tasks_list == "unauthorized": 
    st.warning("Session expired. Please login again.")
    st.session_state["token"] = None 
    st.rerun()

# Metrics - Display at least 2 st.metric() cards (total tasks, completed tasks)
col1, col2 = st.columns(2)
col1.metric("Total", stats["total"])
col2.metric("Completed", stats["done"])

# Task list - Display all tasks with their status
st.subheader("Tasks")
if tasks_list:
    for task in tasks_list:
        status = "✅" if task["done"] else "⬜"
        st.write(f"{status} {task['title']}")

# Add task form - A form that POSTs a new task to the API
with st.form("add_task", clear_on_submit=True): 
    new_title = st.text_input("New Task")
    if st.form_submit_button("➕ Add Task") and new_title.strip(): 
        api_post("/tasks", token, {"title": new_title.strip()})
        st.rerun()

