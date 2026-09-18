from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

document = """
  Artificial intelligence software engineering combines traditional software development with machine learning, cloud infrastructure, and modern AI tooling. AI engineers build systems that can process information, learn patterns from data, and generate intelligent responses in real-world applications. Unlike traditional software, which follows fixed rules written by developers, AI systems often rely on machine learning models that improve performance through training data and inference. Engineers must understand concepts such as embeddings, vector databases, model evaluation, and retrieval-augmented generation to build scalable AI systems.",
  
  "Backend engineering is a major part of AI software development. Frameworks like FastAPI are commonly used to create high-performance APIs that expose AI functionality to web and mobile applications. Developers learn how to handle authentication, validate requests with Pydantic models, and manage asynchronous operations for real-time interactions. AI systems frequently connect to databases, external APIs, and large language models, making API orchestration and data flow management essential skills for production-ready applications.",
  
  "Modern AI applications also depend heavily on data storage and retrieval systems. Relational databases such as PostgreSQL store structured application data, while vector databases like ChromaDB store embeddings used for semantic search. Knowledge bases are often split into smaller text chunks before embeddings are generated, allowing systems to retrieve contextually relevant information efficiently. This architecture is widely used in chatbots, recommendation systems, and AI assistants that need access to external knowledge sources.",
  
  "Cloud infrastructure and deployment tools are equally important in AI engineering. Docker containers package applications with all required dependencies to ensure consistent deployment across environments. Engineers often use Docker Compose and CI/CD pipelines to manage APIs, databases, and AI services together. Scalability, monitoring, logging, and caching become critical concerns when handling large numbers of users or expensive AI inference requests in production systems.",
  
  "AI software engineering courses also emphasize prompt engineering, frontend integration, and system reliability. Developers learn how to design prompts that guide large language models toward accurate outputs and how to integrate AI systems into interfaces built with tools like React or Streamlit. Because AI outputs are probabilistic rather than deterministic, testing and evaluation require different strategies than traditional software engineering. Reliability, safety, and user experience are essential considerations when deploying intelligent applications at scale.
"""

# Fixed-size (300 characters, 50 character overlap)
def fixed_chunks(text, size=300, overlap = 50):
    chunks = []
    start = 0 
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end].strip())
        if end == len(text):  
            break
        start = end - overlap
    return [c for c in chunks if c]
# Paragraph-based (split on double newlines)
def paragraph_chunks(text):
    paragraphs = text.strip().split('\\n\\n')
    return [p.strip() for p in paragraphs if p.strip()]
# Embed all chunks from both strategies
strategies = {
    "Fixed (300 chars)": fixed_chunks(document), 
    "Paragraph": paragraph_chunks(document),
}
# Run 3 different queries against both sets

# For each query, display the top 2 results from each strategy with scores
queries = [
  "What technologies are commonly used in AI software engineering?",
  "How do vector databases support AI applications?",
  "Why are Docker and cloud infrastructure important for deploying AI systems?"
]
for query in queries: 
    print(f"\n Query: '{query}'\n")
    query_embeddings = model.encode(query)

    for name, chunks in strategies.items():
        chunk_embeddings = model.encode(chunks)

        scores = util.cos_sim(query_embeddings, chunk_embeddings )[0]
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        for rank, (idx, score) in enumerate(ranked[:2], 1):
            print(f"Strategy: {name}")
            print(f"{rank}. [{score:.4f}] {chunks[idx]} ")

# At the bottom, write a brief comparison: which strategy performed better and why?
print(f"\nComparison:\n Paragraph chunking performed better because each chunk preserves complete ideas from the document. Fixed-size chunking sometimes splits sentences mid-thought, losing context at the boundaries.")