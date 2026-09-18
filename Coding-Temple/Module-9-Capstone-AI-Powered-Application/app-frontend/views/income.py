import streamlit as st
import requests

def render_income_manager(api_url, headers, incomes):
    col_inc_form, col_inc_list = st.columns([1, 1])

    with col_inc_form:
        st.subheader("Add Additional Income")
        with st.form("inc_form", clear_on_submit=True):
            source = st.text_input("Source/Client", placeholder="e.g. Consulting, Investments")
            amount = st.number_input("Amount ($)", min_value=0.0, value=500.0, step=50.0)
            if st.form_submit_button("Save Income Entry"):
                if source:
                    try:
                        res = requests.post(
                            f"{api_url}/income/", 
                            json={"source": source, "amount": float(amount)}, 
                            headers=headers,
                            timeout=10
                        )
                        if res.status_code in (200, 201):
                            st.success(f"Added ${amount:,.2f} from '{source}'")
                            st.rerun()
                        else:
                            detail = res.json().get("detail", "Failed to add income.")
                            st.error(f"Error {res.status_code}: {detail}")
                    except Exception as e:
                        st.error(f"Error connecting to backend: {e}")
                else:
                    st.warning("Please enter a source description.")

    with col_inc_list:
        st.subheader("Logged Additional Income")
        if incomes:
            formatted = [{"Source": i["source"], "Amount": f"${i['amount']:,.2f}"} for i in incomes]
            st.dataframe(formatted, use_container_width=True, hide_index=True)
        else:
            st.info("No additional income entries logged yet.")
    

# ------------------------------------------------------------------------------
# TOP-UP DIALOG MODAL
# ------------------------------------------------------------------------------
@st.dialog("💳 Top Up Account")
def show_topup_dialog(api_url, headers):
    st.write("Add funds to your account balance.")
    
    with st.form("topup_form", clear_on_submit=True):
        source = st.text_input("Source / Description", value="Direct Top Up", placeholder="e.g. Bank Transfer, Client Deposit")
        amount = st.number_input("Amount ($)", min_value=1.00, step=50.00, value=100.00)
        submitted = st.form_submit_button("Confirm Top Up", use_container_width=True)
        
        if submitted:
            payload = {
                "source": source,
                "amount": amount
            }
            try:
                res = requests.post(f"{api_url}/income/", json=payload, headers=headers, timeout=5)
                if res.status_code in (200, 201):
                    st.toast("✅ Account topped up successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to process top-up ({res.status_code}).")
            except Exception as e:
                st.error(f"Connection error: {e}")