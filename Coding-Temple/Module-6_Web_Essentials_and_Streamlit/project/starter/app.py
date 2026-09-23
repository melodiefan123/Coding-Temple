"""
Module 6 Project — AI Dashboard
"""

import streamlit as st
from mock_data import MOCK_TASKS, MOCK_STATS, MOCK_USER, MOCK_TOKEN, MOCK_CHAT_HISTORY
import api_client
import time
import anthropic
import pandas as pd

# Page Configuration
st.set_page_config(layout="wide", page_title="AI Dashboard", page_icon="🤖")

# Session State Initialisation
if "token" not in st.session_state:
    st.session_state["token"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

if "messages" not in st.session_state: 
    st.session_state["messages"] = []

if "use_mock" not in st.session_state: 
    st.session_state["use_mock"] = False


# SECTION A — AUTHENTICATION GATE
if not st.session_state["token"]:
    st.title("🔐 Login")
    with st.form("Login Form", clear_on_submit=True):
        mock_data = st.checkbox("Use Mock Data")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted: 
            if mock_data:
                st.session_state["token"] = MOCK_TOKEN
                st.session_state["username"] = MOCK_USER
                st.session_state["use_mock"] = True
                st.rerun()
            else:
                token, error = api_client.login(username=username, password=password)
                if error: 
                    st.error(error)
                elif token: 
                    st.session_state["username"] = username
                    st.session_state["token"] = token
                    st.rerun()
    st.stop()


# SECTION B — SIDEBAR
with st.sidebar:
    st.title("Task Manager")
    st.divider()
    st.write(f"👤 Logged in as: **{st.session_state['username']}**")
    st.session_state["use_mock"] = st.checkbox("Use Mock Data", value=st.session_state["use_mock"])
    
    # Read key from secrets if available, or allow manual input
    default_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    api_key = st.text_input("Anthropic API Key", value=default_key, type="password")
    system_prompt = st.text_input("System Prompt", value="You are a helpful AI assistant for task management.", help="Sets AI personality.")
    
    logout = st.button("Logout")
    if logout: 
        st.session_state["username"] = None
        st.session_state["token"] = None
        st.session_state["messages"] = []
        st.rerun()
        
    st.divider()
    st.caption("AI Dashboard v1.0 — Module 6 Project")


# SECTION C — MAIN CONTENT TABS
tab_dash, tab_task, tab_chat = st.tabs(["📊 Dashboard", "✅ Tasks", "🤖 AI Chat"])

# TAB 1: Dashboard
with tab_dash:
    st.header("Dashboard")
    error = None
    tasks = []
    
    if st.session_state["use_mock"]:
        tasks = MOCK_TASKS
    else:
        with st.spinner("Fetching tasks..."):
            tasks, error = api_client.get_tasks(token=st.session_state["token"])
            
    if tasks is None:
        tasks = []
        
    if error: 
        st.error(error)
    else: 
        total_count = len(tasks)
        done_count = sum(1 for task in tasks if task.get('completed'))
        pending_count = total_count - done_count
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Tasks", total_count)
        col2.metric("Done", done_count)
        col3.metric("Pending", pending_count)
        
        st.subheader("Task Overview")
        if tasks:
            df = pd.DataFrame(tasks)
            st.dataframe(df, use_container_width=True)
            
            chart_data = pd.DataFrame({
                "Status": ["Done", "Pending"],
                "Count": [done_count, pending_count]
            })
            st.bar_chart(chart_data.set_index("Status"))
        else:
            st.info("No tasks found.")

# TAB 2: Tasks
with tab_task:
    st.subheader("Create New Task")
    with st.form("Create Tasks", clear_on_submit=True):
        title = st.text_input("Task Title")
        submitted = st.form_submit_button("Add Task")
        
        if submitted: 
            if not title.strip():
                st.error("Task title cannot be empty.")
            else: 
                if st.session_state['use_mock']: 
                    MOCK_TASKS.append({
                        "id": len(MOCK_TASKS) + 1,
                        "title": title,
                        "completed": False
                    })
                    st.success("Task added (mock mode)")
                    st.rerun()
                else:
                    task, error = api_client.create_task(
                        token=st.session_state["token"],
                        title=title
                    )
                    if error:
                        st.error(error)
                    else:
                        st.success("Task created")
                        st.rerun()
                        
    st.divider()
    st.subheader("Your Tasks")
    
    tasks = []
    if st.session_state["use_mock"]:
        tasks = MOCK_TASKS
    else:
        tasks, error = api_client.get_tasks(st.session_state["token"])
        if error:
            st.error(error)
            tasks = []
            
    if tasks:
        for task in tasks: 
            col1, col2 = st.columns([4, 1])
            with col1: 
                status = "✅" if task.get('completed') else "⬜"
                st.write(f"{status} **{task.get('title')}**")
            with col2: 
                if not task.get('completed'): 
                    if st.button("Complete", key=f"complete_{task.get('id')}"):
                        if st.session_state["use_mock"]:
                            task["completed"] = True
                            st.rerun()
                        else:
                            updated, error = api_client.complete_task(
                                token=st.session_state["token"],
                                task_id=task["id"]
                            )
                            if error:
                                st.error(f"Failed to complete task: {error}")
                            else:
                                st.success("Task completed")
                                st.rerun()
    else:
        st.info("No tasks available.")

# TAB 3: AI Chat
with tab_chat: 
    st.header("AI Assistant")
    
    if st.session_state["use_mock"] and not st.session_state["messages"]:
        st.session_state["messages"] = MOCK_CHAT_HISTORY.copy()
    
    for message in st.session_state["messages"]:
        with st.chat_message(message['role']):
            st.write(message['content'])
    
    if prompt := st.chat_input("Can I help with anything?"):
        st.session_state['messages'].append({
            "role": "user", 
            "content": prompt
        })
        
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            streamed = ""

            if st.session_state['use_mock'] or not api_key:
                response = f"Mock response to: {prompt}"
                for word in response.split():
                    streamed += word + " "
                    time.sleep(0.05)
                    placeholder.write(streamed)
            else: 
                client = anthropic.Anthropic(api_key=api_key)
                
                # Format session messages for Anthropic API context
                api_messages = [
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state["messages"]
                ]
                
                with client.messages.stream(
                    model="claude-3-5-sonnet-latest",
                    max_tokens=500,
                    system=system_prompt,
                    messages=api_messages,
                ) as stream:
                    for event in stream:
                        if event.type == "content_block_delta":
                            streamed += event.delta.text
                            placeholder.write(streamed)
        
        st.session_state["messages"].append({
            "role": "assistant",
            "content": streamed
        })
        st.rerun()