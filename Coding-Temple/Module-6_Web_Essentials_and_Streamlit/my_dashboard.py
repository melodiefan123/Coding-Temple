# Create my_dashboard.py - a personal stats dashboard about any topic: study progress, fitness goals, reading list, project tracker, or anything with numbers you can display.



# Requirements:


# Data can be hardcoded - the focus is on layout, not data fetching

import streamlit as st
import pandas as pd

# st.set_page_config() with layout="wide" and a relevant title/icon
st.set_page_config(
    page_title="My Dashboard",      # Browser tab title
    page_icon="📊",                 # Browser tab icon
    layout="wide",                  # Use full browser width (default is "centered")
    initial_sidebar_state="expanded" # Sidebar starts open
)

# Sidebar with at least 2 controls (selectbox, slider, radio, checkbox) that affect the main content
st.sidebar.title("Dashboard Controls")
intake_level = st.sidebar.selectbox(
                                    "Target Intake Level", 
                                    ["High", "Medium", "Low"], 
                                    help="Filter data view based on daily hydration targets.")

show_chart = st.sidebar.checkbox("Show Progress Chart", value=True, help="Toggle visual charts in the overview tab.")

st.sidebar.divider()
st.sidebar.caption("Use these controls to interactively adjust the dashboard view.")


st.title("📊 Weekly Progress & Personal Stats")
st.markdown("Track your daily hydration, reading goals, and task completions.")
# Metrics row - at least 3 st.metric() cards in a st.columns() row, with delta values
col1, col2, col3 = st.columns(3)

with col1: 
    st.metric(label="Daily Water Intake", value="2.5 L", delta="+0.5 L")
with col2: 
    st.metric(label="Books Read", value="4 Books", delta="+1 this week")
with col3: 
    st.metric(label="Pending Tasks", value="11 Tasks", delta="-4 completed")

st.divider()

# 2 tabs with different content in each (e.g., "Overview" and "Details")
tab1, tab2 = st.tabs(["📈 Overview", "📋 Details & Data"])

chart_data_map = {
    "High": [8, 9, 10, 8, 9, 10, 9],
    "Medium": [5, 6, 5, 6, 5, 4, 6],
    "Low": [2, 3, 2, 1, 3, 2, 2]
}

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

with tab1: 
    st.subheader("Weekly Activity Summary")
    st.write(f"Currently viewing metrics filtered for **{intake_level}** activity levels.")

    if show_chart:
        chart_df = pd.DataFrame({
            "Day": days,
            "Water Intake (Glasses)": chart_data_map[intake_level]
        }).set_index("Day")
        
        st.bar_chart(chart_df)
    else:
        st.info("Chart is currently hidden. Check 'Show Progress Chart' in the sidebar to view.")

with tab2: 
    st.subheader("Detailed Activity Log")
    st.write("A complete breakdown of recorded daily values across all metrics:")

    detailed_df = pd.DataFrame({
        "Day": days,
        "Water Intake (Glasses)": chart_data_map[intake_level],
        "Pages Read": [30, 45, 12, 50, 60, 25, 40],
        "Tasks Completed": [3, 5, 2, 4, 6, 1, 3],
        "Status": ["Goal Met", "Goal Met", "Below Target", "Goal Met", "Goal Met", "Below Target", "Goal Met"]
    })
    
    st.dataframe(
        detailed_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()



# 1 expander with supplementary information
with st.expander("⚙️ User Profile & Dashboard Settings"):
    st.subheader("Preferences & System Status")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        st.write("**User Details:**")
        st.write("• **User:** Student Developer")
        st.write("• **Goal:** Maintain consistent daily health & study habits")
        st.write("• **Last Sync:** Today at 08:00 AM")
        
    with col_exp2:
        notifications_enabled = st.checkbox("Enable Daily Summary Notifications", value=True)
        
        if notifications_enabled:
            st.success("🔔 Notifications are active. You will receive daily progress summaries.")
        else:
            st.warning("🔕 Notifications are muted. You won't receive automated alerts.")
