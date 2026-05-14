# Create my_dashboard.py - a personal stats dashboard about any topic: study progress, fitness goals, reading list, project tracker, or anything with numbers you can display.



# Requirements:


# Data can be hardcoded - the focus is on layout, not data fetching

import streamlit as st

# st.set_page_config() with layout="wide" and a relevant title/icon
st.set_page_config(
    page_title="My Dashboard",      # Browser tab title
    page_icon="📊",                 # Browser tab icon
    layout="wide",                  # Use full browser width (default is "centered")
    initial_sidebar_state="expanded" # Sidebar starts open
)

# Sidebar with at least 2 controls (selectbox, slider, radio, checkbox) that affect the main content
st.sidebar.title("Controls")
date_range = st.sidebar.selectbox("Water Intake", ["High", "Medium", "Low"])
spending_chart = st.sidebar.checkbox("Show Chart", value=True)
if spending_chart:
    if date_range == "High":
        st.bar_chart({"Water Intake": [8, 9, 10, 8, 9]})
    elif date_range == "Medium":
        st.bar_chart({"Water Intake": [5, 4, 6, 5, 4]})
    elif date_range == "Low":
        st.bar_chart({"Water Intake": [2, 1, 3, 2, 1]})
# Metrics row - at least 3 st.metric() cards in a st.columns() row, with delta values
col1, col2, col3 = st.columns(3)

with col1: 
    st.metric("Water Intake", "2", "+1%")
with col2: 
    st.metric("Books Read", "3", "+33%")
with col3: 
    st.metric("Tasks", "15", "-4")

# 2 tabs with different content in each (e.g., "Overview" and "Details")
tab1, tab2 = st.tabs(["Overview", "Details"])
with tab1: 
    st.write("High-level summary")
with tab2: 
    st.write("Detailed breakdown.")

# 1 expander with supplementary information
with st.expander("Settings"):
    profile = st.checkbox("Show Notifications", value=True)
    st.write("Settings are hidden by default to keep the UI clean")
