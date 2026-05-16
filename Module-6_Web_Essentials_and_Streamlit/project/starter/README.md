# Module 6 Project — AI Dashboard (Starter)

## Overview

Build a full-featured Streamlit dashboard that integrates everything from Module 6:
authentication, task management, data visualisation, and an AI chat interface.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) Start the FastAPI backend:
   ```bash
   pip install fastapi uvicorn
   uvicorn backend:app --reload --port 8000
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit app — your primary work file |
| `api_client.py` | Stub functions for backend communication |
| `mock_data.py` | Sample data for offline development |
| `requirements.txt` | Python dependencies |

## Requirements

See the project brief on the course platform for full requirements.
Key sections to implement:

1. **Authentication** — login form, JWT stored in session state, logout
2. **Dashboard** — metrics row (st.metric), dataframe, chart
3. **Task management** — add task form, complete task buttons
4. **AI Chat** — chat history, mock responses, streaming with st.write_stream
5. **Layout** — wide layout, sidebar controls, multiple tabs

## Tips

- Use `mock_data.py` to build and test the UI before the backend is ready.
- All API calls should go through `api_client.py`, not inline `requests` calls.
- Follow the session state pattern: initialise all keys before reading them.
