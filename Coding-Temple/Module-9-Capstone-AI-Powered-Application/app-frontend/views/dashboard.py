import streamlit as st
import requests
import plotly.graph_objects as go

API_URL = "http://localhost:8000"

st.set_page_config(page_title="LedgeAI - Dashboard", page_icon="📊", layout="wide")

st.title("📊My Dashboard")

# 1. Require Authentication
if "token" not in st.session_state or not st.session_state["token"]:
    st.warning("Please log in on the Authentication page to view your dashboard.")
    st.stop()

headers = {
    "Authorization": f"Bearer {st.session_state['token']}",
    "Content-Type": "application/json"
}

# 2. Fetch User Budgets
def fetch_budgets():
    try:
        res = requests.get(f"{API_URL}/budgets/", headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()
        return []
    except Exception:
        return []

budgets = fetch_budgets()

# 3. Interactive Income & Expense Controls
st.sidebar.header("💰 Financial Inputs")
income = st.sidebar.number_input("Monthly Income ($)", min_value=0.0, value=5000.0, step=100.0)
spent_so_far = st.sidebar.number_input("Spent So Far ($)", min_value=0.0, value=1800.0, step=50.0)

# Calculate totals
total_budgeted = sum(b.get("monthly_limit", 0.0) for b in budgets)
budget_remaining = max(total_budgeted - spent_so_far, 0.0)
income_left = max(income - spent_so_far, 0.0)
budget_used_pct = (spent_so_far / total_budgeted * 100) if total_budgeted > 0 else 0.0

# 4. Top Summary Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Monthly Income", f"${income:,.2f}")
c2.metric("Total Budgeted", f"${total_budgeted:,.2f}")
c3.metric("Spent So Far", f"${spent_so_far:,.2f}")
c4.metric("Budget Remaining", f"${budget_remaining:,.2f}")

st.divider()

# 5. Circular Percentage Visuals
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🎯 Overall Budget Usage Gauge")
    
    # Circular Gauge Chart
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=spent_so_far,
        number={'prefix': "$", 'valueformat': ",.2f"},
        delta={'reference': total_budgeted, 'position': "top", 'relative': False},
        title={'text': f"Budget Limit: ${total_budgeted:,.2f}"},
        gauge={
            'axis': {'range': [None, max(total_budgeted, spent_so_far, 1.0)]},
            'bar': {'color': "#3182ce"},
            'steps': [
                {'range': [0, total_budgeted * 0.75], 'color': "#e6fffa"},
                {'range': [total_budgeted * 0.75, total_budgeted], 'color': "#feebc8"},
                {'range': [total_budgeted, max(total_budgeted * 1.25, spent_so_far)], 'color': "#fed7d7"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': total_budgeted
            }
        }
    ))
    fig_gauge.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_right:
    st.subheader("🍩 Cash Breakdown (Spent vs Left vs Income)")
    
    # Donut Percentage Chart
    labels = ["Amount Spent", "Remaining Budget", "Unallocated Income"]
    values = [spent_so_far, budget_remaining, max(income_left - budget_remaining, 0.0)]
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=["#e53e3e", "#38a169", "#cbd5e0"]),
        textinfo="percent+label",
        hoverinfo="label+value+percent"
    )])
    
    fig_donut.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=30, b=20),
        annotations=[{
            'text': f"{budget_used_pct:.1f}%<br>Used",
            'x': 0.5, 'y': 0.5,
            'font_size': 20,
            'showarrow': False
        }]
    )
    st.plotly_chart(fig_donut, use_container_width=True)

st.divider()

# 6. Category Breakdown Table
st.subheader("📋 Category Budget Allocation")
if budgets:
    formatted_rows = [
        {"Category": b["category"], "Limit": f"${b['monthly_limit']:,.2f}"}
        for b in budgets
    ]
    st.dataframe(formatted_rows, use_container_width=True, hide_index=True)
else:
    st.info("No budget categories found yet.")


# Inside pages/3_Dashboard.py:

# Fetch total from invoices + additional income endpoints
def get_total_combined_income():
    try:
        inv_res = requests.get(f"{API_URL}/invoices/", headers=headers, timeout=5)
        inc_res = requests.get(f"{API_URL}/income/", headers=headers, timeout=5)
        
        invoices_sum = sum(i.get("amount", 0.0) for i in inv_res.json() if i.get("status") == "paid") if inv_res.status_code == 200 else 0.0
        income_sum = sum(i.get("amount", 0.0) for i in inc_res.json()) if inc_res.status_code == 200 else 0.0
        
        return invoices_sum + income_sum
    except Exception:
        return 0.0

# Auto-calculate income for gauge and donut charts
income = get_total_combined_income()