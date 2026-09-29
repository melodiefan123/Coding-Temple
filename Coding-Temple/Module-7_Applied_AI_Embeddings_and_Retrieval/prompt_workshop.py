"""
prompt_workshop.py
Module Prompt Engineering Practice Exercise
"""

# =====================================================================
# TASK 1 — Code Explanation: st.session_state in Streamlit
# =====================================================================

bad_prompt_1 = "Explain st.session_state"

good_prompt_1 = """You are a senior Streamlit developer and technical instructor.

Explain what `st.session_state` is and why it is necessary in Streamlit applications.

Follow these rules:
1. Explain the concept using an everyday analogy (e.g., shopping cart, notebook).
2. Keep the explanation clear, beginner-friendly, and concise (under 120 words).
3. Do not include full code implementations, only a concise summary of its state-preservation mechanism.
"""


# =====================================================================
# TASK 2 — Data Formatting: Natural Language Tasks to JSON Array
# =====================================================================

bad_prompt_2 = "Convert a task list into a JSON array"

good_prompt_2 = """You are a data transformation API that strictly converts unstructured natural language tasks into structured JSON.

Convert the following task list into a valid JSON array of objects.

Schema requirements:
Each object must contain exactly three keys:
- "title": (string) summary of the action
- "priority": (string) high, medium, or low
- "status": (string) complete, pending, or not started

Example Input:
"I need to call mom tonight (high priority) and clean the kitchen (not urgent)."

Example Output:
[
  {"title": "Call mom", "priority": "high", "status": "pending"},
  {"title": "Clean the kitchen", "priority": "low", "status": "pending"}
]

Input Task List:
"I need to go to the grocery store to get ginger, garlic, and rice (urgent). Then I need to go to the bank to deposit cash (medium priority), and finally read 10 pages of my book."
"""


# =====================================================================
# TASK 3 — System Prompt Design: Course Study Assistant
# =====================================================================

# System prompt meeting all 4 required constraints:
# 1. Use provided context only
# 2. Admit when it doesn't know
# 3. Keep answers under 150 words
# 4. Include source document reference
system_prompt_3 = """You are a Course Study Assistant. Your goal is to accurately answer student questions using ONLY the provided course notes context.

Rules:
1. Rely EXCLUSIVELY on the provided context. Do NOT use outside knowledge or assumptions.
2. If the context does not contain enough information to answer the question, respond strictly with: "I don't know based on the provided notes."
3. Keep all answers under 150 words.
4. Always cite the source document name (e.g., [Source: doc_name.md]) at the end of your response.
"""

bad_prompt_3 = "Design a system prompt for study assistant"

good_prompt_3 = f"""[System Prompt]:
{system_prompt_3}

[Context Document]:
Doc_Name: Lecture_04_State Management.md
Content: Streamlit reruns the entire Python script from top to bottom every time a user interacts with a widget. Because of this execution model, standard Python variables are reset on every rerun. `st.session_state` provides a dictionary-like stateful memory that persists user interaction variables across script reruns.

[User Question]:
Why do standard Python variables reset in Streamlit, and how does session state help?
"""


# =====================================================================
# DYNAMIC MOCK FUNCTION (Task & Quality Aware)
# =====================================================================

