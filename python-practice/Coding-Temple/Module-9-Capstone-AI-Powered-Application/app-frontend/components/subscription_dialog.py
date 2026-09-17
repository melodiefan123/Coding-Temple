import streamlit as st
import requests

@st.dialog("➕ Add New Subscription")
def add_subscription_dialog(cards: list, api_url: str, headers: dict, active_card_id: int = None):
    st.markdown("""
        <style>
        /* Force dialog modal container */
        div[role="dialog"], div[data-testid="stDialog"] {
            background-color: #121413 !important;
            color: #ffffff !important;
        }
        /* Force form submit button inside dialog */
        div[role="dialog"] button, 
        div[role="dialog"] button[kind="primary"],
        div[role="dialog"] button[kind="secondary"] {
            background-color: #1c1f1d !important;
            background: #1c1f1d !important;
            color: #ffffff !important;
            border: 1px solid #3f4652 !important;
        }
        div[role="dialog"] button:hover {
            background-color: #2b303c !important;
            border-color: #605D5C !important;
        }
        div[role="dialog"] button * {
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)
    if not cards:
        st.warning("No cards found. Please add a credit card first before creating a subscription.")
        return

    # Map card labels (e.g., "Visa ending in 4242") to card IDs
    card_options = {
        f"{c.get('card_type', 'Card').upper()} •••• {str(c.get('card_number', ''))[-4:]}": c.get('id')
        for c in cards
    }
    card_ids = list(card_options.values())
    default_index = card_ids.index(active_card_id) if active_card_id in card_ids else 0

    with st.form("add_sub_form", clear_on_submit=True):
        sub_name = st.text_input("Subscription Name", placeholder="e.g. Netflix, Spotify, ChatGPT")
        
        col_amt, col_cycle = st.columns([1, 1])
        with col_amt:
            sub_amount = st.number_input("Amount ($)", min_value=0.01, step=1.00, value=14.99)
        with col_cycle:
            sub_cycle = st.selectbox("Billing Cycle", ["monthly", "yearly", "weekly"])

        selected_card_label = st.selectbox("Pay With Card", options=list(card_options.keys()), index=default_index)
        selected_card_id = card_options[selected_card_label]

        submitted = st.form_submit_button("Save Subscription", use_container_width=True)

        if submitted:
            if not sub_name.strip():
                st.error("Please enter a subscription name.")
            else:
                payload = {
                    "card_id": selected_card_id,
                    "name": sub_name.strip(),
                    "amount": float(sub_amount),
                    "billing_cycle": sub_cycle
                }                
                try:
                    res = requests.post(f"{api_url}/cards/subscriptions", json=payload, headers=headers)
                    if res.status_code in (200, 201):
                        st.success(f"Linked {sub_name} to card!")
                        st.rerun()
                    else:
                        st.error(f"Failed to save: {res.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")