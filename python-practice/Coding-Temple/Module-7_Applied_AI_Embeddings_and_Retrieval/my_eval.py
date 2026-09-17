from sentence_transformers import SentenceTransformer, util
import json

model = SentenceTransformer('all-MiniLM-L6-v2')
# Set up a ChromaDB collection with at least 12 documents covering 3–4 topics (you can reuse documents from previous exercises)
documents = {
    "doc_jwt": "JWT tokens provide stateless authentication for REST APIs. The server creates a signed token containing user info.",
    "doc_pydantic": "Pydantic models define data schemas for FastAPI. They automatically validate incoming request data.",
    "doc_session": "Streamlit session state persists data across re-runs. Initialize with: if key not in st.session_state.",
    "doc_cors": "CORS middleware in FastAPI allows cross-origin requests from frontend applications running on different ports.",
    "doc_embed": "Embeddings convert text into numerical vectors capturing semantic meaning. Similar texts get similar vectors.",
    "doc_cosine": "Cosine similarity measures the angle between two vectors. A score of 1.0 means identical direction.",
    "doc_chunk": "Chunking splits documents into smaller pieces for embedding. Chunk size affects search precision and recall.",
    "doc_chroma": "ChromaDB is a vector database for storing and querying embeddings. It supports metadata filtering.",
    "doc_flex": "CSS Flexbox arranges elements in rows or columns. Use display:flex on the container.",
    "doc_dom": "The DOM is the browser's tree representation of HTML. JavaScript uses it to modify page content.",
    "doc_api": "REST APIs enable communication between frontend and backend systems through HTTP requests and JSON responses.",
    "doc_index": "Database indexes improve query performance by reducing the amount of data scanned during searches."
}
doc_ids = list(documents.keys())
doc_texts = list(documents.values())
doc_embeddings = model.encode(doc_texts)
# Create an evaluation set with at least 6 test queries, each with a list of expected relevant document IDs
eval_set=[
    {
    "query": "how does authentication work in APIs?",
    "relevant": ["doc_jwt", "doc_cors"]
    },
    {
    "query": "What is semantic similarity and how is it measured?",
    "relevant": ["doc_embed", "doc_cosine"]
    },
    {
    "query": "How should I prepare documents for a search system?",
    "relevant": ["doc_chunk", "doc_chroma"] 
    }, 
    {
    "query": "How do I make a webpage interactive?",
    "relevant": ["doc_dom", "doc_flex"]
    }, 
    {
    "query": "How does Streamlit remember data between interactions?",
    "relevant": ["doc_session"]
    }, 
    {
    "query": "How do CSS flexboxes work? ",
    "relevant": ["doc_flex"]
    }]
# Implement an evaluate() function that:
# Runs each test query against your collection
# Computes precision and recall for each query
# Computes average precision and recall across all queries
# Displays per-query results and overall scores
def evaluate(eval_set, top_k = 3, threshold =0.3):
    total_precision = 0 
    total_recall = 0 
    
    print(f"\n ===Evaluation at threshold = {threshold}, n_results = {top_k} ")
    for item in eval_set:
        query = item["query"]
        relevant = set(item["relevant"])
        query_embed = model.encode(query)
        scores = util.cos_sim(query_embed,doc_embeddings)[0]
        results = []
        for i, score in enumerate(scores):
            if score.item() >= threshold:
                results.append((doc_ids[i], score.item()))

        results.sort(key=lambda x: x[1], reverse=True)
        retrieved = [id for id, score in results[:top_k]]
        matches = set(retrieved) & relevant
        precision = len(matches) / len(retrieved) if retrieved else 0
        recall = len(matches) / len(relevant) if relevant else 0
        total_precision += precision
        total_recall += recall
        print(f"  Query: {query}")
        print(f"  Precision: {precision:.2f}, Recall: {recall:.2f}")
    avg_precision = total_precision / len(eval_set)
    avg_recall = total_recall / len(eval_set)
    print(f"\n  Avg Precision: {avg_precision:.2f}, Avg Recall: {avg_recall:.2f}")
        
# Run the evaluation at 3 different settings (vary either the threshold, n_results, or both) and compare the results
evaluate(eval_set, top_k = 5, threshold =0.5)
evaluate(eval_set, top_k = 9, threshold =0.3)
evaluate(eval_set, top_k = 3, threshold =0.75)
# Write a brief analysis (as comments or print statements): Which queries worked well? Which failed? What would you change to improve scores?

#Queries such as the semantic similarity, api authentication, streamlit data worked well, the evaluation at 0.75 threshold failed. What I found interesting is the API authentication query has a precision of 1 at threshold 0.5 but a precision of 0.5 at a threshold of 0.3. To improve the score, I can look through my eval set and see if I can add more relevant docs. 