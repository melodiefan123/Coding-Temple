import os
import chromadb

# 1. Initialize Persistent ChromaDB Client
DB_PATH = "./chroma_demo"
client = chromadb.PersistentClient(path=DB_PATH)

# Get or create collection to allow re-runs
collection = client.get_or_create_collection(
    name="my_knowledge",
    metadata={"description": "AI Engineering Knowledge Base"}
)

# 2. Document Ingestion (Dynamic Data Structure)
documents = [
    {
        "id": "DOC001",
        "content": "REST APIs use standard HTTP methods like GET, POST, PUT, and DELETE to enable communication between client and server applications.",
        "metadata": {"module": "Backend Development", "topic": "api"}
    },
    {
        "id": "DOC002",
        "content": "GraphQL allows clients to request only the data they need, reducing over-fetching in modern web applications.",
        "metadata": {"module": "Backend Development", "topic": "api"}
    },
    {
        "id": "DOC003",
        "content": "JWT authentication provides a secure way to verify users through signed access tokens.",
        "metadata": {"module": "Security Fundamentals", "topic": "api"}
    },
    {
        "id": "DOC004",
        "content": "Relational databases organize data into tables connected through keys and relationships.",
        "metadata": {"module": "Database Systems", "topic": "database"}
    },
    {
        "id": "DOC005",
        "content": "Indexes improve SQL query performance by reducing the amount of data scanned during searches.",
        "metadata": {"module": "Database Systems", "topic": "database"}
    },
    {
        "id": "DOC006",
        "content": "NoSQL databases are optimized for flexible schemas and large-scale distributed applications.",
        "metadata": {"module": "Database Systems", "topic": "database"}
    },
    {
        "id": "DOC007",
        "content": "React components help developers build reusable and maintainable frontend interfaces.",
        "metadata": {"module": "Frontend Engineering", "topic": "frontend"}
    },
    {
        "id": "DOC008",
        "content": "CSS Flexbox simplifies the process of aligning and distributing elements within a webpage layout.",
        "metadata": {"module": "Frontend Engineering", "topic": "frontend"}
    },
    {
        "id": "DOC009",
        "content": "Responsive web design ensures applications display properly across desktop, tablet, and mobile devices.",
        "metadata": {"module": "Frontend Engineering", "topic": "frontend"}
    },
    {
        "id": "DOC010",
        "content": "State management libraries like Redux centralize application state for predictable frontend behavior.",
        "metadata": {"module": "Frontend Engineering", "topic": "frontend"}
    },
    {
        "id": "DOC011",
        "content": "Machine learning models learn patterns from training data to make predictions or classifications.",
        "metadata": {"module": "Artificial Intelligence", "topic": "ai"}
    },
    {
        "id": "DOC012",
        "content": "Natural language processing enables computers to understand and generate human language.",
        "metadata": {"module": "Artificial Intelligence", "topic": "ai"}
    },
    {
        "id": "DOC013",
        "content": "Neural networks are inspired by the structure of the human brain and are widely used in deep learning.",
        "metadata": {"module": "Artificial Intelligence", "topic": "ai"}
    },
    {
        "id": "DOC014",
        "content": "AI ethics focuses on fairness, accountability, and transparency in intelligent systems.",
        "metadata": {"module": "Artificial Intelligence", "topic": "ai"}
    },
    {
        "id": "DOC015",
        "content": "Database normalization reduces redundancy and improves data consistency within relational databases.",
        "metadata": {"module": "Database Systems", "topic": "database"}
    }
]

def load_documents(doc_list):
    """Upserts documents into ChromaDB with validation and basic error handling."""
    if not doc_list:
        print("Warning: No documents provided to load.")
        return

    try:
        collection.upsert(
            ids=[doc["id"] for doc in doc_list],
            documents=[doc["content"] for doc in doc_list],
            metadatas=[doc["metadata"] for doc in doc_list]
        )
        print(f"Successfully upserted {len(doc_list)} documents into 'my_knowledge'.")
    except Exception as e:
        print(f"Error during document ingestion: {e}")

load_documents(documents)

# 3. Robust Search Implementation
def search(query: str, module: str = None, top_k: int = 5):
    """
    Searches the knowledge base using semantic embeddings.
    Handles optional filtering, distance display, and count bounds safely.
    """
    print(f"\n=================== Search Query ===================")
    print(f"Query: '{query}' | Module Filter: {module or 'None'}")
    print("---------------------------------------------------")

    where_clause = {"module": module} if module else None

    # Check matching count before querying to avoid ChromaDB ValueError
    try:
        matched_items = collection.get(where=where_clause)
        total_matches = len(matched_items["ids"]) if matched_items and "ids" in matched_items else 0
    except Exception:
        total_matches = collection.count()

    if total_matches == 0:
        print("No matching documents found in the database.")
        return

    # Cap n_results to total available matching documents
    effective_k = min(top_k, total_matches)

    try:
        results = collection.query(
            query_texts=[query],
            n_results=effective_k,
            where=where_clause
        )
    except Exception as e:
        print(f"Query execution failed: {e}")
        return

    # Safely extract lists from ChromaDB query response
    ids = results.get("ids", [[]])[0]
    docs = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not docs:
        print("No matching documents returned.")
        return

    for i, (doc_id, doc, dist, meta) in enumerate(zip(ids, docs, distances, metadatas), start=1):
        print(f"{i}. [{doc_id}] (Distance: {dist:.4f})")
        print(f"   Module: {meta.get('module')} | Topic: {meta.get('topic')}")
        print(f"   Content: {doc}")

# 4. Test Queries Covering Required & Edge Cases
if __name__ == "__main__":
    print("\n--- Running Test Queries ---")

    # Test 1: Broad query without filters (matches top 5)
    search(query="web development and API design")

    # Test 2: Filtered query to a specific module with 4 matching docs
    search(query="UI layout and styling", module="Frontend Engineering")

    # Test 3: Filtered query to a module with only 1 matching doc (handles top_k > count)
    search(query="authentication tokens", module="Security Fundamentals")

    # Test 4: Completely different wording (semantic vector retrieval test)
    search(query="algorithms mimicking biological synaptic networks")

    # Test 5: Edge Case - Filter that matches zero documents
    search(query="data integrity", module="NonExistentModule")