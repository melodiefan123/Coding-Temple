# For each of the 3 tasks below, write two prompts: a “bad” prompt (vague, no framing) and a “good” prompt (using at least 2 of the 3 techniques)

import os
# Task 1 — Code explanation:

# Get the model to explain what st.session_state does in Streamlit.

bad_prompt_1 = "Explain st.session_state"
good_prompt_1 = "You are an expert in creating a Streamlit application. You know what st.session_state does and how it functions with streamlit applications. Explain the function in detail. Answer in a normal conversation."

# Task 2 — Data formatting:

# Get the model to convert a natural language list of tasks into a JSON array with title, priority, and status fields.

bad_prompt_2 = "Convert a task list into a JSON array "
good_prompt_2 = "You are an expert in data formatting.Convert a natural language list of tasks, like I need to goto the grocery store to get ginger, garlic and rice, then I need to goto the bank to deposit some cash, into a JSON array with the following fields: title, priority, include(high/medium/low), and status(complete/pending/not yet started)"

# Task 3 — System prompt design:
# Write a system prompt for a "Course Study Assistant" that answers questions based on provided context from course notes. The system prompt should instruct the model to: use the provided context only, admit when it doesn’t know, keep answers under 150 words, and include which source document the answer came from.

bad_prompt_3 = "Design a system prompt"
system_prompt_3 = """You are a Course Study Assistant. 
Answer questions using only the provided context from course notes.
If you don't know the answer, say 'I don't know'.
Keep answers under 150 words.
Always cite which source document your answer came from."""

# Send both prompts to an API (or use the mock function from the Guided Example) and display the results side by side
def mock_response(prompt):
    prompt_lower = prompt.lower()

    has_role = any(word in prompt_lower for word in ["you are", "act as", "your role"])
    has_constraints = any(word in prompt_lower for word in
        ["under 100", "in 3 sentences", "as a table", "as json", "format", "bullet"])
    has_examples = "input:" in prompt_lower or "example:" in prompt_lower

    quality_score = sum([has_role, has_constraints, has_examples])

    if quality_score == 0:
        return ("[MOCK — Vague prompt detected]\\n"
                "Embeddings are a way to represent data as numbers. "
                "They are used in machine learning and NLP. "
                "There are many types of embeddings.\\n"
                "(This generic response demonstrates what happens with vague prompts.)")
    elif quality_score == 1:
        return ("[MOCK — Decent prompt]\\n"
                "Embeddings convert text into numerical vectors that capture semantic "
                "meaning. Think of it like a GPS coordinate for meaning — similar "
                "ideas get similar coordinates. This is how semantic search works: "
                "instead of matching keywords, you compare meaning vectors.\\n"
                "(Better — the prompt gave some direction.)")
    else:
        return ("[MOCK — Well-engineered prompt]\\n"
                "| Feature | Keyword Search | Semantic Search |\\n"
                "|---------|---------------|-----------------|\\n"
                "| Matching | Exact words | Meaning/intent |\\n"
                "| Handles synonyms | No | Yes |\\n"
                "| Requires | Word overlap | Embedding model |\\n\\n"
                "Think of keyword search like a librarian who only looks at book "
                "titles. Semantic search is a librarian who actually read every book "
                "and can recommend the right one even if you describe it differently.\\n"
                "(Excellent — role + constraints + format produced focused output.)")
print("---Task 1---")
print(f"\n Bad Prompt")
print(mock_response(bad_prompt_1))
print(f"\n Good Prompt")
print(mock_response(good_prompt_1))
print("---Task 2---")
print(f"\n Bad Prompt")
print(mock_response(bad_prompt_2))
print(f"\n Good Prompt")
print(mock_response(good_prompt_2))
print("---Task 3---")
print(f"\n Bad Prompt")
print(mock_response(bad_prompt_3))
print(f"\n Good Prompt")
print(mock_response(system_prompt_3))

    



