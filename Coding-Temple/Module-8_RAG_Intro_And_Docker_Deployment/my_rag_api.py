from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import chromadb
import requests
import os

app = FastAPI(
    title="RAG API with Ollama and ChromaDB", 
    description="A production-ready RAG API featuring ChromaDB vector storage and local LLM generation via Ollama.",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# --- Config --- 
OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"
DB_PATH = "./rag_db"

# --- ChromaDB Setup ---
try: 
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection("documents")
except Exception: 
    collection = None

# --- Schemas --- 
class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The query string to search and answer.")
    n_results: int = Field(default=3, ge=1, le=10, description="Number of context chunks to retrieve.")
    max_distance: float = Field(default=1.2, gt=0, description="Maximum vector distance threshold.")

    @field_validator("question")
    @classmethod
    def validate_question_not_empty(cls, value: str) -> str: 
        if not value.strip(): 
            raise ValueError("Question cannot be empty or consist solely of whitespace.")
        return value.strip()


class SourceChunk(BaseModel):
    text: str = Field(..., description="Retrieved chunk content.")
    source: str = Field(..., description="Source filename.")
    distance: float = Field(..., description="Vector distance metric.")


class AskResponse(BaseModel):
    answer: str = Field(..., description="Grounded answer produced by LLM.")
    sources: list[SourceChunk] = Field(default=[], description="List of source document chunks used.")
    confidence: str = Field(..., description="Confidence assessment: high, medium, low, or none.")


class IngestResponse(BaseModel):
    message: str = Field(..., description="Summary of the ingestion result.")
    chunks_ingested: int = Field(..., description="Total count of text chunks indexed.")


class StatsResponse(BaseModel):
    document_count: int = Field(..., description="Total chunks currently stored in ChromaDB.")
    model: str = Field(..., description="Ollama model configured.")
    ollama_url: str = Field(..., description="Ollama instance endpoint.")


class HealthResponse(BaseModel): 
    chromadb: str = Field(..., description="Status of ChromaDB vector store connection.")
    ollama: str = Field(..., description="Status of Ollama service connection.")
    documents: int = Field(..., description="Current stored document count.")


# --- Helpers ---
def check_ollama_alive() -> bool: 
    try: 
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return r.status_code == 200
    except requests.RequestException: 
        return False


def retrieve(question: str, n_results: int, max_distance: float):
    if collection is None or collection.count() == 0:
        return []
    results = collection.query(
        query_texts=[question],
        n_results=min(n_results, collection.count())
    )
    chunks = []
    if results and results.get('documents') and len(results['documents']) > 0:
        for i in range(len(results['documents'][0])):
            dist = results['distances'][0][i]
            if dist <= max_distance:
                chunks.append(SourceChunk(
                    text=results['documents'][0][i],
                    source=results['metadatas'][0][i].get('source', 'unknown'),
                    distance=round(dist, 4)
                ))
    return chunks


def get_confidence(chunks: list[SourceChunk]) -> str:
    if not chunks:
        return "none"
    best = chunks[0].distance
    if best < 0.5: 
        return "high"
    if best < 1.0: 
        return "medium"
    return "low"


def generate(messages: list) -> str:
    if not check_ollama_alive(): 
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Ollama is not running or unreachable"
        )
    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat", json={
            "model": MODEL, "messages": messages, "stream": False
        }, timeout=30)
        r.raise_for_status()
        return r.json()["message"]["content"]
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Ollama is not running or unreachable"
        )


# --- Endpoints ---

@app.post(
    "/ask", 
    response_model=AskResponse, 
    summary="Submit a query to the RAG pipeline", 
    responses={
        200: {"description": "Successful retrieval and generation."},
        422: {"description": "Validation error (e.g., empty or invalid question)."},
        503: {"description": "Ollama service unavailable."}
    }
)
def ask(request: AskRequest):
    chunks = retrieve(request.question, request.n_results, request.max_distance)
    confidence = get_confidence(chunks)

    if not chunks:
        return AskResponse(
            answer="I don't have enough information to answer that based on the available documents.",
            sources=[],
            confidence="none"
        )

    SYSTEM_PROMPT = (
        "You are a helpful AI assistant. Answer ONLY from the provided context. "
        "If the context doesn't contain the answer, say you don't have enough "
        "information. Cite source documents. Keep responses under 200 words."
    )

    # Added so the LLM can cite sources properly
    context = "\n\n".join([f"\n{c.text}" for c in chunks])

    messages = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\nCONTEXT:\n{context}"},
        {"role": "user", "content": request.question}
    ]
    answer = generate(messages)
    return AskResponse(answer=answer, sources=chunks, confidence=confidence)


@app.post(
    "/ingest", 
    response_model=IngestResponse, 
    summary="Ingest text and markdown documents from docs/ into ChromaDB", 
    responses={
        200: {"description": "Documents successfully processed."},
        400: {"description": "docs/ directory missing or unreadable."},
        500: {"description": "ChromaDB connection unavailable."}
    }
)
def ingest():
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ChromaDB collection is inaccessible"
        )

    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="docs/ directory not found"
        )
    
    chunks, ids, metadatas = [], [], []
    for filename in os.listdir(docs_dir):
        if not filename.endswith((".txt", ".md")):
            continue
        filepath = os.path.join(docs_dir, filename)
        if not os.path.isfile(filepath):
            continue

        try: 
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
            for i, para in enumerate(paragraphs):
                chunks.append(para)
                ids.append(f"{filename}_{i}")
                metadatas.append({"source": filename, "chunk_index": str(i)})
        except Exception as e: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Error reading file {filename}: {str(e)}"
            )
        
    if chunks: 
        collection.upsert(documents=chunks, ids=ids, metadatas=metadatas)

    return IngestResponse(
        message=f"Ingested {len(chunks)} chunks from {docs_dir}.",
        chunks_ingested=len(chunks)
    )


@app.get(
    "/stats", 
    response_model=StatsResponse, 
    summary="Retrieve collection stats and model configuration", 
    responses={
        500: {"description": "Database connection error."}
    }
)
def stats():
    if collection is None: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="ChromaDB collection is inaccessible"
        )
    return StatsResponse(
        document_count=collection.count(),
        model=MODEL, 
        ollama_url=OLLAMA_URL
    )


@app.get(
    "/health", 
    response_model=HealthResponse, 
    summary="Verify operational state of ChromaDB and Ollama", 
    responses={
        200: {"description": "All dependencies are healthy."},
        503: {"description": "Ollama or ChromaDB service unavailable."}
    }
)
def health():
    ollama_ok = check_ollama_alive()
    
    chroma_ok = False
    doc_count = -1
    if collection is not None:
        try:
            doc_count = collection.count()
            chroma_ok = True
        except Exception:
            chroma_ok = False

    if not ollama_ok or not chroma_ok: 
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Ollama or ChromaDB service is unreachable"
        )

    return HealthResponse(
        chromadb="ok",
        ollama="ok", 
        documents=doc_count
    )