def mock_response(prompt: str) -> str:
    prompt_lower = prompt.lower()
    
    # Task 1: st.session_state
    if "session_state" in prompt_lower or "explain st" in prompt_lower:
        is_engineered = len(prompt) > 80 and ("role" in prompt_lower or "developer" in prompt_lower or "analogy" in prompt_lower)
        if not is_engineered:
            return (
                "[MOCK OUTPUT — Vague Prompt]\n"
                "st.session_state is a feature in Streamlit used to store state. "
                "It works like a dictionary in Python. You can store key-value pairs in it."
            )
        else:
            return (
                "[MOCK OUTPUT — Well-Engineered Prompt]\n"
                "Think of Streamlit like a waiter who forgets who you are every time they leave the table—every "
                "user click reruns the entire script from top to bottom, resetting standard variables.\n\n"
                "`st.session_state` acts like a notepad the waiter keeps in their pocket. It preserves key-value "
                "data (like user login status or shopping cart items) across script reruns, allowing your web app "
                "to retain memory between interactions without restarting from scratch."
            )

    # Task 2: Data Formatting / JSON
    elif "json" in prompt_lower or "grocery store" in prompt_lower:
        is_engineered = "example" in prompt_lower or "schema" in prompt_lower
        if not is_engineered:
            return (
                "[MOCK OUTPUT — Vague Prompt]\n"
                "Here is the task list in JSON format:\n"
                "Task 1: Go to grocery store\n"
                "Task 2: Bank deposit\n"
                "(Failed to return raw JSON array or follow priority/status fields)."
            )
        else:
            return (
                "[MOCK OUTPUT — Well-Engineered Prompt]\n"
                "[\n"
                '  {"title": "Go to grocery store for ginger, garlic, and rice", "priority": "high", "status": "pending"},\n'
                '  {"title": "Deposit cash at the bank", "priority": "medium", "status": "pending"},\n'
                '  {"title": "Read 10 pages of book", "priority": "low", "status": "pending"}\n'
                "]"
            )

    # Task 3: System Prompt / Course Assistant
    elif "system prompt" in prompt_lower or "course study assistant" in prompt_lower:
        is_engineered = "lecture_04" in prompt_lower or "rules:" in prompt_lower
        if not is_engineered:
            return (
                "[MOCK OUTPUT — Vague Prompt]\n"
                "You should act as a study assistant and answer questions about course notes clearly and helpfully."
            )
        else:
            return (
                "[MOCK OUTPUT — System Prompt Execution Test]\n"
                "Standard Python variables reset because Streamlit reruns the entire Python script from top to bottom "
                "every time a user interacts with a widget. `st.session_state` helps by providing a persistent, "
                "dictionary-like memory that retains variable values across these reruns.\n\n"
                "[Source: Lecture_04_State Management.md]\n"
                "(Word count: 42 words | Fully constrained to provided context)"
            )

    # Generic Fallback
    return "[MOCK OUTPUT] Unrecognized prompt category."


# =====================================================================
# DISPLAY OUTPUTS
# =====================================================================

if __name__ == "__main__":
    print("=====================================================================")
    print("TASK 1 — CODE EXPLANATION: st.session_state")
    print("=====================================================================")
    print("\n--- BAD PROMPT ---")
    print(bad_prompt_1)
    print("\n--- RESPONSE ---")
    print(mock_response(bad_prompt_1))
    
    print("\n" + "-"*50)
    print("\n--- GOOD PROMPT ---")
    print(good_prompt_1)
    print("\n--- RESPONSE ---")
    print(mock_response(good_prompt_1))

    print("\n\n=====================================================================")
    print("TASK 2 — DATA FORMATTING: Natural Language to JSON")
    print("=====================================================================")
    print("\n--- BAD PROMPT ---")
    print(bad_prompt_2)
    print("\n--- RESPONSE ---")
    print(mock_response(bad_prompt_2))
    
    print("\n" + "-"*50)
    print("\n--- GOOD PROMPT ---")
    print(good_prompt_2)
    print("\n--- RESPONSE ---")
    print(mock_response(good_prompt_2))

    print("\n\n=====================================================================")
    print("TASK 3 — SYSTEM PROMPT DESIGN: Course Study Assistant")
    print("=====================================================================")
    print("\n--- BAD PROMPT ---")
    print(bad_prompt_3)
    print("\n--- RESPONSE ---")
    print(mock_response(bad_prompt_3))
    
    print("\n" + "-"*50)
    print("\n--- SYSTEM PROMPT & EXECUTION TEST ---")
    print(f"Written System Prompt:\n{system_prompt_3}")
    print("-" * 30)
    print(f"Good Prompt Input:\n{good_prompt_3}")
    print("\n--- RESPONSE ---")
    print(mock_response(good_prompt_3))
    print("=====================================================================")