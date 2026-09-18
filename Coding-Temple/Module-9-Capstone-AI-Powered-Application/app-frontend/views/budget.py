# views/budget.py
import streamlit as st
import requests

def render_budget_manager(api_url, headers, budgets):
    col_bud_form, col_bud_list = st.columns([1, 1])

    with col_bud_form:
        st.subheader("Add/Update Category")
        with st.form("budget_form", clear_on_submit=True):
            category = st.text_input("Category", placeholder="e.g. Office, Marketing")
            limit = st.number_input("Monthly Limit ($)", min_value=0.0, value=1000.0, step=50.0)
            if st.form_submit_button("Save Budget"):
                if category:
                    try:
                        res = requests.post(
                            f"{api_url}/budgets", 
                            json={"category": category, "monthly_limit": float(limit)}, 
                            headers=headers,
                            timeout=10
                        )
                        if res.status_code in (200, 201):
                            st.cache_data.clear()
                            st.success(f"Saved limit for '{category}'")
                            st.rerun()
                        else:
                            detail = res.json().get("detail", "Failed to save budget.")
                            st.error(f"Error {res.status_code}: {detail}")
                    except Exception as e:
                        st.error(f"Error connecting to backend: {e}")
                else:
                    st.warning("Please enter a category name.")

    with col_bud_list:
        st.subheader("Active Allocations")
        if budgets:
            formatted = [{"Category": b["category"], "Limit": f"${b['monthly_limit']:,.2f}"} for b in budgets]
            st.dataframe(formatted, use_container_width=True, hide_index=True)
        else:
            st.info("No budget categories found.")


@st.dialog("Add Expense")
def show_expense_dialog(api_url, headers, card_id=None):
    st.write("Record an expense transaction.")
    
    with st.form("expense_form", clear_on_submit=True):
        description = st.text_input("Description", value="", placeholder="e.g. Office Supplies, SaaS Subscription")
        category = st.text_input("Category", value="General", placeholder="e.g. Utilities, Marketing")
        amount = st.number_input("Amount ($)", min_value=1.00, step=1.00, value=50.00)
        
        submitted = st.form_submit_button("Confirm Expense", use_container_width=True)
        
        if submitted:
            parsed_card_id = int(card_id) if (card_id is not None and str(card_id).isdigit()) else None            
            payload = {
                "description": description if description else "Expense Entry",
                "category": category,
                "amount": float(amount),
                "card_id": parsed_card_id
            }
            
            try:
                # 2. Target the exact endpoint: POST /budget/expenses
                res = requests.post(
                    f"{api_url}/budgets/expenses", 
                    json=payload, 
                    headers=headers, 
                    timeout=5
                )

                if res.status_code in (200, 201):
                    st.cache_data.clear()
                    st.toast("✅ Expense added successfully!")
                    st.rerun()
                else:
                    # Capture detail string from FastAPI response validation errors
                    err_resp = res.json()
                    detail = err_resp.get("detail", f"Status Code {res.status_code}")
                    st.error(f"Failed to process expense: {detail}")

            except requests.exceptions.RequestException as e:
                st.error(f"Network error connecting to backend: {e}")
            except Exception as e:
                st.error(f"Application error: {e}")