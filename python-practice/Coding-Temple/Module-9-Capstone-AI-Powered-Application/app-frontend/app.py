import streamlit as st
import requests
import extra_streamlit_components as stx
import pandas as pd

from views.overview import render_overview
from views.income import render_income_manager
from views.budget import render_budget_manager
from views.income import show_topup_dialog
from views.budget import show_expense_dialog
from api_client import APIClient
from components.revenue_chart import render_revenue_chart
from components.expense_chart import render_expense_chart
from components.card_dialog import add_card_dialog, render_interactive_cards
from components.subscription_dialog import add_subscription_dialog 

API_URL = "http://localhost:8001"
api = APIClient(API_URL)

st.set_page_config(page_title="LedgeAI", page_icon="💰", layout="wide")

# Inject Custom CSS for Card Blocks & Navigation Bar
st.markdown("""
<style>
    
    /* Target ALL Form Submit Buttons */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    /* Global App Text */
    html, body, [class*="css"], .stApp {
        color: #FFFFFF !important;
        background-color: #2F2A25 !important;
    }

    label, 
    [data-testid="stWidgetLabel"] *, 
    [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
    }

    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-baseweb="input"] > div {
        background-color: #1f242d !important;
        border-color: #3f4652 !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    .stTextInput input,
    .stNumberInput input {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        background-color: transparent !important;
        caret-color: #FFFFFF !important;
    }

    div[data-baseweb="input"] input::placeholder,
    div[data-baseweb="base-input"] input::placeholder {
        color: #9ea7b3 !important;
        -webkit-text-fill-color: #9ea7b3 !important;
    }

    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        color: #FFFFFF !important;
        background-color: #2d333f !important;
        border-color: #3f4652 !important;
    }

    button[data-testid="stNumberInputStepDown"] svg,
    button[data-testid="stNumberInputStepUp"] svg {
        fill: #FFFFFF !important;
    }

    /* ------------------------------------------------------------------ */
    /* UNIFORM DARK BUTTONS & FILE UPLOADER                               */
    /* ------------------------------------------------------------------ */

    /* Target standard buttons, file dropzone, and form submit buttons */
    .stButton > button,
    div[data-testid="stFormSubmitButton"] > button,
    div[data-testid="stFileUploader"] section {
        background-color: #1c1f1d !important;
        color: #ffffff !important;
        border: 1px solid #3f4652 !important; /* Muted gray border instead of pure white */
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Target the 'Browse files' button inside the File Uploader */
    div[data-testid="stFileUploader"] section button {
        background-color: #2b303c !important;
        color: #ffffff !important;
        border: 1px solid #3f4652 !important;
    }

    /* Hover states for all buttons and file dropzone */
    .stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover,
    div[data-testid="stFileUploader"] section:hover {
        background-color: #2b303c !important;
        border-color: #605D5C !important;
        color: #ffffff !important;
    }


    /* ------------------------------------------------------------------ */
    /* TARGETS SPECIFIC ADD SUBSCRIPTION BUTTON                           */
    /* ------------------------------------------------------------------ */

    /* ================================================================== */
    /* ST.DIALOG & MODAL OVERLAY STYLING (For add_subscription_dialog)    */
    /* ================================================================== */

    /* 1. Target the Dialog Backdrop and Content Window */
    div[data-testid="stDialog"] > div:first-child,
    div[role="dialog"] {
        background-color: #121413 !important;
        color: #ffffff !important;
        border: 1px solid #3f4652 !important;
        border-radius: 12px !important;
    }

    /* 2. Target Buttons INSIDE the Dialog (Save Subscription button) */
    div[data-testid="stDialog"] button,
    div[role="dialog"] button,
    div[role="dialog"] button[data-testid="baseButton-secondary"],
    div[role="dialog"] button[data-testid="baseButton-primary"],
    div[role="dialog"] div[data-testid="stFormSubmitButton"] > button {
        background-color: #1c1f1d !important;
        background: #1c1f1d !important;
        color: #ffffff !important;
        border: 1px solid #3f4652 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }

    /* Hover state for dialog buttons */
    div[data-testid="stDialog"] button:hover,
    div[role="dialog"] button:hover {
        background-color: #2b303c !important;
        background: #2b303c !important;
        border-color: #605D5C !important;
        color: #ffffff !important;
    }

    /* Force text & icons inside dialog buttons to stay white */
    div[data-testid="stDialog"] button *,
    div[role="dialog"] button * {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    /* 3. Style form input fields inside the dialog to match dark theme */
    div[role="dialog"] input,
    div[role="dialog"] div[data-baseweb="select"] {
        background-color: #1c1f1d !important;
        color: #ffffff !important;
        border-color: #3f4652 !important;
    }
    .metric-card-large {
        background: linear-gradient(155deg, #32373D 30%, #D64218 100%) !important;
        border: 1px solid #30363d !important;
        border-radius: 12px;
        padding: 32px 24px;
        min-height: 380px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }

    .metric-card-small {
        background: linear-gradient(145deg, #D64218 20%, #3F3C3A 70%) !important;
        border: 1px solid #30363d !important;
        border-radius: 50px;
        padding: 16px 20px;
        min-height: 184px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }

    .metric-title {
        font-size: 1.25rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        color: #8b949e !important;
        text-transform: uppercase;
    }

    .metric-value-lg {
        font-size: 4.2rem;
        font-weight: 700;
        color: #ffffff !important;
        margin-top: 8px;
    }

    .metric-value-sm {
        font-size: 2.2rem;
        font-weight: 700;
        margin-top: 4px;
    }

    .action-btn-container [data-testid="stColumn"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important; 
    }

    .action-btn-container .stButton > button {
        background-color: #21262d !important;
        color: #ffffff !important;
        border: 1px solid #363b42 !important;
        border-radius: 6px !important;
        padding: 4px 10px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        min-height: 34px !important;
        width: 120px !important;
        max-width: 100% !important;
        transition: all 0.2s ease-in-out !important;
    }

    .action-btn-container .stButton > button:hover {
        background-color: #30363d !important;
        border-color: #8b949e !important;
        transform: translateY(-1px);
    }

    /* ------------------------------------------------------------------ */
/* LOGOUT BUTTON - FAR RIGHT ALIGNMENT                                */
/* ------------------------------------------------------------------ */

    /* 1. Force the parent Streamlit column to push content to the far right */
    div[data-testid="stColumn"]:has(.logout-btn-wrapper) {
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        width: 100% !important;
        margin-left: auto !important;
    }

    /* 2. Style the outer wrapper to occupy full column space and right-align */
    .logout-btn-wrapper {
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        width: 100% !important;
        margin-left: auto !important;
        margin-right: 0 !important;
    }

    /* 3. Override Streamlit's inner element container rules */
    .logout-btn-wrapper [data-testid="stElementContainer"],
    .logout-btn-wrapper [data-testid="element-container"], 
    .logout-btn-wrapper .stButton {
        width: auto !important; 
        margin-left: auto !important;
        margin-right: 0 !important;
    }

    /* 4. Target the actual button element */
    .logout-btn-wrapper .stButton > button {
        background-color: #e53e3e !important;
        color: #ffffff !important;
        border: 1px solid #e53e3e !important;
        border-radius: 6px !important;
        padding: 6px 16px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        min-height: 34px !important;
        width: 110px !important;
        margin-left: auto !important;
        margin-right: 0 !important;
        display: block !important;
    }

    .logout-btn-wrapper .stButton > button:hover {
        background-color: #c53030 !important;
        border-color: #c53030 !important;
        transform: translateY(-1px);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #32373D !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }

    /* Custom Width for ONLY the Cards Box */
    .st-key-cards_sidebar_box {
        width: 90% !important;        /* Or exact pixels like 350px */
        max-width: 550px !important;    /* Cap maximum expansion */
        margin-right: 10px !important;
    }
       
    div[data-testid="stVegaLiteChart"],
    div[data-testid="stVegaLiteChart"] > div,
    div[data-testid="stVegaLiteChart"] svg,
    div[data-testid="stVegaLiteChart"] canvas {
        background-color: #32373D !important;
        background: #32373D !important;
    }

    .st-key-recent_transactions_container {
        background-color: #32373D !important;
        border: 1px solid #605D5C !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }

    .st-key-recent_transactions_container [data-testid="stDataFrame"] {
        background-color: transparent !important;
    }

    .st-key-recent_transactions_container [data-testid="stTable"] th,
    .st-key-recent_transactions_container [data-testid="stTable"] td {
        color: #ffffff !important;
    }

    /* ------------------------------------------------------------------ */
    /* 1. EXPAND MAIN CONTAINER TO FULL WIDTH                             */
    /* ------------------------------------------------------------------ */
    
    .stAppViewContainer > .main,
    div[data-testid="stMainBlockContainer"],
    .block-container {
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 1rem !important;
    }

    /* ------------------------------------------------------------------ */
    /* 2. CENTERED NAV BAR                                                */
    /* ------------------------------------------------------------------ */

    div[data-testid="stTabs"] {
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
    }

    div[data-testid="stTabList"], 
    div[role="tablist"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: fit-content !important; 
        margin-left: auto !important;
        margin-right: auto !important;
        margin-bottom: 24px !important;
        background-color: #1f242d !important;
        border-radius: 16px !important;
        border: 1px solid #3f4652 !important;
        padding: 6px 16px !important;
        gap: 8px !important;
    }

    div[data-testid="stTabList"] button,
    div[role="tablist"] button {
        flex: 0 1 auto !important;
        text-align: center !important;
        justify-content: center !important; 
    }

    /* ------------------------------------------------------------------ */
    /* 3. EVENLY SPACED 100% FULL WIDTH DASHBOARD CONTENT                 */
    /* ------------------------------------------------------------------ */

    div[data-testid="stTabPanel"],
    div[role="tabpanel"] {
        width: 100% !important;
        max-width: 100% !important;
        padding: 0 !important;
    }

    div[data-testid="stTabPanel"] div[data-testid="stHorizontalBlock"] {
        width: 100% !important;
        max-width: 100% !important;
        justify-content: space-between !important;
        gap: 2rem !important;
    }

    div[data-testid="stTabPanel"] div[data-testid="stVegaLiteChart"],
    div[data-testid="stTabPanel"] div[data-testid="stDataFrame"],
    div[data-testid="stTabPanel"] .st-key-recent_transactions_container,
    div[data-testid="stTabPanel"] div[data-testid="stVerticalBlockBorderWrapper"] {
        width: 100% !important;
        max-width: 100% !important;
    }

</style>
""", unsafe_allow_html=True)

