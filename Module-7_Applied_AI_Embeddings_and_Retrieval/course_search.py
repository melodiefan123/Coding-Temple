
# Test with queries that use different words than your sentences

from sentence_transformers import SentenceTransformer, util
# Define a list of at least 10 sentences summarizing things you've learned in this course

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
  "Docker containers package applications with all their dependencies for consistent deployment.",
  "Pandas DataFrames make it easy to filter, group, and analyze structured data.",
  "React components re-render automatically when their state changes.",
  "Git branches allow developers to work on features independently before merging.",
  "Redis is commonly used as an in-memory cache for high-performance applications.",
  "REST APIs typically exchange data using JSON formatted payloads.",
  "Environment variables help keep sensitive configuration values out of source code.",
  "NumPy provides optimized array operations for scientific computing in Python.",
  "WebSocket connections enable real-time communication between clients and servers.",
  "Unit tests help verify that individual functions behave as expected."
]
# Embed all sentences using SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(sentences)
# Implement a search loop that asks the user for a query, embeds the query, finds and displays the top 3 most similar sentences with their similarity scores, and continues until the user types "quit"
while True: 
    query = input("Search (or 'quit'):")
    if query.strip().lower() == 'quit':
        break
    query_embedded = model.encode(query)

    scores = util.cos_sim(query_embedded, embeddings)[0]
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

    print("Top 3 results:")
    for rank, (idx, score) in enumerate(ranked[:3], 1):
        print(f" {rank}. [{score:.4f}] {sentences[idx]}")

    


