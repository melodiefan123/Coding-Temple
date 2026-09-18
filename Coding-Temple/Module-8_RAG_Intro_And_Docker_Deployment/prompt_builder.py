# Takes a user question and a list of retrieved document chunks (simulated)
import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("course_docs")

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

collection.add(
    documents=documents,
    metadatas=[{"source": s} for s in sources],
    ids=[f"doc_{i}" for i in range(len(documents))]
)
print(f"Knowledge base loaded: {collection.count()} document chunks\\n")

# Assembles a complete RAG prompt with:
# A system prompt instructing the model to answer from context only
# The retrieved chunks formatted with source labels
# The user’s question
# Instructions to cite sources
system_prompt = ("You are a helpful AI assistant for students learning AI engineering. "
    "Answer the user's question based ONLY on the context provided below. "
    "If the context doesn't contain enough information to answer, say so. "
    "Always cite which source document your answer comes from. "
    "Keep your response under 150 words.")
def rag_prompt(question: str, chunks,system_prompt=system_prompt):
    full_prompt = f""" SYSTEM: {system_prompt}

    CONTEXT: {chunks}

    USER QUESTION: {question}

    ANSWER: """
# Prints the assembled prompt and its token count estimate (characters / 4 as a rough approximation)
    token_count = len(full_prompt)//4
    print(f"Estimated token count: {token_count}")
    return full_prompt

# Tests with at least 2 different questions and different sets of "retrieved" chunks

user_questions = ["How do I protect my API endpoints so only logged-in users can access them?", "How does Docker help with deployment?"]

for user_question in user_questions:
    results = collection.query(
        query_texts=[user_question],
        n_results=3
    )
    context = "\n\n".join([
    f"[Source: {results['metadatas'][0][i]['source']}]\n{results['documents'][0][i]}" for i in range(len(results['documents'][0]))
])
    print(rag_prompt(user_question, chunks=context))
