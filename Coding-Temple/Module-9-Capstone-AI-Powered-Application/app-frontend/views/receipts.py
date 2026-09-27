import streamlit as st
import requests
import os 
from datetime import date

API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

st.set_page_config(page_title="LedgeAI - Receipts", page_icon="🧾", layout="wide")

st.title("🧾 Receipt Management")

# Auth Check
user_token = st.session_state.get("token")
if not user_token:
    st.warning("Please log in on the Authentication page to access receipts.")
    st.stop()

headers = {"Authorization": f"Bearer {user_token}"}

tab1, tab2 = st.tabs(["Upload & Process Receipt", "All Receipts"])

# ── Tab 1: Upload ──
with tab1:
    st.subheader("Upload Receipt / Expense Document")
    uploaded_file = st.file_uploader(
        "Choose a receipt image or PDF", type=["png", "jpg", "jpeg", "pdf"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        merchant_name = st.text_input("Merchant / Store Name (Optional)", placeholder="e.g. Apple, Walmart")
    with col2:
        category = st.selectbox("Category", ["Office", "Travel", "Meals", "Software", "Equipment", "Other"])

    total_amount=st.number_input("Total Amount ($)", min_value=0.0, step=1.0)

    if uploaded_file and st.button("Upload & Index", use_container_width=True):
        if not merchant_name: 
            st.warning("Please enter a merchant name.")
        else: 
            with st.spinner("Processing document & indexing into RAG..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {
                    "merchant_name": merchant_name, 
                    "category": category, 
                    "total_amount": total_amount
                    }
            
            # Send to FastAPI Upload Endpoint
            try: 
                res = requests.post(f"{API_URL}/receipts/upload", headers=headers, files=files, data=data, timeout=15)
                
                if res.status_code in (200, 201):
                    st.success("Receipt successfully processed and stored!")
                else:
                    st.error(res.json().get("detail", "Upload failed."))
            except requests.exceptions.RequestException as e: 
                st.error(f"Could not connect to backend server: {e}")

# ── Tab 2: Gallery / List ──
with tab2:
    st.subheader("Stored Receipts")
    
    if st.button("🔄 Refresh Receipts"):
        st.rerun()
    try: 
        res = requests.get(f"{API_URL}/receipts/", headers=headers,timeout=10)
        
        if res.status_code == 200:
            receipts = res.json()
            if receipts:
                st.dataframe(receipts, use_container_width=True, hide_index=True)
            else:
                st.info("No receipts uploaded yet.")
        else:
            st.error(f"Failed to fetch receipts: {res.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to backend server: {e}")