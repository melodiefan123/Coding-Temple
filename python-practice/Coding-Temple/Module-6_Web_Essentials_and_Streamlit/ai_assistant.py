# Chat interface using st.chat_message() and st.chat_input()
# Chat history stored in st.session_state and re-rendered on every run
# Sidebar with:
# A system prompt text area (editable personality for the AI)
# Context checkboxes (e.g., "Include Python expertise", "Include web development context", "Include AI/ML context") - when checked, these append relevant context to the system prompt
# A "Clear Chat" button that resets the history
# Loading indicator - show st.spinner("Thinking...") while generating a response
# Response generation - use a real API (OpenAI, Anthropic) if the student has a key, or a meaningful mock that references the prompt and selected context checkboxes
import streamlit as st
import time

st.set_page_config(page_title="AI Chat", page_icon="🤖", layout="centered")

if "messages" not in st.session_state: 
    st.session_state["messages"] = []

# --- Sidebar: Settings ---
with st.sidebar:
    st.title("Settings")
    system_prompt = st.text_input("System Prompt", value = "You are a helpful AI assistant for students learning AI engineering.", help="This sets the AI's personality and behavior.")
    python = st.checkbox("Include Python expertise")
    web_development = st.checkbox("Include web development context")
    ml = st.checkbox("Include AI/ML context")
    contexts = []
    if python: 
        system_prompt += "You have Python expertise"
        contexts.append("Python expertise")
    if web_development: 
        system_prompt += "You have web development context"
        contexts.append("web development context")
    if ml: 
        system_prompt += "You have AI/ML context"
        contexts.append("AI/ML context")

    if st.button("🗑️ Clear Chat"):
        st.session_state["messages"] = []
        st.rerun()
    
    if st.button("📋 Copy Conversation"):
        if st.session_state["messages"]:
            export_text = ""
            for msg in st.session_state["messages"]:
                role = "You" if msg["role"] == "user" else "AI"
                export_text += f"{role}: {msg['content']}\\n\\n"

            st.code(export_text, language=None)
            st.caption("Select all the text above and copy it (Cmd/Ctrl + C)")

            st.download_button( "💾 Download Chat", data=export_text ,file_name="chat_export.txt",mime="text/plain")
        else:
            st.info("No messages to export yet.")

    

#--Mock Response--
def mock_response(prompt, contexts):
    context_str = ", ".join(contexts) if contexts else "general knowledge"
    response = (f"Based on my {context_str} expertise, here's my take on "
                f"'{prompt[:40]}': [This would be a real AI response in production. "
                f"The system prompt and {len(contexts)} context areas would shape "
                f"how the AI responds.]")
    for word in response.split():
        yield word + " "
        time.sleep(0.03)
#--Main Chat --
st.title("AI Chat")

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state["messages"].append({"role": "user","content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            try:
                response = st.write_stream(mock_response(prompt, contexts))
            except Exception as e:
                    response = f"API Error: {str(e)}"
                    st.error(response)
        st.session_state["messages"].append({"role": "assistant", "content": response})
