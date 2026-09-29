import streamlit as st
import pandas as pd
import requests

# Page setup
st.set_page_config(
    page_title="User Data Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

API = "https://jsonplaceholder.typicode.com"

# Cache the API call for 300 seconds (5 minutes) to avoid redundant HTTP requests
# on every user interaction/re-run while ensuring data freshness if remote data changes.
@st.cache_data(ttl=300)
def fetch_users():
    """Fetches user list from API with error handling and a 300s TTL cache."""
    try:
        response = requests.get(f"{API}/users", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch user data: {e}")
        return []

st.title("User Data Explorer")

users = fetch_users()

if not users: 
    st.warning("No user data available.")
else: 
    # Extract & flatten nested JSON structures for clean display
    processed_data = []
    for u in users: 
        processed_data.append({
            "ID": u.get("id"),
            "Name": u.get("name"),
            "Username": u.get("username"),
            "Email": u.get("email"),
            "Phone": u.get("phone"),
            "Website": u.get("website"),
            "City": u.get("address", {}).get("city"),
            "Company": u.get("company", {}).get("name")
        })

    df = pd.DataFrame(processed_data)

    # Sidebar Filter
    st.sidebar.header("Filter Options")
    name_filter = st.sidebar.text_input("Filter by Name", "")

    # Dynamic global filtering
    if name_filter: 
        filtered_df = df[df["Name"].str.contains(name_filter, case=False, na=False)]
    else:
        filtered_df = df.copy()

    # 1. Metrics Row (Dynamic based on filter)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users", len(filtered_df))
    with col2:
        st.metric("Unique Cities", filtered_df["City"].nunique() if not filtered_df.empty else 0)
    with col3:
        st.metric("Unique Companies", filtered_df["Company"].nunique() if not filtered_df.empty else 0)

    st.markdown("---")

    # 2. Interactive Dataframe Display (FIXED: Added st.dataframe)
    st.subheader("User Directory")
    st.dataframe(filtered_df, use_container_width=True)

    st.markdown("---")

    # 3. Bar Chart (Dynamic based on filter)
    st.subheader("Users per City")
    if not filtered_df.empty: 
        city_counts = filtered_df["City"].value_counts().reset_index()
        city_counts.columns = ["City", "User Count"]

        st.bar_chart(
            data=city_counts, 
            x="City",
            y="User Count",
            use_container_width=True
        )
    else:
        st.info("No matching records found for the applied filter.")