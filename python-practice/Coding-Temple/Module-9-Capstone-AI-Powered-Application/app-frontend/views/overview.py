import streamlit as st
import plotly.graph_objects as go
st.markdown("""
<style>
    /* 1. Labels above input fields */
    div[data-widget="stTextInput"] label,
    div[data-widget="stNumberInput"] label,
    div[data-widget="stSelectbox"] label,
    div[data-testid="stWidgetLabel"] p {
        color: #FFFFFF !important;
    } 
</style>
""", unsafe_allow_html=True)

def render_overview(budgets, incomes, invoices):
    # Calculate Totals
    paid_invoices_sum = sum(inv.get("amount", 0.0) for inv in invoices if inv.get("status") == "paid")
    additional_income_sum = sum(inc.get("amount", 0.0) for inc in incomes)
    total_income = paid_invoices_sum + additional_income_sum
    total_budgeted = sum(b.get("monthly_limit", 0.0) for b in budgets)

    # 1. Top Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Income", f"${total_income:,.2f}")
    m2.metric("Total Budgeted", f"${total_budgeted:,.2f}")
    m3.metric("Invoice Earnings", f"${paid_invoices_sum:,.2f}")
    m4.metric("Additional Income", f"${additional_income_sum:,.2f}")

    st.divider()

    # 2. Circular Gauge & Donut Charts
    col_gauge, col_donut = st.columns(2)

    with col_gauge:
        st.subheader("Budget vs Income Gauge")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total_budgeted,
            number={'prefix': "$", 'valueformat': ",.2f"},
            title={'text': f"Target Income: ${total_income:,.2f}"},
            gauge={
                'axis': {'range': [None, max(total_income, total_budgeted, 1.0)]},
                'bar': {'color': "#3182ce"},
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': total_income
                }
            }
        ))
        fig_gauge.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_donut:
        st.subheader("Income Source Distribution")
        fig_donut = go.Figure(data=[go.Pie(
            labels=["Paid Invoices", "Additional Income"],
            values=[paid_invoices_sum, additional_income_sum],
            hole=0.6,
            marker=dict(colors=["#3182ce", "#38a169"])
        )])
        fig_donut.update_layout(height=320, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_donut, use_container_width=True)