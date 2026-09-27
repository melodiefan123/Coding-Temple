from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
import requests
from config import settings

app = FastAPI(title="RAG API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = chromadb.PersistentClient(path=settings.CHROMA_PATH)
collection = client.get_or_create_collection("documents")

class QuestionRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    ollama_ok = False
    try:
        r = requests.get(f"{settings.OLLAMA_URL}/api/tags", timeout=3)
        ollama_ok = r.status_code == 200
    except Exception:
        pass
    return {
        "status": "healthy",
        "ollama": "connected" if ollama_ok else "unavailable",
        "ollama_url": settings.OLLAMA_URL,
        "documents": collection.count()
    }

@app.get("/")
def root():
    return {"message": "RAG API running in Docker", "model": settings.MODEL_NAME}

@app.post("/ingest")
def ingest():
    sample_docs = [
        "Docker Compose is a tool for defining and running multi-container Docker applications.",
        "Streamlit turns data scripts into shareable web apps in minutes.",
        "FastAPI is a modern, fast web framework for building APIs with Python."
    ]
    sample_metadatas = [
        {"source": "docker_overview.txt"},
        {"source": "streamlit_overview.txt"},
        {"source": "fastapi_overview.txt"}
    ]
    sample_ids = ["doc1", "doc2", "doc3"]

    collection.add(
        documents=sample_docs,
        metadatas=sample_metadatas,
        ids=sample_ids
    )
    return {"message": "Documents indexed successfully", "count": collection.count()}

@app.post("/ask")
def ask(req: QuestionRequest):
    results = collection.query(query_texts=[req.question], n_results=settings.MAX_RESULTS)
    
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0] if results.get("distances") else [0.0] * len(docs)

    context = "\n".join(docs) if docs else "No context available."
    
    prompt = f"Context:\n{context}\n\nQuestion: {req.question}\nAnswer the question using only the context provided:"
    
    try:
        res = requests.post(
            f"{settings.OLLAMA_URL}/api/generate",
            json={"model": settings.MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=30
        )
        answer = res.json().get("response", "No response generated.")
    except Exception as e:
        answer = f"Error querying Ollama: {str(e)}"

    sources = [
        {"source": metas[i].get("source", "unknown"), "distance": float(distances[i]), "text": docs[i]}
        for i in range(len(docs))
    ]

    return {
        "answer": answer,
        "sources": sources,
        "confidence": "high" if docs else "low"
    }