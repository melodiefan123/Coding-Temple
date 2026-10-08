import chromadb
import requests
import json 
import os 
import time 

OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.2:1b"

# Ingest: Load documents, chunk by paragraphs, store in persistent ChromaDB
def load_documents(directory):
    docs = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(('.txt', '.md')):
            with open(os.path.join(directory, filename), 'r') as f: 
                content = f.read()
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            for i, para in enumerate(paragraphs):
                docs.append({
                    "text": para, 
                    "id": f"{filename}_{i}",
                    "metadata": {"source": filename}
                })
    return docs

def ingest(collection, docs_directory):
    chunks = load_documents(docs_directory)
    if not chunks:
        print("No documents found!")
        return 0 
    
    collection.upsert(
        documents = [c["text"] for c in chunks], 
        metadatas = [c["metadata"] for c in chunks], 
        ids = [c["id"] for c in chunks]
    )
    return len(chunks)
# Retrieve: Query ChromaDB with a user question, return top 3 chunks
# Guardrail 1: Distance threshold filtering
# Only send chunks with distance below a configurable threshold (start with 1.0)
# If no chunks pass the filter, return a "no relevant information" response
def safe_retrieve(collection, query, n_results = 3, max_distance = 1.0):
    if collection.count() == 0:
        print("No documents in collection.")
        return []
    
    results = collection.query(
        query_texts=[query], 
        n_results = min(n_results, collection.count())
        )

    filtered_chunks = []
    for i in range(len(results['documents'][0])):
        dist = results['distances'][0][i]
        if dist <= max_distance:
            filtered_chunks.append({
                "text": results['documents'][0][i],
                "metadata": results['metadatas'][0][i], 
                "distance": dist,
                })
    if not filtered_chunks:
        print("No relevant information found in the documents.")
    return filtered_chunks

# Guardrail 2: Confidence levels
# Return a confidence level with each response: "high" (best distance < 0.5), "medium" (< 1.0), "low" (>= 1.0)
def get_confidence(chunks):
    if not chunks: 
        return "none", "🔴"
    best_distance = chunks[0]['distance']
    if best_distance < 0.5:
        return "high", "🟢"
    elif best_distance < 1.0:
        return "medium", "🟡"
    else:
        return "low", "🔴"

# Guardrail 3: Strengthened system prompt
# Add explicit guardrail instructions: never make up information, say "I don’t know" when unsure, always cite sources 
SYSTEM_PROMPT = (
    """You are a helpful AI assistant for students learning AI engineering.
Answer the user's question based ONLY on the context provided below.

Rules:
- Only use information from the CONTEXT section
- If the context doesn't contain the answer, say "I don't have enough information
  to answer that based on the available documents."
- Cite your sources by mentioning the document name in parentheses
- Never make up information. If you don't know, say you don't know.
"""
)
def build_messages(question, retrieved_chunks):
    context_parts = []
    for chunk in retrieved_chunks:
        source = chunk['metadata']['source']
        context_parts.append(f"[Document: {source}]\n{chunk['text']}")
    
    context = '\n---\n'.join(context_parts) if context_parts else "NO RELEVANT CONTEXT FOUND."
    system_with_context = f"{SYSTEM_PROMPT}\nCONTEXT:\n{context}"

    return [
        {"role": "system", "content": system_with_context}, 
        {"role": "user", "content": question}
    ]
def generate(messages, stream = False):
    try: 
        response = requests.post(f"{OLLAMA_URL}/api/chat", json={
            "model": MODEL, 
            "messages": messages, 
            "stream": stream
        }, stream=stream, timeout=30)

        if stream: 
            full_response = ""
            for line in response.iter_lines():
                if line: 
                    data = json.loads(line)
                    token = data.get("message", {}).get("content", "")
                    if token: 
                        print(token, end="", flush=True) #Print as they arrive
                        full_response += token 
            print()
            return full_response
        else: 
            return response.json()["message"]["content"]
    # Handle the case where Ollama isn’t running (graceful error message)
    except requests.exceptions.ConnectionError: 
        return "ERROR: Cannot connect to Ollama. Is it running? (ollama serve)"
    except Exception as e: 
        return f"ERROR: {str(e)}"
    
# Guardrail 4: Structured response
# Return responses as a dictionary with: answer, sources, confidence, chunks_retrieved
def rag_query(collection, question, n_results=3, stream=False, verbose = True):
    start = time.time()
    chunks = safe_retrieve(collection, question, n_results, max_distance=1.0)
    confidence, icon = get_confidence(chunks)
    if not chunks:
        answer = "I don't have enough information to answer that based on the available documents."
    else:
        messages = build_messages(question, chunks)
        answer = generate(messages, stream=stream)

    elapsed = time.time() - start
    sources = list(set([c['metadata']['source'] for c in chunks]))

    if verbose:
        print(f"\n{'='*60}\nQuestion: {question}\n{'='*60}")
        print(f"Confidence: {icon} {confidence} | Retrieved {len(chunks)} chunks in {elapsed:.2f}s")
        for i, c in enumerate(chunks):
            print(f"  [{i+1}] (dist: {c['distance']:.4f}) Source: {c['metadata']['source']}")
        print(f"\nAnswer:\n{answer}\n")

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "best_distance": chunks[0]['distance'] if chunks else None,
        "chunks_retrieved": len(chunks),
        "latency_seconds": round(elapsed, 2)
    }
# An interactive loop (keep asking until the user types "quit")
if __name__=="__main__":
    client = chromadb.PersistentClient(path="./rag_db")
    collection = client.get_or_create_collection("course_docs")

    if collection.count() == 0: 
        count = ingest(collection, "docs")
        print(f"Ingested {count} document chunks.")
    else: 
        print(f"Using existing collection: {collection.count()} chunks")

    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ('quit', 'exit', 'q'):
            break
        if question:
            rag_query(collection, question)

