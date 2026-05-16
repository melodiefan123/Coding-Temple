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
from mock_data import MOCK_TASKS, MOCK_STATS, MOCK_USER, MOCK_TOKEN
import api_client
import time

# ── Step 1: Page configuration ─────────────────────────────────────────────
# TODO: st.set_page_config(layout="wide", page_title="AI Dashboard", page_icon="🤖")

# ── Step 2: Session state initialisation ───────────────────────────────────
# TODO: Initialise all session state keys you will need:
#   "token"    → None
#   "username" → None
#   "messages" → []    (chat history)
#   "use_mock" → False (toggle to use mock data instead of the real API)

# ════════════════════════════════════════════════════════════════════════════
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
# SECTION B — SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
# TODO: with st.sidebar:
#   - App title and divider
#   - "Logged in as [username]"
#   - Logout button (clear token/username, st.rerun())
#   - AI Chat settings (API key input, system prompt)
#   - Divider and caption

# ════════════════════════════════════════════════════════════════════════════
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
