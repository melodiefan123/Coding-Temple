import chromadb

# Initialize local in-memory ChromaDB client
client = chromadb.Client()
collection = client.get_or_create_collection("course_docs")

# Knowledge base setup
documents = [
    "FastAPI uses Pydantic models for automatic request validation. "
    "Define a Pydantic class with field types and FastAPI validates "
    "incoming data automatically, returning 422 errors for invalid requests.",

    "JWT (JSON Web Token) authentication in FastAPI works by creating "
    "a /auth/token endpoint that validates credentials and returns a "
    "signed token. Protected endpoints verify the token on each request.",

    "Streamlit session state persists data across re-runs using "
    "st.session_state. Initialize with: if 'key' not in st.session_state: "
    "st.session_state['key'] = default_value. Without this, all variables "
    "reset on every widget interaction.",

    "ChromaDB is a vector database that stores document embeddings for "
    "fast similarity search. It supports metadata filtering, persistent "
    "storage, and automatic embedding generation.",

    "CSS Flexbox arranges child elements in a row or column. Apply "
    "display: flex to the container, use gap for spacing, and "
    "flex-wrap: wrap for responsive layouts.",

    "Docker containers package an application with all its dependencies "
    "into a standardized unit. This ensures the application runs the "
    "same way on every machine, solving the 'works on my machine' problem.",
]

sources = [
    "module5_validation.md", "module5_auth.md", "module6_streamlit.md",
    "module7_chromadb.md", "module6_css.md", "module8_docker.md"
]

# Add documents and metadata to vector database
collection.add(
    documents=documents,
    metadatas=[{"source": s} for s in sources],
    ids=[f"doc_{i}" for i in range(len(documents))]
)
print(f"Knowledge base loaded: {collection.count()} document chunks\n")

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful AI assistant for students learning AI engineering.\n"
    "Answer the user's question based ONLY on the context provided below.\n"
    "If the context doesn't contain enough information to answer, say so.\n"
    "Always cite which source document your answer comes from.\n"
    "Keep your response under 150 words."
)

def rag_prompt(question: str, chunks: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
    """Assembles full RAG prompt and outputs estimated token length."""
    full_prompt = (
        f"SYSTEM:\n{system_prompt}\n\n"
        f"CONTEXT:\n{chunks}\n\n"
        f"USER QUESTION:\n{question}\n\n"
        f"ANSWER:"
    )
    
    # Estimate token count (~4 characters per token)
    token_count = len(full_prompt) // 4
    print(f"--- Prompt Assembled (Estimated Tokens: ~{token_count}) ---")
    return full_prompt

# Test with 2 different questions
user_questions = [
    "How do I protect my API endpoints so only logged-in users can access them?",
    "How does Docker help with deployment?"
]

for i, user_question in enumerate(user_questions, 1):
    results = collection.query(
        query_texts=[user_question],
        n_results=3
    )
    
    # Format retrieved document chunks with metadata labels
    formatted_chunks = "\n\n".join([
        f"[Source: {results['metadatas'][0][j]['source']}]\n{results['documents'][0][j]}"
        for j in range(len(results['documents'][0]))
    ])
    
    print(f"================ TEST CASE {i} ================")
    assembled_prompt = rag_prompt(user_question, chunks=formatted_chunks)
    print(assembled_prompt)
    print("\n" + "=" * 45 + "\n")