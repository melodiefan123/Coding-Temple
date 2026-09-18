
from sentence_transformers import SentenceTransformer, util

# Define a knowledge base of at least 15 sentences covering 3-4 distinct topics (e.g., Python development, cooking, space, music)
model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
 #Group 1: Python
  "Python uses indentation to define code blocks instead of curly braces.",
  "FastAPI supports automatic data validation using Pydantic models.",
  "Git commits create snapshots of a project’s file history.",
  "Docker Compose can manage multiple containers in a single application stack.",
  "Machine learning models improve performance by learning patterns from data.",
  #Group 2: Cooking
  "Baking bread requires yeast, flour, water, and time for fermentation.",
  "Olive oil is commonly used in Mediterranean cooking.",
  "Grilling vegetables can enhance their flavor through caramelization.",
  "Fresh herbs are often added at the end of cooking for stronger aroma.",
  "Cast iron pans retain heat very effectively for searing food.",
  #Group 3: Space
  "Mars is known as the Red Planet because of iron oxide on its surface.",
  "Black holes have gravitational fields so strong that light cannot escape.",
  "The International Space Station orbits Earth approximately every ninety minutes.",
  "Telescopes allow astronomers to observe distant galaxies and stars.",
  "Jupiter is the largest planet in the solar system.",
#   Group 4: Music
  "Classical music often features orchestras with string and wind instruments.",
  "Jazz music frequently uses improvisation during performances.",
  "Electronic music producers rely heavily on synthesizers and digital audio software.",
  "A metronome helps musicians maintain a consistent tempo while practicing.",
  "Vinyl records store audio in grooves that are read by a stylus."
]

embeddings = model.encode(sentences)

# Define 5 test queries — some clearly matching one topic, some ambiguous

queries = [
  "How do I validate API request data in FastAPI?",
  "What ingredients are needed to bake homemade bread?",
  "Why is Mars called the Red Planet?",
  "How do musicians keep a steady rhythm while practicing?",
  "What tools are commonly used for recording audio and processing data?"
]

# For each query, compute similarity scores against all documents
for query in queries:
    query_emb = model.encode(query)
    scores = util.cos_sim(query_emb, embeddings)[0]
    thresholds = [0.3, 0.5, 0.7]
    # Display results at three different thresholds: 0.3, 0.5, and 0.7
    
    # For each threshold, show:
    # How many results pass the threshold
    # Which results are included
    for threshold in thresholds: 
        passing = [(idx, score) for idx, score in enumerate(scores) if score >= threshold]
        print(f"Threshold {threshold}: {len(passing)} results")
        for idx, score in passing: 
            print(f"  [{score:.4f}] {sentences[idx]}")









