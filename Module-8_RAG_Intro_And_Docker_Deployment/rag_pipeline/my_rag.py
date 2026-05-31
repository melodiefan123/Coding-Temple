# Ingest: Load documents, chunk by paragraphs, store in persistent ChromaDB

# Retrieve: Query ChromaDB with a user question, return top 3 chunks
# Generate: Build a RAG prompt with retrieved context + system instructions, call Ollama, return the response
# Include these features:
# Source citation instructions in the system prompt
# Display which chunks were retrieved before showing the answer
# Handle the case where Ollama isn’t running (graceful error message)
# An interactive loop (keep asking until the user types "quit")
# Test with at least 3 questions:
# One that should be answerable from your documents
# One that’s related but not directly in the documents
# One that’s completely outside the scope