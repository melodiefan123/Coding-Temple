# Use at least 5 different widget types from this list:
# st.text_input(), st.number_input(), st.slider(), st.selectbox(), st.multiselect(), st.radio(), st.checkbox(), st.text_area(), st.date_input()
# Content that changes based on widget values (use if/elif or conditional logic)
# At least one calculation that uses widget values (e.g., a cost calculator, a rating average, a progress tracker)
# Use at least two of these display elements: st.write(), st.info(), st.success(), st.warning(), st.metric(), st.code(), st.progress()
# A st.title() and at least one st.header() or st.subheader()
import datetime
import streamlit as st

# Trip planner: Selectbox for destination, date_input for travel dates, number_input for budget, calculate daily budget

st.title("Trip Planner Demo")
st.header("Trip Budget Helper")

destination = st.selectbox("Where are you going?", ["London", "Beijing", "Seoul", "Kyoto"])

preferred_sights = st.checkbox("Check if you want destination recommendations.", value=True)
departing = st.date_input("When are you leaving?", value= datetime.date.today())
returning = st.date_input("When are you returning?", value=datetime.date.today() + datetime.timedelta(days=7))
budget = st.number_input("Total Budget", min_value=1, value=1000)
trip_pace = st.slider("Trip Pace (1 = Relaxed, 5 = Fast-paced)", min_value=1, max_value=5, value=3)

total_days = (returning - departing).days

st.subheader("Budget & Trip Summary")

if total_days <= 0:  
    st.warning("⚠️ Return date must be after departure date!")
else:
    daily_budget = budget / total_days
    st.metric("Daily Budget", f"${daily_budget:.2f}")
    if daily_budget < 20:
        st.warning("You are hitting low on your budget, spend wisely!")
    else: 
        st.success("Your daily budget looks good!")

if preferred_sights:
    st.subheader("Destination Recommendations")
    if destination == "London":
        st.write("Go visit the Big Ben")
    elif destination == "Beijing": 
        st.write("Go to the great wall.")
    elif destination == "Seoul": 
        st.write("Go get skin care.")
    elif destination == "Kyoto": 
        st.write("Go eat some street food.")



