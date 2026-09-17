"""
Module 7 Project — Semantic Search Engine
==========================================
app.py — Streamlit search interface

Run with:
    streamlit run app.py

Make sure you've indexed documents first:
    python ingest.py
"""

import streamlit as st
from search import search, get_collection_stats
from ingest import ingest, DEFAULT_CHUNK_SIZE, DEFAULT_OVERLAP

st.set_page_config(page_title="Semantic Search", page_icon="🔍", layout="wide")
# --- Sidebar: Ingestion Controls ---

with st.sidebar:
    st.title("📁 Search Manager")
    stats = get_collection_stats()
    selected_sources = st.multiselect("Filter by source", options=stats["source_names"])
    if st.button("🔄 Re-index Documents"):
        ingest_func = ingest(DEFAULT_CHUNK_SIZE, DEFAULT_OVERLAP)
        st.success("Documents re-indexed successfully!")
    st.metric("Total Chunks",stats["total_chunks"])
    st.metric("Unique Sources", stats["unique_sources"])
    st.divider()
    n_results = st.slider("Results to show", 1,10,5)
    distance_threshold = st.slider("Distance Threshold", 0.0,2.0, 1.0)

# --- Main Search Interface ---
st.title("🔍 Semantic Search")
st.write("Search your course documents by meaning, not just keywords.")

query = st.text_input("Enter your search query", placeholder="How does authentication work?",
                      value=st.session_state.get("query", ""))

if query and stats["total_chunks"] > 0:
    results = search( 
        query = query,
        n_results = n_results,
        sources = selected_sources or None ,
        distance_threshold = distance_threshold)
    for result in results: 
        with st.expander(f"e.g. 📄 filename — chunk index (score: int)"):
            st.write(f"{result["text"]}- chunk{result["chunk_index"]} (score: {result["score"]})")
            st.write(result['source'])
            st.write(result['distance'])
    if not results: 
        st.error("The results are empty")

    