cookie_manager = stx.CookieManager(key="ledgeai_cookie_mgr")

# 1. Auth state initialization
if "token" not in st.session_state or not st.session_state["token"]:
    saved_token = cookie_manager.get(cookie="ledgeai_token")
    st.session_state["token"] = saved_token if saved_token else None

# 2. Login / Register Guard
if not st.session_state.get("token"):
    with st.container():
        st.info("Welcome! Sign in to access your financial command center.")
        tab_login, tab_reg = st.tabs(["Sign In", "Register"])
        
        with tab_login:
            username = st.text_input("Username", key="l_user")
            password = st.text_input("Password", type="password", key="l_pass")
            if st.button("Sign In"):
                login_data = {"username": username, "password": password}
                res = requests.post(f"{API_URL}/auth/login", data=login_data)

                if res.status_code == 200:
                    token = res.json().get("access_token", "").strip()
                    st.session_state["token"] = token
                    cookie_manager.set("ledgeai_token", token, key="set_token_login", max_age=604800)
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

        with tab_reg:
            r_user = st.text_input("Username", key="r_user")
            r_email = st.text_input("Email", key="r_email")
            r_pass = st.text_input("Password", type="password", key="r_pass")
            if st.button("Create Account"):
                res = requests.post(f"{API_URL}/auth/register", json={"username": r_user, "email": r_email, "password": r_pass})
                if res.status_code in (200, 201):
                    token = res.json().get("access_token", "").strip()
                    st.session_state["token"] = token
                    cookie_manager.set("ledgeai_token", token, key="set_token_reg", max_age=604800)
                    st.rerun()
                else:
                    st.error("Registration failed.")
        st.stop()

