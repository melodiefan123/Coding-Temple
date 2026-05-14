# 5 hardcoded questions with multiple-choice answers (use topics from this course - HTML, CSS, JavaScript, Python, APIs)
# Session state tracking:
    # current_question (index of the current question)
    # score (number of correct answers)
    # answered (whether the current question has been answered)
#Answer flow: When the user selects an answer and clicks Submit:
    # Show whether they were correct or incorrect (using st.success() or st.error())
    # Show the correct answer if they were wrong
    # Show a "Next" button to advance
#Progress indicator: "Question 2 of 5" and a progress bar
#Results screen: After the last question, show the final score and a "Restart" button that resets all session state

import streamlit as st

# st.set_page_config() with layout="wide" and a relevant title/icon
st.set_page_config(
    page_title="My Dashboard",      # Browser tab title
    page_icon="📊",                 # Browser tab icon
    layout="wide",                  # Use full browser width (default is "centered")
    initial_sidebar_state="expanded" # Sidebar starts open
)

#----Initialize Session State --- 
if "current_question" not in st.session_state: 
    st.session_state["current_question"] = 0 

if "score" not in st.session_state: 
    st.session_state["score"] = 0 

if "answered" not in st.session_state: 
    st.session_state["answered"] = False

questions = [
    {
        "question": "What does HTML stand for?",
        "options": ["Hyper Text Markup Language", "High Tech Modern Language",
                    "Hyper Transfer Markup Language", "Home Tool Markup Language"],
        "answer": 0
    },
    {
        "question": "Which Python keyword is used to define a function?",
        "options": ["func", "define", "def", "function"],
        "answer": 2
    },
    {
        "question": "What HTTP method is used to send data to an API to create a new resource?",
        "options": ["GET", "DELETE", "PATCH", "POST"],
        "answer": 3
    },
    {
        "question": "Which JavaScript method is used to filter an array?",
        "options": [".map()", ".filter()", ".reduce()", ".find()"],
        "answer": 1
    },
    {
        "question": "Which CSS property controls the space between elements?",
        "options": ["padding", "margin", "border", "spacing"],
        "answer": 1
    },
]

if st.session_state["current_question"] >= len(questions):
    st.write(f"Final Score:{st.session_state['score']} ")
    restart = st.button("Restart")
    if restart: 
        st.session_state["current_question"] = 0 
        st.session_state["score"] = 0 
        st.session_state['answered'] = False
else: 
    q = questions[st.session_state["current_question"]]

    with st.form("quiz_form", clear_on_submit=True):
        title = st.write(q["question"])
        options = st.selectbox("Options", q["options"])
        submit = st.form_submit_button("Submit")
        if submit: 
            if q["options"][q["answer"]] == options:
                st.session_state["answered"] = True
                st.session_state["score"] += 1
                st.success("Correct! Move to the next question.")
            else:
                st.session_state["answered"] = True
                st.error("Wrong answer.")
                st.write(f"Correct answer is {q['options'][q['answer']]}")
    next = st.button("Next")
    if next and st.session_state['answered'] == True:
        st.session_state["current_question"] += 1
        st.session_state['answered'] = False

    st.write(f"Question {st.session_state['current_question'] + 1} of {len(questions)}")
    st.progress((st.session_state['current_question'] + 1)/len(questions))
