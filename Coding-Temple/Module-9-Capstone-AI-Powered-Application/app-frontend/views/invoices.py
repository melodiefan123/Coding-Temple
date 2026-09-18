import streamlit as st
import requests
from datetime import date

API_URL = "http://localhost:8000"

st.set_page_config(page_title="LedgeAI - Invoices", page_icon="📄", layout="wide")

st.title("📄 Invoice Management")

# Auth Check
if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in first from the Auth page.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

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
            payload = {
                "invoice_number": invoice_number,
                "client_name": client_name,
                "amount": amount,
                "status": status,
                "issued_date": str(issued_date),
                "due_date": str(due_date),
                "description": description
            }
            
            res = requests.post(f"{API_URL}/invoices/", headers=headers, json=payload)
            if res.status_code in (200, 201):
                st.success("Invoice created successfully!")
            else:
                st.error(res.json().get("detail", "Failed to create invoice."))

# ── Tab 2: Ledger Table ──
with tab2:
    st.subheader("Active & Past Invoices")
    
    res = requests.get(f"{API_URL}/invoices/", headers=headers)
    
    if res.status_code == 200:
        invoices = res.json()
        if not invoices:
            st.info("No invoices found.")
        else:
            # Metrics Overview
            total_billed = sum(i["amount"] for i in invoices)
            total_pending = sum(i["amount"] for i in invoices if i["status"] == "pending")
            
            m1, m2 = st.columns(2)
            m1.metric("Total Billed", f"${total_billed:,.2f}")
            m2.metric("Outstanding Balance", f"${total_pending:,.2f}")
            
            st.divider()
            
            # Format table display
            table_data = [
                {
                    "Invoice #": inv["invoice_number"],
                    "Client": inv["client_name"],
                    "Amount": f"${inv['amount']:,.2f}",
                    "Status": inv["status"].upper(),
                    "Due Date": inv["due_date"], 
                    "Description": inv.get("description", "")
                }
                for inv in invoices
            ]
            
            st.dataframe(table_data, use_container_width=True)
    else:
        st.error("Failed to fetch invoices.")