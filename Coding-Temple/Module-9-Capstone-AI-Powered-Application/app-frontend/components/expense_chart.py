import pandas as pd
import streamlit as st
import altair as alt

def render_expense_chart(fetch_expense_fn):
    """
    Renders an Expense Split Donut Chart inside a single unified card box 
    using Streamlit's native key-based container targeting.
    """
    CARD_BG = "#32373D"     # Main card background
    INNER_BG = "#21262D"    # Selectbox inner background

    st.markdown(f"""
        <style>
            /* 1. Target the exact container card by key */
            .st-key-expense_card_container {{
                background-color: {CARD_BG} !important;
                border: 1px solid #605D5C !important;
                border-radius: 12px !important;
                padding: 20px !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }}

            /* 2. Selectbox styling inside this card */
            .st-key-expense_card_container div[data-testid="stSelectbox"] > div > div {{
                background-color: {INNER_BG} !important;
                border: 1px solid #363b42 !important;
                border-radius: 6px !important;
                color: #f0f6fc !important;
                font-size: 0.85rem !important;
            }}

            /* 3. Match chart canvas background to card */
            .st-key-expense_card_container div[data-testid="stVegaLiteChart"],
            .st-key-expense_card_container div[data-testid="stVegaLiteChart"] canvas {{
                background-color: {CARD_BG} !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Key attached directly to st.container isolates all child elements into this styled card
    with st.container(border=True, key="expense_card_container"):
        col_title, col_dropdown = st.columns([2.5, 1])

        with col_title:
            st.markdown(
                "<h4 style='margin: 0; padding-top: 2px; color: #ffffff; font-weight: 600; font-size: 1.1rem;'>Expense Breakdown</h4>",
                unsafe_allow_html=True
            )

        with col_dropdown:
            selected_period = st.selectbox(
                label="Select Period",
                options=["This Month", "Last Month", "Year to Date"],
                index=0,
                label_visibility="collapsed",
                key="expense_dropdown_select"
            )

        expense_data = fetch_expense_fn(period=selected_period)
        if not expense_data:
            st.info("No expense records found for this timeframe.")
            return

        df = pd.DataFrame(expense_data)

        if "category" in df.columns and "amount" in df.columns:
            total_expense = df["amount"].sum()

            df["percentage"] = (df["amount"] / total_expense) * 100
            df["formatted_amount"] = df["amount"].apply(lambda x: f"${x:,.0f}")
            df["formatted_pct"] = df["percentage"].apply(lambda x: f"{x:.1f}%")

            # 1. Base Donut Arc
            donut = alt.Chart(df).mark_arc(
                innerRadius=65,
                outerRadius=95,
                cornerRadius=4,
                padAngle=0.03
            ).encode(
                theta=alt.Theta("amount:Q"),
                color=alt.Color(
                    "category:N",
                    scale=alt.Scale(scheme="tableau10"),
                    legend=alt.Legend(
                        orient="right",
                        labelColor="#f0f6fc",
                        labelFontSize=12,
                        title=None,
                        symbolType="circle",
                        symbolSize=100
                    )
                ),
                tooltip=[
                    alt.Tooltip("category:N", title="Category"),
                    alt.Tooltip("formatted_amount:N", title="Spent"),
                    alt.Tooltip("formatted_pct:N", title="Share")
                ]
            )

            # 2. Total Amount Center Label
            center_total = alt.Chart(pd.DataFrame([{"text": f"${total_expense:,.0f}"}])).mark_text(
                align="center",
                baseline="middle",
                fontSize=20,
                fontWeight="bold",
                color="#ffffff",
                dy=-8
            ).encode(text="text:N")

            # 3. Subtitle Center Label ("Total Spent")
            center_subtitle = alt.Chart(pd.DataFrame([{"text": "Total Spent"}])).mark_text(
                align="center",
                baseline="middle",
                fontSize=11,
                color="#8b949e",
                dy=12
            ).encode(text="text:N")

            # Combine chart layers
            chart = (
                alt.layer(donut, center_total, center_subtitle)
                .properties(height=230)
                .configure_view(
                    fill=CARD_BG,
                    strokeWidth=0
                )
                .configure(
                    background=CARD_BG
                )
            )

            st.altair_chart(chart, width="stretch", theme=None)
        else:
            st.info("Invalid expense data structure.")