from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import chromadb
import requests
import json
import os

app = FastAPI(title="RAG API with Ollama and ChromaDB", version="1.0")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], 
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

#--- Config --- 
OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"
DB_PATH = "./rag_db"

#--- ChromaDB Setup ---
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("documents")

#---Schemas --- 
class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    n_results: int = 3
    max_distance: float = 1.2

class SourceChunk(BaseModel):
    text: str
    source: str
    distance: float

class AskResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    confidence: str

#---RAG Logic---
SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Answer ONLY from the provided context. "
    "If the context doesn't contain the answer, say you don't have enough "
    "information. Cite source documents. Keep responses under 200 words."
)

def retrieve(question: str, n_results: int, max_distance: float):
    if collection.count() == 0:
        return []
    results = collection.query(
        query_texts=[question],
        n_results=min(n_results, collection.count())
    )
    chunks = []
    for i in range(len(results['documents'][0])):
        dist = results['distances'][0][i]
        if dist <= max_distance:
            chunks.append(SourceChunk(
                text=results['documents'][0][i],
                source=results['metadatas'][0][i].get('source', 'unknown'),
                distance=round(dist, 4)
            ))
    return chunks

def get_confidence(chunks):
    if not chunks:
        return "none"
    best = chunks[0].distance
    if best < 0.5: return "high"
    if best < 1.0: return "medium"
    return "low"

def generate(messages):
    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat", json={
            "model": MODEL, "messages": messages, "stream": False
        })
        return r.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        raise HTTPException(503, "Ollama is not running")


# POST /ask - Accept a question, return a grounded answer with sources and confidence
@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    chunks = retrieve(request.question, request.n_results, request.max_distance)
    confidence = get_confidence(chunks)

    if not chunks:
        return AskResponse(
            answer="I don't have enough information to answer that based on the available documents.",
            sources=[],
            confidence="none"
        )

    context = "\n\n".join([f"[Source: {c.source}]\n{c.text}" for c in chunks])

    messages = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\nCONTEXT:\n{context}"},
        {"role": "user", "content": request.question}
    ]
    answer = generate(messages)
    return AskResponse(answer=answer, sources=chunks, confidence=confidence)

# POST /ingest - Load documents from the docs/ folder into ChromaDB

@app.post("/ingest")
def ingest():
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        raise HTTPException(400, "docs/ directory not found")
    
    chunks, ids, metadatas = [], [], []
    for filename in os.listdir(docs_dir):
        if not filename.endswith((".txt", ".md")):
            continue
        with open(os.path.join(docs_dir, filename), "r") as f:
            content = f.read()
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        for i, para in enumerate(paragraphs):
            chunks.append(para)
            ids.append(f"{filename}_{i}")
            metadatas.append({"source": filename, "chunk_index": str(i)})
        
    if chunks: 
        collection.upsert(documents=chunks, ids=ids, metadatas=metadatas)
    return {"message": f"Ingested {len(chunks)} chunks from {docs_dir}."}

# GET /stats - Return document count and model info
@app.get("/stats")
def stats():
    return{
        "document_count": collection.count(),
        "model": MODEL,
        "ollama_url": OLLAMA_URL
    }
# GET /health - Check if ChromaDB is accessible and Ollama is running
@app.get("/health")
def health():
    ollama_ok = False
    try: 
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout = 2)
        ollama_ok = r.status_code == 200
    except: 
        pass
    return {
        "chromadb": "ok", 
        "ollama": "ok" if ollama_ok else "unreachable",
        "documents": collection.count()
    }
# Include Pydantic schemas for all request/response models
# Add CORS middleware for frontend connectivity
# Handle these error cases:
# Ollama not running → 503 Service Unavailable
# No documents ingested → clear message in /ask response
# Invalid question (empty string) → 422 validation error via Pydantic
# Test all endpoints using Swagger UI at /docs