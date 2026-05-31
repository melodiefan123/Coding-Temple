"""
Module 7 Project — Semantic Search Engine
==========================================
search.py — query ChromaDB and return ranked results

Import this module into app.py:
    from search import search, get_collection_stats
"""

from pathlib import Path
import chromadb


# ── Configuration (must match ingest.py) ─────────────────────────────────────
CHROMA_PATH     = Path("chroma_data")
COLLECTION_NAME = "semantic_search"
MODEL_NAME      = "all-MiniLM-L6-v2"


def get_collection():
    """Return the persistent ChromaDB collection."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )
    return collection


def search(
    query: str,
    n_results: int = 5,
    sources: list[str] = None,
    distance_threshold: float = None,
) -> list[dict]:
    """
    Search the ChromaDB collection and return ranked results.

    Args:
        query:              Natural language search query.
        n_results:          Maximum number of results to return.
        sources:            If provided, only return chunks from these filenames.
        distance_threshold: If provided, exclude results with distance above this
                            value (lower = more similar).

    Returns:
        List of result dicts sorted by distance ascending (best first):
        {
                "text":        str,
                "source":      str,
                "chunk_index": int,
                "distance":    float,
                "score":       float,  # 1 - distance
            }
        Returns [] for empty queries or if the collection has no documents.
    """
    if not query: 
        return []
    collection = get_collection()
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where={"filename": {"$in":sources}} if sources else None
        )
    result_list = []
    docs = results["documents"][0]
    meta = results["metadatas"][0]
    dists = results["distances"][0]
    
    for i in range(len(docs)):
       if distance_threshold and dists[i] > distance_threshold:
            continue
       result_list.append(
       {
        "text": docs[i],
        "source": meta[i]["filename"],
        "chunk_index": meta[i]["chunk_index"],
        "distance": dists[i],
        "score": 1 - dists[i]
        }) 
    return result_list
    






def get_collection_stats() -> dict:
    """
    Return basic stats about the indexed collection.

    Returns:
        {
            "total_chunks":   int,
            "unique_sources": int,
            "source_names":   list[str],
        }
    """
    collection = get_collection()
    metadatas = collection.get()["metadatas"]
    source_names = set()
    for metadata in metadatas: 
        source_names.add(metadata['filename'])
    return {"total_chunks": collection.count(), "unique_sources": len(source_names), "source_names": list(source_names)}
