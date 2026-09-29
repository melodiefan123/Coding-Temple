import streamlit as st
import time

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Web & API Fundamentals Quiz",
    page_icon="🧠",
    layout="centered"
)

# --- 2. Session State Initialization ---
if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0

if "score" not in st.session_state:
    st.session_state["score"] = 0

if "answered" not in st.session_state:
    st.session_state["answered"] = False

if "selected_option" not in st.session_state:
    st.session_state["selected_option"] = None

if "question_start_time" not in st.session_state:
    st.session_state["question_start_time"] = time.time()

# --- 3. Questions Data ---
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
        "question": "Which CSS property controls the space outside an element's border?",
        "options": ["padding", "margin", "border", "spacing"],
        "answer": 1
    },
]

total_questions = len(questions)
time_limit = 15  # seconds per question

# --- 4. Main App Layout ---
st.title("🧠 Web & API Fundamentals Quiz")

# State 1: Quiz Completed (Results Screen)
if st.session_state["current_question"] >= total_questions:
    st.balloons()
    st.header("🎉 Quiz Complete!")
    
    score = st.session_state["score"]
    percentage = (score / total_questions) * 100
    
    st.metric(label="Final Score", value=f"{score} / {total_questions}", delta=f"{percentage:.0f}%")
    
    # Custom feedback summary based on performance
    if percentage == 100:
        st.success("🌟 Perfect score! Exceptional job mastering these core web concepts.")
    elif percentage >= 60:
        st.info("👍 Solid effort! You have a good grasp of the foundational topics.")
    else:
        st.warning("📚 Keep practicing! Review the concepts and try again.")
        
    if st.button("Restart Quiz", type="primary"):
        st.session_state["current_question"] = 0
        st.session_state["score"] = 0
        st.session_state["answered"] = False
        st.session_state["selected_option"] = None
        st.session_state["question_start_time"] = time.time()
        st.rerun()

# State 2: Active Quiz Question
else:
    q_index = st.session_state["current_question"]
    q = questions[q_index]

    # --- Progress Indicator (Placed above the question for better UX) ---
    st.caption(f"Question {q_index + 1} of {total_questions}")
    st.progress((q_index + 1) / total_questions)

    # --- Fragment-based Non-Blocking Live Countdown Timer ---
    @st.fragment(run_every=1)
    def render_timer():
        if not st.session_state["answered"]:
            elapsed = time.time() - st.session_state["question_start_time"]
            remaining = int(time_limit - elapsed)

            if remaining <= 0:
                st.session_state["answered"] = True
                st.session_state["selected_option"] = None
                st.rerun(scope="app")
            else:
                st.write(f"⏰ **Time Remaining:** `{remaining}` seconds")
        else:
            st.write("⏱️ **Timer paused** (Question answered)")

    render_timer()

    # --- Question Display & Form ---
    st.subheader(f"Q{q_index + 1}: {q['question']}")

    # Form keeps option selection stable during fragment interval re-renders
    with st.form(f"quiz_form_{q_index}"):
        user_choice = st.radio(
            "Select your answer:",
            options=q["options"],
            index=q["options"].index(st.session_state["selected_option"]) if st.session_state["selected_option"] in q["options"] else None,
            disabled=st.session_state["answered"]
        )
        
        submit_button = st.form_submit_button("Submit Answer", type="primary", disabled=st.session_state["answered"])

        if submit_button and not st.session_state["answered"]:
            if user_choice is None:
                st.warning("Please select an answer before submitting.")
            else:
                st.session_state["answered"] = True
                st.session_state["selected_option"] = user_choice
                
                correct_answer = q["options"][q["answer"]]
                if user_choice == correct_answer:
                    st.session_state["score"] += 1
                st.rerun()

    # --- Feedback and Next Step ---
    if st.session_state["answered"]:
        correct_answer = q["options"][q["answer"]]
        user_choice = st.session_state["selected_option"]

        if user_choice is None:
            st.error(f"⌛ **Time's up!** You didn't submit an answer in time. The correct answer was: **{correct_answer}**")
        elif user_choice == correct_answer:
            st.success("✅ **Correct!** Great job.")
        else:
            st.error(f"❌ **Incorrect.** The correct answer was: **{correct_answer}**")

        if st.button("Next Question ➡️", type="primary"):
            st.session_state["current_question"] += 1
            st.session_state["answered"] = False
            st.session_state["selected_option"] = None
            st.session_state["question_start_time"] = time.time()
            st.rerun()