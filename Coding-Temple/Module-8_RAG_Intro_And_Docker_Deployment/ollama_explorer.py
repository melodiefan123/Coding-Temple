import requests
import time
# Write a generate() helper function that calls Ollama’s /api/chat endpoint, measures response time, and returns the response text
OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"

def generate(prompt, system="You are a helpful assistant.", temperature=None):
    start = time.time()
    payload = {
    "model": MODEL,
    "messages": [   
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}],
        "stream": False
    }
    if temperature is not None:
        payload["temperature"] = temperature
    response = requests.post(f"{OLLAMA_URL}/api/chat", json=payload)

    elapsed = time.time() - start
    data = response.json()
    text = data["message"]["content"]
    return f"{text}\n [Generated in {elapsed:.1f}s]"


# Run these 4 experiments:
# Experiment 1: Same question, different system prompts

print(f"=====Experiment 1: No system prompt====")
print(generate("What is an API?", system=""))
print(f"\n=====Experiment 1: 5 Year Old Explanation====")
print(generate("What is an API?", system="explain like I'm 5 years old"))
print(f"\n=====Experiment 1: Senior SE Explanation====")
print(generate("What is an API?", system="You are a senior software architect. Be technical and precise."))
# Ask "What is an API?" with three different system prompts: (a) no system prompt, (b) "Explain like I’m 5 years old," (c) "You are a senior software architect. Be technical and precise."
# Compare how the responses differ
    #Responses correlate to the system prompt. Senior SE gives a more detailed and technical answer, while ELI5 gives a simpler explanation.



# Experiment 2: RAG-style context grounding
# Provide a short paragraph of context about a topic you choose
context = ("FastAPI is a modern python web framework. It uses Pydantic for validation and generates automatic API documentation at /docs.")
rag_system = ("Answer the user's question based ONLY on the following context. If the context doesn't contain the answer, say 'I don't have enough information to answer that'\n\n"
              f"CONTEXT: \n{context}")

# # Ask a question that CAN be answered from the context
print(f"====Experiment 2: question that can be answered from context====")
print(generate("What framework should I use to build a python API?", system=rag_system))
# Ask a question that CANNOT be answered from the context
print(f"\n===Experiment 2: Question that CANNOT be answered from context=== ")
print(generate("How do I deploy Kubernets", system=rag_system))
# Does the model correctly refuse the second question?
 #Model doesn't correctly refuse the second question, it tries to answer based on the context but ends up giving an incorrect answer about FastAPI instead of admitting it doesn't have enough information. Good note for the importance of clear system prompt instructions and testing edge cases. 

# # Experiment 3: Response timing

# Ask questions of varying length (short: 5 words, medium: 20 words, long: 50 words)
print(f"\n===Experiment 3: 5 Words Question=== ")
print(generate("What is API?"))
print(f"\n===Experiment 3: 20 Words Question=== ")
print(generate("Can you explain how FastAPI handles request validation and what happens when a user sends invalid data to an endpoint?"))
print(f"\n===Experiment 3: 50 Words Question=== ")
print(generate("Can you walk me through the complete lifecycle of an HTTP request in a FastAPI application, starting from when a client sends a POST request with JSON data, through Pydantic validation, route handler execution, database interaction, and finally how the response is serialized and returned to the client?"))
# Record and compare response times
    # Longer questions take more time to generate a response, but generates a more meaningful response. 


# Experiment 4: Temperature (optional)

# Add "temperature": 0.1 to one request and "temperature": 1.0 to another with the same prompt
print(f"\n===Experiment 4: 0.1 Temperature=== ")
print(generate("What is API?", temperature=0.1))

print(f"\n===Experiment 4: 1.0 Temperature=== ")
print(generate("What is API?", temperature=1.0))

# Compare how deterministic vs creative the responses are
 #The higher the temperature, the more creative and varied the response.
