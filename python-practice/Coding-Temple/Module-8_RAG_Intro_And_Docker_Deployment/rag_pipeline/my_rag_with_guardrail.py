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
        context_parts.append(f"[Source: {source}]\n{chunk['text']}")
    
    context = '\n---\n'.join(context_parts)
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
        }, stream=stream)

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
    
# Guardrail 4: Structured response
# Return responses as a dictionary with: answer, sources, confidence, chunks_retrieved
def rag_query(collection, question, n_results=3, stream=True):
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"\n{'='*60}")

    chunks = safe_retrieve(collection, question, n_results, max_distance=1.0)
    confidence, icon = get_confidence(chunks)
    print(f"\n Confidence: {icon} {confidence}")
    print(f"\n Retrieved {len(chunks)} chunks")

    for i, chunk in enumerate(chunks):
        print(f" [{i+1}] (dist: {chunk['distance']:.4f}) {chunk['metadata']['source']}")
    if confidence == "low":
        print(f"\nWarning: The retrieved information may not be very relevant to your question.")
    messages = build_messages(question, chunks)

    print(f"\nAnswer (streaming):\n")
    start = time.time()
    answer = generate(messages, stream=stream)
    elapsed = time.time() - start
    print(f"\n[Generated in {elapsed:.1f}s]")

    return {
        "answer": answer,
        "sources": [chunk['metadata']['source'] for chunk in chunks],
        "confidence": confidence,
        "chunks_retrieved": len(chunks)
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
    
    print("\nRAG Pipeline Ready! Ask questions about your documents.")
    print("Type 'quit' to exit.\n")
    # Test with 4 queries: one in-scope, one partially in-scope, one out-of-scope, and one ambiguous
# Print the structured response for each query

# Test 1 (answerable): "What is ChromaDB used for?" → correctly answered from module7_chromadb.txt
    print(f"\nTest 1: In-scope question")
    response1 = rag_query(collection, "What is ChromaDB used for?", stream=False)
    print(f"\nStructured Response:\n{json.dumps(response1, indent=2)}")
    # Test 2 (related but not in docs): "How does Pinecone compare to ChromaDB?" → said it didn't have enough info
    print(f"\nTest 2: Partially in-scope question")
    response2 = rag_query(collection, "How does Pinecone compare to ChromaDB?", stream=False)
    print(f"\nStructured Response:\n{json.dumps(response2, indent=2)}")
    # Test 3 (out of scope): "What is the best pizza recipe?" → correctly refused
    print(f"\nTest 3: Out-of-scope question")
    response3 = rag_query(collection, "What is the best pizza recipe?", stream=False)
    print(f"\nStructured Response:\n{json.dumps(response3, indent=2)}")
    # Test 4 (ambiguous): "What are the best practices for RAG?" → likely low confidence, may or may not answer based on retrieved chunks
    print(f"\nTest 4: Ambiguous question")
    response4 = rag_query(collection, "What are the best practices for RAG?", stream=False)
    print(f"\nStructured Response:\n{json.dumps(response4, indent=2)}")
    
    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ('quit', 'exit', 'q'):
            break
        if question:
            rag_query(collection, question)

