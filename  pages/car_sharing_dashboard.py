import streamlit as st
import pandas as pd

st.set_page_config(page_title="Car Sharing Dashboard", layout="wide")

page_bg = """
<style>
/* Clean and Professional White Background */
[data-testid="stAppViewContainer"] {
    background: #F8F9FA;
    color: black;
}

/* Sidebar Design - Subtle Grey */
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 2px solid #E0E0E0;
    color: black;
}

/* Modern Header */
h1, h2, h3 {
    color: #2C3E50;
    font-weight: 700;
    text-align: center;
    text-transform: uppercase;
}

/* Metric Box Enhancements */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 10px;
    padding: 10px;
    text-align: center;
}

/* Glass Effect on Data Tables */
[data-testid="stDataFrame"], .stTable {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 10px;
}

/* Button Styling */
.stButton>button {
    background-color: #3498DB;
    color: white;
    border-radius: 5px;
    font-weight: bold;
    padding: 10px 15px;
    border: none;
}

/* Improve Dropdown & Multiselect */
[data-baseweb="select"] {
    background-color: white;
    border-radius: 8px;
    border: 1px solid #E0E0E0;
}

/* Subtle Card Shadows */
[data-testid="stMetric"], [data-testid="stDataFrame"], .stTable {
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.05);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)


st.title("🚗 Car Sharing Analytics Dashboard")

st.markdown("Welcome to the Car Sharing Dashboard! Explore trends, revenue, and key business insights from car rentals across various cities.")

st.markdown("---")

@st.cache_data
def load_data():
    trips = pd.read_csv("Datasets/trips.csv")  
    cars = pd.read_csv("Datasets/cars.csv")
    cities = pd.read_csv("Datasets/cities.csv")
    return trips, cars, cities

trips, cars, cities = load_data()

trips_merged = trips.merge(cars, left_on="car_id", right_on="id", how="left")

trips_merged = trips_merged.merge(cities, left_on="city_id", right_on="city_id", how="left")

columns_to_drop = ["id", "id_customer", "city_id", "id_car"]
existing_columns = [col for col in columns_to_drop if col in trips_merged.columns]
trips_merged = trips_merged.drop(columns=existing_columns)

trips_merged["pickup_time"] = pd.to_datetime(trips_merged["pickup_time"])
trips_merged["dropoff_time"] = pd.to_datetime(trips_merged["dropoff_time"])

trips_merged["pickup_date"] = trips_merged["pickup_time"].dt.date

cars_brand = st.sidebar.multiselect(
    "Select the Car Brand", 
    trips_merged["brand"].dropna().unique()
)

if cars_brand:
    trips_merged = trips_merged[trips_merged["brand"].isin(cars_brand)]

total_trips = len(trips_merged)
total_distance = trips_merged["distance"].sum()
top_car = trips_merged.groupby("model")["revenue"].sum().idxmax()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Trips", value=total_trips)

with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car)

with col3:
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}")

st.write("### Preview of Final Trips Data", trips_merged.head())
trips_over_time = trips_merged.groupby("pickup_date").size()

st.subheader("Trips Over Time")
st.line_chart(trips_over_time)
revenue_by_model = trips_merged.groupby("model")["revenue"].sum().sort_values(ascending=False)

st.subheader("Revenue by Car Model")
st.bar_chart(revenue_by_model)
daily_revenue = trips_merged.groupby("pickup_date")["revenue"].sum()
cumulative_revenue = daily_revenue.cumsum()

st.subheader("Cumulative Revenue Over Time")
st.area_chart(cumulative_revenue)
revenue_by_city = trips_merged.groupby("city_name")["revenue"].sum().sort_values(ascending=False)
st.subheader(" Revenue by City")
st.bar_chart(revenue_by_city)

trips_per_model = trips_merged["model"].value_counts()

st.subheader("Number of Trips Per Car Model")
st.bar_chart(trips_per_model)
trips_merged["trip_duration"] = (trips_merged["dropoff_time"] - trips_merged["pickup_time"]).dt.total_seconds() / 60

avg_duration_by_city = trips_merged.groupby("city_name")["trip_duration"].mean().sort_values(ascending=False)

st.subheader(" Average Trip Duration by City")
st.bar_chart(avg_duration_by_city)
import matplotlib.pyplot as plt

st.subheader(" Revenue Share by City")

fig, ax = plt.subplots()
revenue_by_city.plot(kind="pie", autopct="%1.1f%%", ax=ax)
ax.set_ylabel("")  # Hide y-axis label

st.pyplot(fig)
