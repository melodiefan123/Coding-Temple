import streamlit as st
import requests
from datetime import date
import os 

API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

st.set_page_config(page_title="LedgeAI - Invoices", page_icon="📄", layout="wide")

st.title("📄 Invoice Management")

# Auth Check
user_token = st.session_state.get("token")
if not user_token:
    st.warning("Please log in first from the Auth page.")
    st.stop()

headers = {"Authorization": f"Bearer {user_token}",
           "Content-Type": "application/json"
           }

tab1, tab2 = st.tabs(["Create Invoice", "Invoice Ledger"])

# ── Tab 1: Create Invoice ──
with tab1:
    st.subheader("Generate New Client Invoice")
    
    with st.form("create_invoice_form"):
        col1, col2 = st.columns(2)
        with col1:
            invoice_number = st.text_input("Invoice Number", value="INV-1001")
            client_name = st.text_input("Client Name", placeholder="Acme Corp")
            amount = st.number_input("Total Amount ($)", min_value=0.0, step=10.0)
        
        with col2:
            status = st.selectbox("Initial Status", ["pending", "paid", "overdue"])
            issued_date = st.date_input("Issued Date", value=date.today())
            due_date = st.date_input("Due Date", value=date.today())
            
        description = st.text_area("Line Items / Description", placeholder="e.g. Web Development Services - July 2026")
        
        submitted = st.form_submit_button("Create Invoice", use_container_width=True)
        
        if submitted:
            if not client_name:
                st.warning("Please enter a client name.")
            else: 
                payload = {
                    "invoice_number": invoice_number,
                    "client_name": client_name,
                    "amount": amount,
                    "status": status,
                    "issued_date": str(issued_date),
                    "due_date": str(due_date),
                    "description": description
                }
                try: 
                    res = requests.post(f"{API_URL}/invoices/", headers=headers, json=payload, timeout=10)
                    if res.status_code in (200, 201):
                        st.success("Invoice created successfully!")
                    else:
                        st.error(res.json().get("detail", "Failed to create invoice."))
                except requests.exceptions.RequestException as e:
                    st.error(f"Could not connect to backend server: {e}")

# ── Tab 2: Ledger Table ──
with tab2:
    st.subheader("Active & Past Invoices")
    try: 
        res = requests.get(f"{API_URL}/invoices/", headers=headers, timeout=10)
        if res.status_code == 200:
            invoices = res.json()
            if invoices:
                st.dataframe(invoices, use_container_width=True, hide_index=True)
            else:
                st.info("No invoices created yet.")
        else:
            st.error(f"Failed to fetch invoices: {res.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to backend server: {e}")