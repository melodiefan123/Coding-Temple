# Module 7 Project — Semantic Search Engine (Starter)

## Overview

Build a semantic search tool over a document collection. The tool loads, chunks,
embeds, and stores documents in ChromaDB, then provides a Streamlit interface
where users can type a question and see ranked results. You'll also run a
chunking experiment and document your findings.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Index the document corpus:
   ```bash
   python ingest.py
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit search interface — your primary work file |
| `ingest.py` | Document loading, chunking, and ChromaDB storage |
| `search.py` | Search functions: query ChromaDB and rank results |
| `evaluate.py` | Evaluation framework: precision and recall |
| `docs/` | Starter document corpus (add your own documents here) |
| `chroma_data/` | Persistent ChromaDB storage (created on first run) |
| `requirements.txt` | Python dependencies |

## Requirements

See the project brief on the course platform for the full rubric. Key sections:

1. **Document Ingestion** — load `docs/` folder, configurable chunk size/overlap,
   store in ChromaDB with source and chunk-index metadata
2. **Semantic Search** — ranked results with scores, configurable `n_results` and
   threshold, edge-case handling
3. **Streamlit Interface** — search input, sidebar controls (filter, re-index,
   result count), at least one `st.metric()`
4. **Chunking Experiment** — re-index at 2+ chunk sizes, run 5 identical queries,
   compare and document findings in this README
5. **Code Quality** — docstrings, modular files, working `requirements.txt`

## Chunking Experiment Results

**Chunk sizes tested:** 200 chars vs 500 chars

**Test queries:**
1.How do you create a FastAPI route?
2.What are the differences between lists and dictionaries in Python?
3.How do you join tables in SQL?
4.What are word embeddings and how do vectors represent meaning?
5.How do you display a dataframe in Streamlit?


**Findings:**

Both chunk sizes (200 and 500) produced identical results, with average precision 
of 0.20 and perfect recall of 1.00 across all queries. Chunk size did not affect 
whether the right document was found. Precision is likely limited by n_results=5 
with single-source relevance judgments rather than chunk quality. Smaller chunks 
(200) may be better for pinpointing specific passages, while larger chunks (500) 
provide more context per result.
