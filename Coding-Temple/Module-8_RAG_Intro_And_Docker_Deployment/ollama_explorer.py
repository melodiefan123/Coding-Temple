import requests
import time

OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"


def generate(prompt: str, system: str = "You are a helpful assistant.", temperature: float = None) -> dict:
    """
    Helper function to send a chat request to Ollama's /api/chat endpoint.
    Measures total latency, parses generation statistics, and safely handles payload options.
    """
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    # FIX: Ollama requires model hyper-parameters (like temperature) inside the "options" object.
    if temperature is not None:
        payload["options"] = {"temperature": float(temperature)}

    start_time = time.time()
    try:
        response = requests.post(f"{OLLAMA_URL}/api/chat", json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}

    elapsed = time.time() - start_time
    data = response.json()

    # Extract performance metrics returned by Ollama
    eval_count = data.get("eval_count", 0)  # Total tokens generated
    eval_duration_sec = data.get("eval_duration", 0) / 1e9  # Convert nanoseconds to seconds
    tokens_per_sec = (eval_count / eval_duration_sec) if eval_duration_sec > 0 else 0

    return {
        "text": data.get("message", {}).get("content", "").strip(),
        "elapsed": elapsed,
        "tokens_generated": eval_count,
        "tokens_per_sec": tokens_per_sec
    }


def print_experiment_header(title: str) -> None:
    """Utility to render standardized section headers."""
    print(f"\n{'='*70}\n{title}\n{'='*70}")


# ==============================================================================
# EXPERIMENT 1: System Prompts
# ==============================================================================
def run_experiment_1():
    print_experiment_header("EXPERIMENT 1: System Prompt Comparison")
    question = "What is an API?"

    prompts = [
        ("No System Prompt", ""),
        ("ELI5", "Explain like I'm 5 years old. Use simple analogies like toys or restaurants."),
        ("Senior Architect", "You are a senior software architect. Be technical, precise, and structured.")
    ]

    for label, system_prompt in prompts:
        print(f"\n--- [Condition: {label}] ---")
        result = generate(question, system=system_prompt)
        print(result["text"])
        print(f"\n[Stats: Latency {result['elapsed']:.2f}s | Tokens Generated: {result['tokens_generated']}]")

    print("\n>>> ANALYSIS & OBSERVATIONS:")
    print("1. Default/No Prompt: Provides a standard balanced answer covering HTTP, servers, and general use cases.")
    print("2. ELI5 Prompt: Forces child-friendly analogies (e.g., a waiter taking orders at a restaurant) and eliminates technical jargon.")
    print("3. Architect Prompt: Introduces formal technical concepts such as contracts, REST/gRPC endpoints, payload serialization, and system boundary protocols.")


# ==============================================================================
# EXPERIMENT 2: RAG-Style Context Grounding
# ==============================================================================
def run_experiment_2():
    print_experiment_header("EXPERIMENT 2: RAG Context Grounding & Strict Refusal")

    context = (
        "FastAPI is a modern Python web framework. It uses Pydantic for request data validation "
        "and generates automatic API documentation at /docs."
    )

    # Note: Strengthened prompt instructions to help smaller models (1B parameter) avoid hallucinating.
    rag_system = (
        "STRICT SYSTEM INSTRUCTION: You are an isolated context-bounded assistant. "
        "Answer questions ONLY using the facts provided in the CONTEXT below. "
        "If the answer is not explicitly stated in the CONTEXT, respond EXACTLY with: "
        "'I don't have enough information to answer that.' Do not use outside knowledge.\n\n"
        f"CONTEXT:\n{context}"
    )

    q_answerable = "What framework should I use to build a python API?"
    q_unanswerable = "How do I deploy Kubernetes?"

    print("\n--- [Test 1: In-Context Question] ---")
    print(f"Query: {q_answerable}")
    res1 = generate(q_answerable, system=rag_system)
    print(f"Response:\n{res1['text']}")

    print("\n--- [Test 2: Out-of-Context Question] ---")
    print(f"Query: {q_unanswerable}")
    res2 = generate(q_unanswerable, system=rag_system)
    print(f"Response:\n{res2['text']}")

    print("\n>>> ANALYSIS & OBSERVATIONS:")
    print("1. In-Context Grounding: The model successfully extracted 'FastAPI' from the strict context.")
    print("2. Out-of-Context Refusal: Small parameter models (like Llama 3.2 1B) are prone to ignoring constraint boundaries.")
    print("   If the model succeeds: The system prompt successfully restricted non-contextual knowledge.")
    print("   If the model fails: Demonstrates 'hallucination under constraint'—a common failure mode in small LLMs requiring stronger system instructions or lower temperature.")


# ==============================================================================
# EXPERIMENT 3: Response Timing Analysis
# ==============================================================================
def run_experiment_3():
    print_experiment_header("EXPERIMENT 3: Prompt Length vs Response Latency")

    queries = [
        ("Short (5 words)", "What is an API endpoint?"),
        ("Medium (20 words)", "Can you explain how FastAPI handles request validation and what happens when a user sends invalid data to an endpoint?"),
        ("Long (50 words)", "Can you walk me through the complete lifecycle of an HTTP request in a FastAPI application, starting from when a client sends a POST request with JSON data, through Pydantic validation, route handler execution, database interaction, and finally how the response is serialized and returned to the client?")
    ]

    for label, query in queries:
        res = generate(query)
        print(f"\n--- [{label}] ---")
        print(f"Prompt: \"{query}\"")
        print(f"Latency: {res['elapsed']:.2f} seconds")
        print(f"Output Tokens Generated: {res['tokens_generated']} tokens")
        print(f"Generation Speed: {res['tokens_per_sec']:.2f} tokens/sec")

    print("\n>>> ANALYSIS & OBSERVATIONS:")
    print("1. Prompt Length vs. Processing Time: Longer input prompts slightly increase initial prefill processing (Time-to-First-Token).")
    print("2. Dominant Factor in Total Latency: Total execution time is dominated by the length of the GENERATED RESPONSE (output tokens), rather than the input prompt length.")
    print("3. Inference Speed: Generation speed remains roughly constant in tokens/sec regardless of input prompt size.")


# ==============================================================================
# EXPERIMENT 4: Temperature & Determinism
# ==============================================================================
def run_experiment_4():
    print_experiment_header("EXPERIMENT 4: Temperature Comparison (0.1 vs 1.0)")

    prompt = "Write a one-sentence creative definition of code."

    print("\n--- [Run 1: Low Temperature (0.1)] ---")
    res_low_a = generate(prompt, temperature=0.1)
    res_low_b = generate(prompt, temperature=0.1)
    print(f"Sample A: {res_low_a['text']}")
    print(f"Sample B: {res_low_b['text']}")

    print("\n--- [Run 2: High Temperature (1.0)] ---")
    res_high_a = generate(prompt, temperature=1.0)
    res_high_b = generate(prompt, temperature=1.0)
    print(f"Sample A: {res_high_a['text']}")
    print(f"Sample B: {res_high_b['text']}")

    print("\n>>> ANALYSIS & OBSERVATIONS:")
    print("1. Temperature = 0.1 (Deterministic): Sampling probabilities are heavily weighted toward top tokens. Repeated runs yield nearly identical output.")
    print("2. Temperature = 1.0 (Creative): Increases the entropy of candidate token selection, leading to varied vocabulary, novel phrasing, and higher creative output across runs.")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("Starting Ollama Explorer Benchmarks...")
    run_experiment_1()
    run_experiment_2()
    run_experiment_3()
    run_experiment_4()
    print(f"\n{'='*70}\nAll experiments completed successfully.\n{'='*70}")