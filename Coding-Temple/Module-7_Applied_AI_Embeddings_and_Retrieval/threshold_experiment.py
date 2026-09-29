from sentence_transformers import SentenceTransformer, util

# Load pre-trained model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Knowledge base (20 sentences covering 4 distinct topics)
sentences = [
    # Group 1: Python Development
    "Python uses indentation to define code blocks instead of curly braces.",
    "FastAPI supports automatic data validation using Pydantic models.",
    "Git commits create snapshots of a project’s file history.",
    "Docker Compose can manage multiple containers in a single application stack.",
    "Machine learning models improve performance by learning patterns from data.",
    
    # Group 2: Cooking & Culinary
    "Baking bread requires yeast, flour, water, and time for fermentation.",
    "Olive oil is commonly used in Mediterranean cooking.",
    "Grilling vegetables can enhance their flavor through caramelization.",
    "Fresh herbs are often added at the end of cooking for stronger aroma.",
    "Cast iron pans retain heat very effectively for searing food.",
    
    # Group 3: Space & Astronomy
    "Mars is known as the Red Planet because of iron oxide on its surface.",
    "Black holes have gravitational fields so strong that light cannot escape.",
    "The International Space Station orbits Earth approximately every ninety minutes.",
    "Telescopes allow astronomers to observe distant galaxies and stars.",
    "Jupiter is the largest planet in the solar system.",
    
    # Group 4: Music & Audio
    "Classical music often features orchestras with string and wind instruments.",
    "Jazz music frequently uses improvisation during performances.",
    "Electronic music producers rely heavily on synthesizers and digital audio software.",
    "A metronome helps musicians maintain a consistent tempo while practicing.",
    "Vinyl records store audio in grooves that are read by a stylus."
]

embeddings = model.encode(sentences, convert_to_tensor=True)

# Define 5 test queries (direct and ambiguous)
queries = [
    "How do I validate API request data in FastAPI?",
    "What ingredients are needed to bake homemade bread?",
    "Why is Mars called the Red Planet?",
    "How do musicians keep a steady rhythm while practicing?",
    "What tools are commonly used for recording audio and processing data?"
]

thresholds = [0.3, 0.5, 0.7]

for query in queries:
    query_emb = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, embeddings)[0]

    # Zip sentences with scores and sort in descending order
    results = sorted(zip(sentences, scores), key=lambda x: x[1], reverse=True)

    # 1. Clear Section Header & Query Title
    print("=" * 80)
    print(f'QUERY: "{query}"')
    print("=" * 80)

    # Store baseline results passing 0.3 threshold to track dropped candidates
    baseline_passing = [(sent, score.item()) for sent, score in results if score >= 0.3]

    for threshold in thresholds:
        # 2. Filter & sort matches above current threshold
        passing = [(sent, score.item()) for sent, score in results if score >= threshold]

        print(f"\n  Threshold {threshold}: {len(passing)} results")

        if passing:
            for sent, score in passing:
                print(f"    [{score:.2f}] {sent}")
        else:
            print("    [No matching results]")

        # 3. Explicitly identify excluded sentences (baseline matches filtered out by stricter threshold)
        if threshold > 0.3:
            excluded = [(sent, score) for sent, score in baseline_passing if score < threshold]

            if excluded:
                print(f"    -- Excluded by stricter threshold (dropped from >= 0.3):")
                for sent, score in excluded:
                    print(f"       [{score:.2f}] {sent}")
            else:
                print("    -- Excluded: None (All baseline matches survived this threshold)")

    print("\n")