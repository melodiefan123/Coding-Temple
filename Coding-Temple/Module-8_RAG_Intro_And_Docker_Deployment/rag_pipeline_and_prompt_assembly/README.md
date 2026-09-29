# Retrieval-Augmented Generation (RAG) Architecture Pipeline

+----------------------------------------------------------------------------------------------------+
|                                              LEGEND                                                |
|  [ Input / Output ]      ( Data Processing Stage )      { Database / Storage }     ---> Data Flow  |
+----------------------------------------------------------------------------------------------------+

1. USER QUESTION INPUT
   +-------------------------------------------------------------------------------------------------+
   | Description : User enters a natural language query.                                             |
   | Technology  : User Interface / Client Application (e.g., Streamlit, React)                      |
   | Data Output : Raw Text String -> "How do I deploy a Flask app?"                                 |
   +-------------------------------------------------------------------------------------------------+
                                                  |
                                                  v  (Raw Question String)
2. QUERY EMBEDDING
   +-------------------------------------------------------------------------------------------------+
   | Description : Converts the user's plain text question into a high-dimensional dense vector.      |
   | Technology  : Embedding Model (e.g., SentenceTransformers / `all-MiniLM-L6-v2`)                  |
   | Data Output : Numerical Vector -> [0.21, -0.44, 0.82, ...] (384-dimensional array)               |
   +-------------------------------------------------------------------------------------------------+
                                                  |
                                                  v  (Dense Query Vector)
3. VECTOR DATABASE RETRIEVAL
   +-------------------------------------------------------------------------------------------------+
   | Description : Performs cosine similarity search (Nearest Neighbors) to fetch relevant chunks.   |
   | Technology  : Vector Database (e.g., ChromaDB with persistent HNSW index)                       |
   | Data Output : Top-K Text Chunks + Metadata -> [{"source": "module8.md", "text": "..."}]         |
   +-------------------------------------------------------------------------------------------------+
                                                  |
                                                  v  (Formatted Context Chunks)
4. PROMPT ASSEMBLY
   +-------------------------------------------------------------------------------------------------+
   | Description : Combines system directives, retrieved context with sources, and original question.|
   | Technology  : Prompt Engineering / Template Builder (`prompt_builder.py`)                       |
   | Data Output : Unified Prompt String -> SYSTEM + CONTEXT + USER QUESTION                         |
   +-------------------------------------------------------------------------------------------------+
                                                  |
                                                  v  (Full Assembled Prompt Text)
5. LLM GENERATION & RESPONSE
   +-------------------------------------------------------------------------------------------------+
   | Description : Processes assembled prompt and synthesizes a grounded answer with citations.      |
   | Technology  : Large Language Model (e.g., Ollama / Llama 3, OpenAI GPT-4o)                       |
   | Data Output : Final Answer String -> "Deploy Flask using Gunicorn... [Source: module8.md]"      |
   +-------------------------------------------------------------------------------------------------+