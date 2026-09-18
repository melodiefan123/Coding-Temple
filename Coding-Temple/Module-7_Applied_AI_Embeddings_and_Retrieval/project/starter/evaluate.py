"""
Module 7 Project — Semantic Search Engine
==========================================
evaluate.py — precision and recall for your search system

Run with:
    python evaluate.py
    python evaluate.py --n-results 5 --threshold 0.4

Define your evaluation set in EVAL_SET, then run this script against
different index configurations (different chunk sizes) to compare results.
"""

import argparse
from search import search


# Define your evaluation set here.
# Each entry needs a query and the source filenames you expect to be relevant.
# Use at least 5 queries for the chunking experiment.
EVAL_SET = [
    {"query": "How do you create a FastAPI route?",
     "relevant_sources": ["fastapi.txt"]},
    {"query": "What are the differences between lists and dictionaries in Python?",
     "relevant_sources": ["python-fundamentals.txt"]},
    {"query": "How do you join tables in SQL?",
     "relevant_sources": ["sql-databases.txt"]},
    {"query": "What are word embeddings and how do vectors represent meaning?",
     "relevant_sources": ["embeddings-and-vectors.txt"]},
    {"query": "How do you display a dataframe in Streamlit?",
     "relevant_sources": ["streamlit.txt"]},
]


def precision_recall(
    retrieved_sources: list[str], relevant_sources: list[str]
) -> tuple[float, float]:
    """
    Compute source-level precision and recall.

    Returns (precision, recall) as floats in [0, 1].
    """
    if not retrieved_sources:
        return (0.0, 0.0)
    relevant_retrieved = set(retrieved_sources) & set(relevant_sources)
    precision = len(relevant_retrieved) / len(retrieved_sources)
    recall = len(relevant_retrieved) / len(relevant_sources)
    return (precision, recall)

def evaluate(n_results: int = 5, distance_threshold: float = None):
    """
    Run every query in EVAL_SET and print per-query and average precision/recall.
    """
    total_precision = 0 
    total_recall = 0 
    if not EVAL_SET:
        print("Eval set is empty.")
        return
    for item in EVAL_SET:
        query = item["query"]
        relevant = set(item["relevant_sources"])
        sources = search(query, n_results, distance_threshold)
        retrieved_sources = [result["source"] for result in sources]
        precision, recall = precision_recall(retrieved_sources, relevant)
        total_precision += precision
        total_recall += recall
        print(f"  Query: {query}")
        print(f"  Precision: {precision:.2f}, Recall: {recall:.2f}")
    avg_precision = total_precision / len(EVAL_SET)
    avg_recall = total_recall / len(EVAL_SET)
    print(f"\n  Avg Precision: {avg_precision:.2f}, Avg Recall: {avg_recall:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate search quality")
    parser.add_argument("--n-results", type=int,   default=5)
    parser.add_argument("--threshold", type=float, default=None)
    args = parser.parse_args()
    evaluate(n_results=args.n_results, distance_threshold=args.threshold)
