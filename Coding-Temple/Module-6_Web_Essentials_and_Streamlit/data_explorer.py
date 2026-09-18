# Fetch users from https://jsonplaceholder.typicode.com/users using requests.get()
import streamlit as st
import pandas as pd
import requests


# st.set_page_config() with layout="wide" and a relevant title/icon
st.set_page_config(
    page_title="My Dashboard",      # Browser tab title
    page_icon="📊",                 # Browser tab icon
    layout="wide",                  # Use full browser width (default is "centered")
    initial_sidebar_state="expanded" # Sidebar starts open
)
API = "https://jsonplaceholder.typicode.com"

# Cache the fetch with @st.cache_data so it doesn’t re-fetch on every re-run
@st.cache_data(ttl=300)
def fetch_users():
    response = requests.get(f"{API}/users")
    return response.json()

users = fetch_users()

df = pd.DataFrame(users)
cities = df['address'].apply(lambda x: x['city'])
companies = df['company'].apply(lambda x: x['name'])
# 3 metrics in a st.columns() row: total users, unique cities, unique companies
col1, col2, col3 = st.columns(3)
with col1: 
    st.metric("Total Users", f"{len(users)}")
with col2: 
    st.metric("Unique Cities", cities.nunique())
with col3: 
    st.metric("Unique Companies", companies.nunique())

# Interactive dataframe (st.dataframe()) displaying users - with a sidebar name filter (text input that filters the displayed users)
name_filter = st.sidebar.text_input("Filter by name")
filtered_df = df[df['name'].str.contains(name_filter, case=False)]
st.dataframe(filtered_df)

# Bar chart showing the number of users per city
st.bar_chart(cities.value_counts())