# ------------------------------------------------------------------------------
# 3. HELPER DATA FETCHING
# ------------------------------------------------------------------------------
headers = {
    "Authorization": f"Bearer {st.session_state['token']}",
    "Content-Type": "application/json"
}

def fetch_data(endpoint: str):
    try:
        url = f"{API_URL}/{endpoint}" if not endpoint.startswith("http") else endpoint
        res = requests.get(url, headers=headers)
        
        if res.status_code == 200:
            return res.json()
        elif res.status_code == 401:
            st.error("🔒 Session expired or unauthorized. Please log in again.")
            return []
        else:
            return []
    except Exception as e:
        st.error(f"Connection error: {e}")
        return []
    
# Fetch shared data up-front
budgets = fetch_data("budgets")
incomes = fetch_data("income")
invoices = fetch_data("invoices")
expenses = fetch_data("budgets/expenses")

# ------------------------------------------------------------------------------
# 4. TOP NAVIGATION BAR & LOGOUT HEADER
# ------------------------------------------------------------------------------
header_col, logout_col = st.columns([10, 1], vertical_alignment="center")

with header_col:
    st.markdown("<h2 style='margin:0; padding:0; text-align: left;'>💰 LedgeAI</h2>", unsafe_allow_html=True)

with logout_col:
    st.markdown('<div class="logout-btn-wrapper">', unsafe_allow_html=True)
    if st.button("Logout", key="btn_logout"):
        st.session_state["token"] = None
        cookie_manager.delete("ledgeai_token")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
