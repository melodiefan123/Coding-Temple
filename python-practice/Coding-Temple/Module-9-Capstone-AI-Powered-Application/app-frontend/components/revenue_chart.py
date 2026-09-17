import pandas as pd
import streamlit as st
import altair as alt

def render_revenue_chart(fetch_revenue_fn):
    CARD_BG = "#32373D"       # Main card background
    HEADER_BG = "#21262D"     # Distinct background behind title + chart
    BAR_COLOR = "#D64218"

    # Selectbox alignment CSS
    st.markdown(f"""
            <style>
                /* 1. Target the exact container card by key */
                .st-key-revenue_card_container {{
                    background-color: {CARD_BG} !important;
                    border: 1px solid #605D5C !important;
                    border-radius: 12px !important;
                    padding: 20px !important;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                }}
    
                /* 2. Selectbox styling inside this card */
                .st-key-revenue_card_container div[data-testid="stSelectbox"] > div > div {{
                    background-color: {HEADER_BG} !important;
                    border: 1px solid #363b42 !important;
                    border-radius: 6px !important;
                    color: #f0f6fc !important;
                    font-size: 0.85rem !important;
                }}
    
                /* 3. Match chart canvas background to card */
                .st-key-revenue_card_container div[data-testid="stVegaLiteChart"],
                .st-key-revenue_card_container div[data-testid="stVegaLiteChart"] canvas {{
                    background-color: {CARD_BG} !important;
                }}
            </style>
        """, unsafe_allow_html=True)

    with st.container(border=True, key="revenue_card_container"):
        # Top bar with just the dropdown align right
        _, col_dropdown = st.columns([2.5, 1])
        with col_dropdown:
            selected_view = st.selectbox(
                label="Select View",
                options=["Monthly", "Weekly"],
                index=0,
                label_visibility="collapsed",
                key="revenue_dropdown_select"
            )

        revenue_data = fetch_revenue_fn(group_by=selected_view.lower())
        if not revenue_data:
            st.info("No revenue data recorded yet.")
            return

        df = pd.DataFrame(revenue_data)
        if "date" in df.columns and "revenue" in df.columns:
            df["formatted_revenue"] = df["revenue"].apply(
                lambda x: f"${x/1000:.1f}k" if x >= 1000 else f"${int(x)}"
            )

            # Chart with native title embedded inside
            base = alt.Chart(df, title=alt.TitleParams(
                text="Revenue Flow",
                anchor="start",
                color="#FFFFFF",
                fontSize=16,
                fontWeight="bold",
                dy=-10
            )).encode(
                x=alt.X(
                    "date:N",
                    title=None,
                    axis=alt.Axis(
                        labelAngle=0,
                        labelColor="#8b949e",
                        labelFontSize=11,
                        tickColor="transparent",
                        domainColor="#30363d"
                    )
                ),
                y=alt.Y("revenue:Q", axis=None)
            )

            bars = base.mark_bar(
                cornerRadiusTopLeft=6,
                cornerRadiusTopRight=6,
                color=BAR_COLOR,
                size=32
            )

            text = base.mark_text(
                align="center",
                baseline="top",
                dy=8,
                color="#ffffff",
                fontSize=11,
                fontWeight="bold"
            ).encode(
                text="formatted_revenue:N"
            )

            # Configure unified background for Title + Chart canvas
            chart = (
                alt.layer(bars, text)
                .properties(height=240)
                .configure_view(
                    fill=HEADER_BG,  # Injected background color behind title & bars
                    strokeWidth=0
                )
                .configure(
                    background=HEADER_BG
                )
            )

            st.altair_chart(chart, width="content", theme=None)