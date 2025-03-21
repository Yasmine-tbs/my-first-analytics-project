import streamlit as st
import pandas as pd

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
