import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    trips = pd.read_csv("Datasets/trips.csv")  
    cars = pd.read_csv("Datasets/cars.csv")
    cities = pd.read_csv("Datasets/cities.csv")
    return trips, cars, cities

trips, cars, cities = load_data()

st.write("### Preview: Trips Data", trips.head())
st.write("### Preview: Cars Data", cars.head())
st.write("### Preview: Cities Data", cities.head())

trips_merged = trips.merge(cars, left_on="car_id", right_on="id", how="left")

trips_merged = trips_merged.merge(cities, left_on="city_id", right_on="city_id", how="left")

columns_to_drop = ["id", "id_customer", "city_id", "id_car"]
existing_columns = [col for col in columns_to_drop if col in trips_merged.columns]
trips_merged = trips_merged.drop(columns=existing_columns)

