# Use at least 5 different widget types from this list:
# st.text_input(), st.number_input(), st.slider(), st.selectbox(), st.multiselect(), st.radio(), st.checkbox(), st.text_area(), st.date_input()
# Content that changes based on widget values (use if/elif or conditional logic)
# At least one calculation that uses widget values (e.g., a cost calculator, a rating average, a progress tracker)
# Use at least two of these display elements: st.write(), st.info(), st.success(), st.warning(), st.metric(), st.code(), st.progress()
# A st.title() and at least one st.header() or st.subheader()

import streamlit as st

# Trip planner: Selectbox for destination, date_input for travel dates, number_input for budget, calculate daily budget

st.title("Trip Planner Demo")
st.header("Trip Budget Helper")
destination = st.selectbox("Where are you going?", ["London", "Beijing", "Seoul", "Kyoto"])
preferred_sights = st.checkbox("Check if you want destination recommendations.")
departing = st.date_input("When are you leaving?")
returning = st.date_input("When are you returning?")
budget = st.number_input("Total Budget")
total_days = returning - departing
if total_days > 0:  
    daily_budget = budget / total_days
    st.metric("Daily Budget", f"${daily_budget:.2f}")
    if daily_budget < 20:
        st.warning("You are hitting low on your budget, spend wisely!")

if preferred_sights:
    if destination == "London":
        st.write("Go visit the Big Ben")
    elif destination == "Beijing": 
        st.write("Go to the great wall.")
    elif destination == "Seoul": 
        st.write("Go get skin care.")
    elif destination == "Kyoto": 
        st.write("Go eat some street food.")



