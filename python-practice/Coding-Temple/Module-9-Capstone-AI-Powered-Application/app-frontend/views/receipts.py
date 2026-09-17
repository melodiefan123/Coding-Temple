import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="LedgeAI - Receipts", page_icon="🧾", layout="wide")

st.title("🧾 Receipt Management")

# Auth Check
if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in first from the Auth page.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

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
            res = requests.post(f"{API_URL}/receipts/upload", headers=headers, files=files, data=data)
            
            if res.status_code in (200, 201):
                st.success("Receipt successfully processed and stored!")
            else:
                st.error(res.json().get("detail", "Upload failed."))

# ── Tab 2: Gallery / List ──
with tab2:
    st.subheader("Stored Receipts")
    
    if st.button("🔄 Refresh Receipts"):
        st.rerun()

    res = requests.get(f"{API_URL}/receipts/", headers=headers)
    
    if res.status_code == 200:
        receipts = res.json()
        if not receipts:
            st.info("No receipts found. Upload your first receipt in the tab above!")
        else:
            for receipt in receipts:
                merchant = receipt.get("merchant_name", "Unknown Merchant")
                amount = float(receipt.get("total_amount", 0.0))
                date_str = receipt.get("transaction_date", "N/A")[:10] if receipt.get("transaction_date") else "N/A"
                
                with st.expander(f"🧾 {merchant} — ${amount:,.2f}"):
                    c1, c2, c3 = st.columns(3)
                    c1.write(f"**Date:** {date_str}")
                    c2.write(f"**Category:** {receipt.get('category', 'Uncategorized')}")
                    c3.write(f"**Verified:** {'Yes ✅' if receipt.get('is_verified') else 'No ❌'}")
    else:
        st.error("Could not retrieve receipts from server.")