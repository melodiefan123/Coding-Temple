import streamlit as st
import requests
import os 

API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

st.set_page_config(page_title="LedgeAI - Ask RAG", page_icon="💬")
st.title("💬 Chat with your Documents & Receipts")

user_token = st.session_state.get("token")
if not user_token:
    st.warning("Please log in on the Authentication page to use the AI assistant.")
    st.stop()

headers = {"Authorization": f"Bearer {user_token}"}

# Document Upload Section
uploaded_file = st.file_uploader("Upload a Receipt / Invoice for RAG Indexing", type=["pdf", "png", "jpg", "txt"])

if uploaded_file and st.button("Index Document"):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    try: 
        res = requests.post(f"{API_URL}/rag/index", headers=headers, files=files, timeout=30)
        if res.status_code == 200:
            st.success("Document successfully indexed into vector store!")
        else:
            st.error("Failed to index document.")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to AI backend service: {e}")

st.divider()

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask something about your expenses or invoices..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI RAG Query endpoint
    with st.chat_message("assistant"):
        with st.spinner("Analyzing financial data..."):
            try: 
                res = requests.post(
                    f"{API_URL}/rag/query",
                    headers=headers,
                    json={"question": prompt}, 
                    timeout=30
                )
                if res.status_code == 200:
                    answer = res.json().get("answer", "No answer returned.")
                else:
                    answer = f"Error from RAG backend: {res.json().get('detail', res.text)}"
            except requests.exceptions.RequestException as e:
                answer = f"Could not connect to AI backend service: {e}"
            
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})