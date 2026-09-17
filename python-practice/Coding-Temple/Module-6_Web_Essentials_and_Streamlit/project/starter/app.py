"""
Module 6 Project — AI Dashboard  (STARTER)
==========================================
Run with:
    # Start the backend (when ready):
    uvicorn backend:app --reload --port 8000

    # Start the Streamlit app:
    streamlit run app.py

Your goal: build a full Streamlit dashboard with authentication,
task management, data visualisation, and an AI chat feature.

Required sections (each marked with TODO):
    1. Authentication — login form, JWT in session state, logout
    2. Dashboard view — metrics, task list, chart
    3. Data interaction — add task form, complete task buttons
    4. AI chat feature — chat history, mock responses, streaming
    5. Layout — sidebar, tabs, metrics, error messages

Import the API functions from api_client.py (not requests directly).
Use mock_data.py to test the UI while the backend is being built.
"""

import streamlit as st
from mock_data import MOCK_TASKS, MOCK_STATS, MOCK_USER, MOCK_TOKEN, MOCK_CHAT_HISTORY
import api_client
import time
import anthropic
import pandas as pd

# ── Step 1: Page configuration ─────────────────────────────────────────────
# TODO: st.set_page_config(layout="wide", page_title="AI Dashboard", page_icon="🤖")
st.set_page_config(layout="wide", page_title="AI Dashboard", page_icon="🤖")

# ── Step 2: Session state initialisation ───────────────────────────────────
# TODO: Initialise all session state keys you will need:
#   "token"    → None
#   "username" → None
#   "messages" → []    (chat history)
#   "use_mock" → False (toggle to use mock data instead of the real API)

#════════════════════════════════════════════════════════════════════════════
if "token" not in st.session_state:
    st.session_state["token"]= None

if "username" not in st.session_state:
    st.session_state["username"] = None

if "messages" not in st.session_state: 
    st.session_state["messages"] = []

if "use_mock" not in st.session_state: 
    st.session_state["use_mock"] = False

# SECTION A — AUTHENTICATION
# ════════════════════════════════════════════════════════════════════════════
# TODO: Auth gate — if no token, show login form and st.stop()
#
# Login form should:
#   - Have username + password fields
#   - Have a "Use Mock Data" checkbox (sets token = MOCK_TOKEN, username = MOCK_USER)
#   - On real login: call api_client.login(username, password)
#   - Store token + username in session state on success
#   - Show st.error on failure
#   - Call st.rerun() after successful login

# ════════════════════════════════════════════════════════════════════════════
if not st.session_state["token"]:
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
                    st.error("Failed to login")
                if token: 
                    st.session_state["username"] = username
                    st.session_state["token"] = token
                    st.rerun()
        st.stop()



# SECTION B — SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
# TODO: with st.sidebar:
#   - App title and divider
#   - "Logged in as [username]"
#   - Logout button (clear token/username, st.rerun())
#   - AI Chat settings (API key input, system prompt)
#   - Divider and caption

# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    title = st.title("Task Manager")
    st.divider()
    st.write(f"Logged in as {st.session_state['username']}")
    st.session_state["use_mock"] = st.checkbox("Use Mock Data", value=st.session_state["use_mock"])
    api_key = st.text_input("Anthropic API Key", type="password")
    system_prompt = st.text_input("System Prompt", value = "You are a helpful AI assistant for task management.", help="This sets the AI's personality and behavior.")
    logout = st.button("Logout")
    if logout: 
        st.session_state["username"] = None
        st.session_state["token"] = None
        st.rerun()
    st.divider()
    st.caption("AI Dashboard v1.0 — Module 6 Project")
        


# SECTION C — MAIN CONTENT (tabs)
# ════════════════════════════════════════════════════════════════════════════
# TODO: Create 3 tabs: "📊 Dashboard", "✅ Tasks", "🤖 AI Chat"
# tab_dash, tab_tasks, tab_chat = st.tabs(["📊 Dashboard", "✅ Tasks", "🤖 AI Chat"])