# ------------------------------------------------------------------------------
# 5. NAVIGATION BAR
# ------------------------------------------------------------------------------
tab_dash, tab_stats, tab_tx, tab_wallet, tab_statements = st.tabs([
        "📊 Overview", 
        "💵 Statistics", 
        "🎯 Transactions", 
        "💳 My Wallet",
        "📑 Statements & AI"
    ])
st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
# ------------------------------------------------------------------------------
# 6. TAB ROUTING & VIEWS
# ------------------------------------------------------------------------------

# --- DASHBOARD / OVERVIEW VIEW ---
with tab_dash:
    paid_invoices = sum(inv.get("amount", 0.0) for inv in invoices if inv.get("status") == "paid")
    additional_income = sum(inc.get("amount", 0.0) for inc in incomes)
    total_income = paid_invoices + additional_income
    actual_expense_sum = sum(float(e.get("amount", 0.0)) for e in expenses)
    
    total_expense = actual_expense_sum
    total_balance = total_income - total_expense
    
    col_dashboard, col_sidebar_panel = st.columns([2, 1])
    
    # Left Column (2/3 Screen)
    with col_dashboard: 
        st.title("💰 LedgeAI Overview")
            
        # Metrics Row
        col_main_bal, col_stacked = st.columns([1.5, 1])
                
        with col_main_bal:
            balance_color = "#e53e3e" if total_balance < 0 else "#ffffff"
            st.markdown(f"""
                <div class="metric-card-large">
                <div class="metric-title">Total Balance</div>
                <div class="metric-value-lg" style="color: {balance_color} !important;">
                    ${total_balance:,.2f}
                </div>
                </div>
                """, unsafe_allow_html=True)
    
            st.markdown('<div class="action-btn-container" style="margin-top: -60px; padding: 0 16px 16px 16px;">', unsafe_allow_html=True)
            _, btn_col1, btn_col2, _ = st.columns([1, 1, 1, 1])

            with btn_col1:
                if st.button("💳 Add Funds", key="btn_topup"):
                    show_topup_dialog(API_URL, headers)

            with btn_col2:
                if st.button("➕ Add Expense", key="btn_add_expense"):
                    show_expense_dialog(API_URL, headers)

            st.markdown('</div>', unsafe_allow_html=True)

        with col_stacked:
            st.markdown(f"""
            <div class="metric-card-small">
                <div class="metric-title">Income</div>
                <div class="metric-value-sm" style="color: #38a169 !important;">
                    +${total_income:,.2f}
                </div>
            </div>
            <div class="metric-card-small" style="margin-bottom: 0;">
                <div class="metric-title">Expense</div>
                <div class="metric-value-sm" style="color: #e53e3e !important;">
                    -${total_expense:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

        # Charts Row
        col_rev_chart, col_exp_chart = st.columns([1.5, 1], vertical_alignment="top")

        with col_rev_chart: 
            render_revenue_chart(lambda group_by: api.get_revenue_flow(group_by=group_by))
        with col_exp_chart: 
            render_expense_chart(lambda period: api.get_expense_breakdown(period=period))

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

        # Recent Transactions
        with st.container(border=True, key="recent_transactions_container"):
            st.markdown("<h4 style='margin:0; padding-bottom:12px; color:#ffffff; font-weight: 600;'>Recent Transactions</h4>", unsafe_allow_html=True)

            def get_exact_post_date(item):
                raw_date = item.get("created_at") or item.get("date") or item.get("issue_date") or item.get("timestamp")
                if not raw_date:
                    return pd.NaT
                try:
                    return pd.to_datetime(raw_date)
                except Exception:
                    return pd.NaT
                
            all_transactions = []

            for inc in incomes: 
                post_dt = get_exact_post_date(inc)
                all_transactions.append({
                    "Date": post_dt.strftime("%Y-%m-%d") if pd.notna(post_dt) else "N/A",
                    "Description": inc.get("source") or inc.get("description") or "Income Entry", 
                    "Category": "Income",
                    "Amount": f"+${inc.get('amount', 0.0):,.2f}",
                    "Status": "Completed"
                })

            for inv in invoices:
                raw_date = inv.get("issued_date") or inv.get("created_at") or inv.get("date")
                post_dt = pd.to_datetime(raw_date, errors="coerce") if raw_date else pd.NaT

                all_transactions.append({
                    "Date": post_dt.strftime("%Y-%m-%d") if pd.notna(post_dt) else "N/A",
                    "Description": f"Invoice: {inv.get('client_name', 'Client')}",
                    "Category": "Invoice",
                    "Amount": f"+${inv.get('amount', 0.0):,.2f}",
                    "Status": str(inv.get("status", "Pending")).capitalize()
                })

            for b in budgets:
                raw_date = b.get("created_at") or b.get("date")
                post_dt = pd.to_datetime(raw_date) if raw_date else pd.NaT
                cat = b.get("category", "Expense")
                notes = b.get("notes") or f"{cat} Budget Limit"

                all_transactions.append({
                    "Date": post_dt.strftime("%Y-%m-%d") if pd.notna(post_dt) else "N/A",
                    "Description": notes,
                    "Category": f"Expense ({cat})",
                    "Amount": f"-${b.get('monthly_limit', 0.0):,.2f}",
                    "Status": "Allocated"
                })

            for exp in expenses: 
                raw_date = exp.get("created_at") or exp.get("date")
                post_dt = pd.to_datetime(raw_date) if raw_date else pd.NaT

                all_transactions.append({
                    "Date": post_dt.strftime("%Y-%m-%d") if pd.notna(post_dt) else "N/A",
                    "Description": exp.get("description", "Expense Entry"),
                    "Category": f"Expense ({exp.get('category', 'General')})",
                    "Amount": f"-${float(exp.get('amount', 0.0)):,.2f}",
                    "Status": "Completed"
                })

            if all_transactions: 
                df_tx = pd.DataFrame(all_transactions)
                df_tx = df_tx.sort_values(by="Date", ascending=False, na_position="last")
                st.dataframe(
                    df_tx, 
                    width="stretch", 
                    hide_index=True, 
                    column_config={
                        "Date": st.column_config.TextColumn("Date", width="small"),
                        "Description": st.column_config.TextColumn("Description", width="medium"),
                        "Amount": st.column_config.TextColumn("Amount", width="small"), 
                        "Status": st.column_config.TextColumn("Status", width="small")
                    }
                )
            else:
                st.info("No recent transactions found.")

    # Right Column (1/3 Screen)
    with col_sidebar_panel: 
        with st.container(border=True, key="cards_sidebar_box"):
            header_col, btn_col = st.columns([2, 1], vertical_alignment="center")
            with header_col:
                st.subheader("💳 Cards")
            with btn_col:
                if st.button("➕ Add", use_container_width='stretch', key="add_card_panel_btn"):
                    add_card_dialog(API_URL, headers)

            st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

            cards = fetch_data("cards")
            selected_card_id = render_interactive_cards(cards, API_URL, headers)

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        with st.container(border=True):
            sub_title_col, sub_btn_col = st.columns([3, 1], vertical_alignment="center")
            with sub_title_col: 
                st.markdown("<h4 style='margin:0; font-weight:600;'>🔄 Active Subscriptions</h4>", unsafe_allow_html=True)
            # Replace your current sub_btn_col block with this:
            with sub_btn_col:
                st.markdown("""
                        <style>
                        .dark-sub-btn button {
                            background-color: #1c1f1d !important;
                            background: #1c1f1d !important;
                            color: #ffffff !important;
                            border: 1px solid #3f4652 !important;
                            border-radius: 8px !important;
                            font-weight: 600 !important;
                        }
                        .dark-sub-btn button:hover {
                            background-color: #2b303c !important;
                            border-color: #605D5C !important;
                        }
                        .dark-sub-btn button * {
                            color: #ffffff !important;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                st.markdown('<div class="dark-sub-btn">', unsafe_allow_html=True)
                if st.button("➕ Add", key="btn_add_sub_inline", use_container_width='stretch'):
                    add_subscription_dialog(cards, API_URL, headers, active_card_id=selected_card_id)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
            
            has_any_subscriptions = False

            if cards:
                for card in cards:
                    card_id = card.get("id")
                    card_num = str(card.get('card_number', ''))
                    last_four = card_num[-4:] if len(card_num) >= 4 else "----"
                    card_label = f"{str(card.get('card_type', 'Card')).upper()} •••• {last_four}"

                    card_subs = fetch_data(f"cards/{card_id}/subscriptions")

                    if isinstance(card_subs, dict) and "subscriptions" in card_subs:
                        card_subs = card_subs["subscriptions"]

                    if isinstance(card_subs, list) and len(card_subs) > 0:
                        active_subs = [s for s in card_subs if str(s.get("status", "active")).lower() == "active"]

                        if active_subs:
                            has_any_subscriptions = True
                            st.markdown(
                                f"<div style='font-size:0.8rem; font-weight:600; color:#8b949e; margin-top:12px; margin-bottom:6px;'>"
                                f"💳 {card_label}</div>", 
                                unsafe_allow_html=True
                            )

                            for sub in active_subs:
                                sub_name = sub.get('name') or sub.get('title') or sub.get('service') or 'Subscription'
                                sub_cycle = sub.get('billing_cycle') or sub.get('frequency') or 'monthly'
                                try:
                                    sub_amount = float(sub.get('amount') or sub.get('price') or sub.get('cost') or 0.0)
                                except (ValueError, TypeError):
                                    sub_amount = 0.0

                                st.markdown(f"""
                                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; margin-bottom: 8px; background-color: rgba(255, 255, 255, 0.04); border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.08);">
                                        <div>
                                            <div style="font-weight: 600; color: #ffffff; font-size: 0.95rem;">{sub_name}</div>
                                            <div style="font-size: 0.78rem; color: #8b949e;">Renews {str(sub_cycle).capitalize()}</div>
                                        </div>
                                        <div style="font-weight: 700; color: #e53e3e; font-size: 1rem;">
                                            -${sub_amount:,.2f}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)

            if not has_any_subscriptions:
                st.info("No active subscriptions found.")

# --- STATISTICS VIEW ---
with tab_stats:
    render_income_manager(API_URL, headers, incomes)

# --- TRANSACTIONS VIEW ---
with tab_tx:
    st.subheader("🎯 All Transactions")
    st.info("Transaction history management view.")

# --- MY WALLET VIEW ---
with tab_wallet:
    render_budget_manager(API_URL, headers, budgets)

# --- STATEMENTS & RAG VIEW ---
with tab_statements:
    st.subheader("📑 Bank Statement Processing & AI Sync")
    st.caption("Upload monthly bank statements (PDF or CSV) to automatically extract, categorize, and index transactions.")

    col_upload, col_review = st.columns([1, 2])

    with col_upload:
        with st.container(border=True):
            st.markdown("<h4 style='margin:0; font-weight:600;'>1. Upload File</h4>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Choose PDF or CSV Statement", 
                type=["pdf", "csv"], 
                help="Supports standard bank statement formats."
            )

            if uploaded_file is not None:
                st.write(f"📁 **File:** `{uploaded_file.name}`")

                if st.button("🔍 Parse Statement", type="primary", use_container_width='stretch'):
                    # Exclude Content-Type header so requests computes multipart boundary
                    auth_headers = {"Authorization": f"Bearer {st.session_state['token']}"}
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

                    with st.spinner("Extracting transactions..."):
                        try:
                            res = requests.post(f"{API_URL}/statements/upload", files=files, headers=auth_headers)
                            if res.status_code in (200, 201):
                                data = res.json()
                                st.session_state["parsed_statement_data"] = data.get("transactions", [])
                                st.success(f"Extracted {data.get('total_extracted', 0)} transactions!")
                                st.rerun()
                            else:
                                st.error(f"Failed to parse statement: {res.text}")
                        except Exception as err:
                            st.error(f"Connection error: {err}")

    with col_review:
        with st.container(border=True):
            st.markdown("<h4 style='margin:0; font-weight:600;'>2. Review & Confirm Transactions</h4>", unsafe_allow_html=True)
            
            if "parsed_statement_data" in st.session_state and st.session_state["parsed_statement_data"]:
                df_parsed = pd.DataFrame(st.session_state["parsed_statement_data"])

                edited_df = st.data_editor(
                    df_parsed,
                    num_rows="dynamic",
                    use_container_width='stretch',
                    column_config={
                        "transaction_type": st.column_config.SelectboxColumn(
                            "Type",
                            options=["income", "expense"],
                            required=True
                        ),
                        "category": st.column_config.SelectboxColumn(
                            "Category",
                            options=["Software & Tech", "Office Supplies", "Freelance Pay", "Meals & Entertainment", "Travel", "Uncategorized"],
                            required=True
                        ),
                        "amount": st.column_config.NumberColumn(
                            "Amount ($)",
                            format="$%.2f"
                        )
                    }
                )

                st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)

                if st.button("✅ Confirm & Sync to Ledger", use_container_width='stretch'):
                    payload = {
                        "transactions": edited_df.to_dict(orient="records")
                    }

                    with st.spinner("Syncing transactions to your database..."):
                        try:
                            sync_res = requests.post(f"{API_URL}/statements/confirm", json=payload, headers=headers)
                            if sync_res.status_code in (200, 201):
                                st.balloons()
                                st.success("Ledger updated successfully!")
                                del st.session_state["parsed_statement_data"]
                                st.rerun()
                            else:
                                st.error(f"Error syncing data: {sync_res.text}")
                        except Exception as sync_err:
                            st.error(f"Connection error: {sync_err}")
            else:
                st.info("Upload a statement on the left to preview extracted transactions here.")
                

            


