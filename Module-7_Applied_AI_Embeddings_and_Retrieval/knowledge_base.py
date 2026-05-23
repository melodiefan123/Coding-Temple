import chromadb
# Create a persistent ChromaDB client (data survives restarts)
client = chromadb.PersistentClient(path="./chroma_demo")

# Create a collection called "my_knowledge"
collection = client.get_or_create_collection(
    name="my_knowledge",
    metadata={"description": "AI Engineering Knowledge Base"}
)
# Add at least 15 documents covering content from at least 3 different modules you’ve completed. Each document should include:
# A unique ID
# The text content (a sentence or short paragraph summarizing a concept)
# Metadata with at least: module (which module it’s from) and topic (general category like "api", "database", "frontend", "ai")

documents = [
  {
    "id": "DOC001",
    "content": "REST APIs use standard HTTP methods like GET, POST, PUT, and DELETE to enable communication between client and server applications.",
    "metadata": {
      "module": "Backend Development",
      "topic": "api"
    }
  },
  {
    "id": "DOC002",
    "content": "GraphQL allows clients to request only the data they need, reducing over-fetching in modern web applications.",
    "metadata": {
      "module": "Backend Development",
      "topic": "api"
    }
  },
  {
    "id": "DOC003",
    "content": "JWT authentication provides a secure way to verify users through signed access tokens.",
    "metadata": {
      "module": "Security Fundamentals",
      "topic": "api"
    }
  },
  {
    "id": "DOC004",
    "content": "Relational databases organize data into tables connected through keys and relationships.",
    "metadata": {
      "module": "Database Systems",
      "topic": "database"
    }
  },
  {
    "id": "DOC005",
    "content": "Indexes improve SQL query performance by reducing the amount of data scanned during searches.",
    "metadata": {
      "module": "Database Systems",
      "topic": "database"
    }
  },
  {
    "id": "DOC006",
    "content": "NoSQL databases are optimized for flexible schemas and large-scale distributed applications.",
    "metadata": {
      "module": "Database Systems",
      "topic": "database"
    }
  },
  {
    "id": "DOC007",
    "content": "React components help developers build reusable and maintainable frontend interfaces.",
    "metadata": {
      "module": "Frontend Engineering",
      "topic": "frontend"
    }
  },
  {
    "id": "DOC008",
    "content": "CSS Flexbox simplifies the process of aligning and distributing elements within a webpage layout.",
    "metadata": {
      "module": "Frontend Engineering",
      "topic": "frontend"
    }
  },
  {
    "id": "DOC009",
    "content": "Responsive web design ensures applications display properly across desktop, tablet, and mobile devices.",
    "metadata": {
      "module": "Frontend Engineering",
      "topic": "frontend"
    }
  },
  {
    "id": "DOC010",
    "content": "State management libraries like Redux centralize application state for predictable frontend behavior.",
    "metadata": {
      "module": "Frontend Engineering",
      "topic": "frontend"
    }
  },
  {
    "id": "DOC011",
    "content": "Machine learning models learn patterns from training data to make predictions or classifications.",
    "metadata": {
      "module": "Artificial Intelligence",
      "topic": "ai"
    }
  },
  {
    "id": "DOC012",
    "content": "Natural language processing enables computers to understand and generate human language.",
    "metadata": {
      "module": "Artificial Intelligence",
      "topic": "ai"
    }
  },
  {
    "id": "DOC013",
    "content": "Neural networks are inspired by the structure of the human brain and are widely used in deep learning.",
    "metadata": {
      "module": "Artificial Intelligence",
      "topic": "ai"
    }
  },
  {
    "id": "DOC014",
    "content": "AI ethics focuses on fairness, accountability, and transparency in intelligent systems.",
    "metadata": {
      "module": "Artificial Intelligence",
      "topic": "ai"
    }
  },
  {
    "id": "DOC015",
    "content": "Database normalization reduces redundancy and improves data consistency within relational databases.",
    "metadata": {
      "module": "Database Systems",
      "topic": "database"
    }
  }
]

collection.upsert(
    ids = [doc["id"] for doc in documents], 
    documents = [doc['content'] for doc in documents], 
    metadatas=[doc['metadata'] for doc in documents])
# Implement a search function that:
# Accepts a query string and an optional module filter
# Returns the top 5 results with distances and metadata
def search(query, module=None):
    if module:
        results = collection.query(
            query_texts=[query],
            n_results = 5, 
            where={"module": module}
        )
    else: 
        results = collection.query(
            query_texts=[query],
            n_results = 5, 
        )
    print(f"\n -----Search Results -----\n")
    print({query})
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        distance = results['distances'][0][i]
        metadata = results['metadatas'][0][i]
        doc_id = results['ids'][0][i]
        print(f"{i+1}. [distance: {distance:.4f}] (Module {metadata['module']}, {metadata['topic']} )")
        print(f"     {doc[:100]}...")
    

# Run at least 3 test queries:
# One broad query (no filter)
search("Find all documents where the topic is 'ai'.")
# One filtered to a specific module
search("Retrieve documents from the 'Frontend Engineering' module.", module="Frontend Engineering")
# One where the query uses completely different words than the stored documents
search("Find documents related to systems that imitate human thinking and decision-making.")