# ── TAB 1: Dashboard ──────────────────────────────────────────────────────
# TODO: with tab_dash:
#   - Load tasks (or use MOCK_TASKS if in mock mode)
#   - Show 3 st.metric() in 3 columns: total, done, pending
#   - Show st.dataframe() with task data
#   - Show a bar chart of done vs pending

# ── TAB 2: Tasks ──────────────────────────────────────────────────────────
# TODO: with tab_tasks:
#   - Add task form (POST to API or append to mock data)
#   - Task list with Complete buttons (PATCH to API or update mock)
#   - Error handling for API failures

# ── TAB 3: AI Chat ────────────────────────────────────────────────────────
# TODO: with tab_chat:
#   - Render chat history (st.chat_message for each message)
#   - st.chat_input for user messages
#   - Mock response generator or real OpenAI call
#   - st.write_stream for streaming display
#   - Append both user and assistant messages to session state

tab_dash, tab_task, tab_chat = st.tabs(["📊 Dashboard", "✅ Tasks", "🤖 AI Chat"])

# TODO: with tab_dash:
#   - Load tasks (or use MOCK_TASKS if in mock mode)
#   - Show 3 st.metric() in 3 columns: total, done, pending
#   - Show st.dataframe() with task data
#   - Show a bar chart of done vs pending


with tab_dash:
    error = None
    tasks=[]
    
    if st.session_state["use_mock"]:
        tasks = MOCK_TASKS
    else:
        tasks, error = api_client.get_tasks(token=st.session_state["token"])
    if tasks is None:
        tasks = []
    if error: 
        st.error(error)
    else: 
        total_count = len(tasks)
        done_count = sum(1 for task in tasks if task['completed']==True)
        pending_count = total_count - done_count
        total, done, pending = st.columns(3)
        with total: 
            st.metric("Total", total_count)
        with done: 
            st.metric("Done",done_count)
        with pending: 
            st.metric("Pending", pending_count)
        
        df = pd.DataFrame(tasks)
        st.dataframe(df, width="stretch")
        chart_data = pd.DataFrame({
            "Status": ["Done", "Pending"],
            "Count": [done_count, pending_count]
        })
        st.bar_chart(chart_data.set_index("Status"))

# TODO: with tab_tasks:
#   - Add task form (POST to API or append to mock data)
#   - Task list with Complete buttons (PATCH to API or update mock)
#   - Error handling for API failures
with tab_task:
    st.subheader("Create New Task")
    with st.form("Create Tasks",clear_on_submit=True):
        title = st.text_input("Task Title")
        submitted = st.form_submit_button("Add Task")
        if submitted: 
            if not title.strip():
                st.error("Task title cannot be empty")
                st.stop()
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
        if tasks is None:
            tasks = []
    for task in tasks: 
        col1, col2 = st.columns([4, 1])
        with col1: 
            status = "✅" if task['completed'] else "⬜"
            st.write(f"{status} {task['title']}")
        with col2: 
            if not task['completed']: 
                if st.button("Complete", key=f"complete_{task['id']}"):
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
# ── TAB 3: AI Chat ────────────────────────────────────────────────────────
# TODO: with tab_chat:
#   - Render chat history (st.chat_message for each message)
#   - st.chat_input for user messages
#   - Mock response generator or real OpenAI call
#   - st.write_stream for streaming display
#   - Append both user and assistant messages to session state          
with tab_chat: 
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
        with st.spinner("Thinking..."):

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
                    
                    stream = client.messages.stream(
                        model="claude-3-5-sonnet-latest",
                        max_tokens=500,
                        system=system_prompt,
                        messages=[{"role": "user", "content": prompt}],
                    )

                    with stream as s:
                        for event in s:
                            if event.type == "content_block_delta":
                                streamed += event.delta.text
                                placeholder.write(streamed)
        
        st.session_state["messages"].append({
             "role": "assistant",
             "content": streamed
            })

        st.rerun()








