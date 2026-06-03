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
def retrieve(collection, query, n_results = 3):
    results = collection.query(
        query_texts=[query], 
        n_results = min(n_results, collection.count())
    )

    chunks = []
    for i in range(len(results['documents'][0])):
        chunks.append({
            "text": results['documents'][0][i],
            "metadata": results['metadatas'][0][i], 
            "distance": results['distances'][0][i],
        })
    return chunks



# Generate: Build a RAG prompt with retrieved context + system instructions, call Ollama, return the response
# Include these features:
# Source citation instructions in the system prompt
SYSTEM_PROMPT = (
    """You are a helpful AI assistant for students learning AI engineering.
Answer the user's question based ONLY on the context provided below.

Rules:
- Only use information from the CONTEXT section
- If the context doesn't contain the answer, say "I don't have enough information
  to answer that based on the available documents."
- Cite your sources by mentioning the document name in parentheses
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
    
# Display which chunks were retrieved before showing the answer

def rag_query(collection, question, n_results=3, stream=True):
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"\n{'='*60}")

    chunks = retrieve(collection, question, n_results)
    print(f"\n Retrieved {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f" [{i+1}] (dist: {chunk['distance']:.4f}) {chunk['metadata']['source']}")
    
    messages = build_messages(question, chunks)

    print(f"\nAnswer (streaming):\n")
    start = time.time()
    answer = generate(messages, stream=stream)
    elapsed = time.time() - start
    print(f"\n[Generated in {elapsed:.1f}s]")

    return answer

# An interactive loop (keep asking until the user types "quit")
if __name__=="__main__":
    client = chromadb.PersistentClient(path="./rag_db")
    collection = client.get_or_create_collection("course_docs")

    if collection.count() == 0: 
        count = ingest(collection, "docs")
        print(f"Ingested {count} document chunks.")
    else: 
        print(f"Using existing collection: {collection.count()} chunks")
    
    print("\\nRAG Pipeline Ready! Ask questions about your documents.")
    print("Type 'quit' to exit.\\n")

    while True:
        question = input("\\nYou: ").strip()
        if question.lower() in ('quit', 'exit', 'q'):
            break
        if question:
            rag_query(collection, question)

# Test with at least 3 questions:
# One that should be answerable from your documents
print(f"\n{'='*60}")

# One that’s related but not directly in the documents
# One that’s completely outside the scope