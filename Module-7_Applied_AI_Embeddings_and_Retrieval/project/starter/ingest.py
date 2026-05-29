"""
Module 7 Project — Semantic Search Engine
==========================================
ingest.py — document loading, chunking, and ChromaDB storage

Run with:
    python ingest.py
    python ingest.py --chunk-size 200 --overlap 50
"""

import argparse
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
import os

# ── Configuration ─────────────────────────────────────────────────────────────
DOCS_DIR        = Path("docs")
CHROMA_PATH     = Path("chroma_data")
COLLECTION_NAME = "semantic_search"
MODEL_NAME      = "all-MiniLM-L6-v2"
DEFAULT_CHUNK_SIZE = 500
DEFAULT_OVERLAP    = 100


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Split text into fixed-size chunks with overlap.

    Args:
        text:       Full document text.
        chunk_size: Maximum characters per chunk.
        overlap:    Characters of overlap between consecutive chunks.

    Returns:
        List of non-empty chunk strings.
    """
    if chunk_size <= 0: 
        raise ValueError("Chunk Size must be greater than 0")
    if overlap < 0: 
        raise ValueError("Overlap must be non-negative")
    chunks = [] 
    start = 0 
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk: 
            chunks.append(chunk)
        start = end - overlap
    return chunks


def load_documents(docs_dir: Path) -> list[dict]:
    """
    Read all .txt and .md files from docs_dir.

    Returns:
        List of dicts: {"filename": str, "text": str}
    """
    documents = []
    
    for filename in docs_dir.glob("*"):
        if filename.suffix in [".txt", ".md"]:
            with open(filename, "r", encoding='utf-8') as f: 
                content = f.read()
            if not content.strip():
                continue
            documents.append({
                "filename": filename.name, 
                "text": content,
                })
    return documents


def get_collection(chroma_path: Path, collection_name: str):
    """Create (or retrieve) a persistent ChromaDB collection."""
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_or_create_collection(
        name=collection_name
    )
    return collection


def ingest(chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_OVERLAP):
    """
    Full ingestion pipeline: load → chunk → embed → upsert.

    Each chunk is stored with metadata: source filename, chunk index,
    and the chunk size used — so experiments with different sizes can
    be compared without ambiguity.
    """
    documents = load_documents(DOCS_DIR)
    collection = get_collection(CHROMA_PATH, COLLECTION_NAME)
    all_chunks = []
    all_metadatas = []
    all_ids = []
    for doc in documents: 
        chunks = chunk_text(doc["text"],chunk_size, overlap)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadatas.append({"filename": doc["filename"], "chunk_index": i, "chunk_size": chunk_size, "overlap": overlap})
            all_ids.append(f"{doc['filename']}_{chunk_size}_{overlap}_{i}")
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(all_chunks)
    collection.upsert(
        documents = all_chunks, 
        embeddings=embeddings,
        metadatas= all_metadatas, 
        ids = all_ids,
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Index docs/ into ChromaDB")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    parser.add_argument("--overlap",    type=int, default=DEFAULT_OVERLAP)
    args = parser.parse_args()
    ingest(chunk_size=args.chunk_size, overlap=args.overlap)
