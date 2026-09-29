import os
import streamlit as st
import chromadb
from typing import List, Dict, Any, Optional

# --- Page Configuration ---
st.set_page_config(
    page_title="Semantic Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
if "query" not in st.session_state:
    st.session_state.query = ""

# --- ChromaDB Initialization ---
@st.cache_resource
def get_collection() -> chromadb.Collection:
    """Initialize and return a persistent ChromaDB collection."""
    client = chromadb.PersistentClient(path="./search_db")
    return client.get_or_create_collection(name="course_docs")

collection = get_collection()

# --- Utility Functions ---
def load_and_chunk(directory: str = "docs", chunk_size: int = 400) -> List[Dict[str, Any]]:
    """
    Safely reads text (.txt, .md) files from the given directory and splits content into chunks.
    
    Args:
        directory: Local directory containing raw text files.
        chunk_size: Maximum character length target for individual chunks.
        
    Returns:
        List of dictionaries containing extracted chunk text and source metadata.
    """
    chunks = []
    
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        return chunks

    filenames = sorted([f for f in os.listdir(directory) if f.endswith(('.txt', '.md'))])
    
    for filename in filenames:
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

            chunk_idx = 0
            for para in paragraphs:
                if len(para) > chunk_size:
                    for i in range(0, len(para), chunk_size):
                        sub_para = para[i:i + chunk_size].strip()
                        if sub_para:
                            chunks.append({
                                "text": sub_para,
                                "source": filename,
                                "chunk_id": f"{filename}_{chunk_idx}",
                                "chunk_index": chunk_idx,
                            })
                            chunk_idx += 1
                else:
                    chunks.append({
                        "text": para,
                        "source": filename,
                        "chunk_id": f"{filename}_{chunk_idx}",
                        "chunk_index": chunk_idx,
                    })
                    chunk_idx += 1

        except Exception as e:
            st.error(f"Error reading file {filename}: {e}")
            
    return chunks

def get_relevance_badge(distance: float) -> str:
    """Maps L2 distance metrics into human-readable relevance threshold badges."""
    if distance < 0.6:
        return ":green[🟢 High Match]"
    elif distance < 1.0:
        return ":orange[🟡 Medium Match]"
    else:
        return ":red[🔴 Low Match]"

# --- Sidebar Controls ---
with st.sidebar:
    st.title("📁 Document Manager")
    
    # Safe retrieval of metadata sources
    db_data = collection.get()
    all_metadatas = db_data.get('metadatas', []) if db_data else []
    
    existing_sources = sorted(
        list(set(m.get('source') for m in all_metadatas if isinstance(m, dict) and 'source' in m))
    )
    
    selected_sources = st.multiselect(
        "Filter by Source File:",
        options=existing_sources,
        help="Select specific document files to limit search results."
    )
    
    if st.button("🔄 Re-index Documents", use_container_width=True):
        with st.spinner("Indexing documents..."):
            chunks = load_and_chunk("docs")
            
            # Purge database before re-indexing to remove deleted file/ghost chunks
            existing_ids = collection.get().get("ids", [])
            if existing_ids:
                collection.delete(ids=existing_ids)
                
            if chunks:
                collection.upsert(
                    documents=[c["text"] for c in chunks],
                    metadatas=[{"source": c["source"], "chunk_index": int(c["chunk_index"])} for c in chunks],
                    ids=[c["chunk_id"] for c in chunks],
                )
                st.sidebar.success(f"Indexed {len(chunks)} chunks from {len(set(c['source'] for c in chunks))} file(s)!")
                st.rerun()
            else:
                st.sidebar.warning("No `.txt` or `.md` files found in `docs/` folder.")

    st.divider()

    st.metric(label="Total Document Chunks", value=collection.count())
    st.metric(label="Unique Sources Ingested", value=len(existing_sources))
    
    st.divider()
    n_results = st.slider("Max Results to Show", min_value=1, max_value=10, value=5)

# --- Main App Body ---
st.title("🔍 Course Material Semantic Search")
st.write("Search course notes and technical documentation using natural language queries.")

# Ensure input key exists in state before rendering text input
if "query_input" not in st.session_state:
    st.session_state["query_input"] = st.session_state.query

query_val = st.text_input(
    "Search Query",
    key="query_input",
    placeholder="e.g., How does FastAPI handle async operations?"
)

# Sync query_val to internal state
st.session_state.query = query_val

total_docs = collection.count()

if st.session_state.query and total_docs > 0:
    where_filter: Optional[Dict[str, Any]] = None
    if selected_sources:
        if len(selected_sources) == 1:
            where_filter = {"source": selected_sources[0]}
        else:
            where_filter = {"source": {"$in": selected_sources}}

    try:
        results = collection.query(
            query_texts=[st.session_state.query],
            n_results=min(n_results, total_docs),
            where=where_filter
        )
        
        retrieved_docs = results['documents'][0] if results and results['documents'] else []
        retrieved_metas = results['metadatas'][0] if results and results['metadatas'] else []
        retrieved_dists = results['distances'][0] if results and results['distances'] else []
        
        shown_count = len(retrieved_docs)
        
        st.markdown(f"### Showing **{shown_count}** of **{total_docs}** total documents")
        st.write("---")

        if shown_count == 0:
            st.info("No matching chunks found for the selected file filter.")

        for idx in range(shown_count):
            doc_text = retrieved_docs[idx]
            meta = retrieved_metas[idx]
            dist = retrieved_dists[idx]
            badge = get_relevance_badge(dist)

            with st.container():
                col_info, col_score = st.columns([3, 1])
                
                with col_info:
                    st.markdown(f"**📄 Source File:** `{meta.get('source', 'Unknown')}` *(Chunk {meta.get('chunk_index', '0')})*")
                    preview_text = doc_text[:150] + ("..." if len(doc_text) > 150 else "")
                    st.write(preview_text)
                    
                with col_score:
                    st.markdown(f"**Relevance:** {badge}")
                    st.caption(f"L2 Distance: `{dist:.4f}`")

                with st.expander("📖 View Full Chunk Text"):
                    st.text(doc_text)

                if st.button("🔗 Find Similar to This Chunk", key=f"btn_similar_{idx}"):
                    # Synchronize both session state keys to force the text input widget to reflect the new text
                    st.session_state["query_input"] = doc_text
                    st.session_state.query = doc_text
                    st.rerun()

                st.divider()

    except Exception as err:
        st.error(f"An error occurred while executing search: {err}")

elif total_docs == 0:
    st.info("💡 The database is currently empty. Add text files to `docs/` and click **Re-index Documents** in the sidebar to get started.")