import chromadb
# Create a persistent ChromaDB client (data survives restarts)
client = chromadb.PersistentClient(path="./chroma_demo")

# Create a collection called "my_knowledge"
collection = client.get_or_create_collection(
    name="my_knowledge",
    metadata={"description": ""}
)
# Add at least 15 documents covering content from at least 3 different modules you’ve completed. Each document should include:
# A unique ID
# The text content (a sentence or short paragraph summarizing a concept)
# Metadata with at least: module (which module it’s from) and topic (general category like "api", "database", "frontend", "ai")

documents = []
# Implement a search function that:
# Accepts a query string and an optional module filter
# Returns the top 5 results with distances and metadata
# Run at least 3 test queries:
# One broad query (no filter)
# One filtered to a specific module
# One where the query uses completely different words than the stored documents