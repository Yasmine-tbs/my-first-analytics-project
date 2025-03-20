import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Visualize CSV Data with Streamlit ")

df = pd.read_csv("Datasets/trips_data_1000.csv")
print(df.describe())

cars_brand = st.sidebar.multiselect("Select the car brand", df["car_brand"].unique(),  df["car_brand"].unique())
df = df[df["car_brand"].isin(cars_brand)]

col1, col2, col3, col4  = st.columns(4)

col1.metric("Car Models in Use", df.shape[0])
col2.metric("Unique Customers",  df["customer_email"].nunique())
with col3:
    total_distance = df['distance'].sum() / 1000
    st.metric("Total Distance", value=f"{total_distance:.2f} K")
with col4:
    average_revenue = df['revenue'].mean()
    st.metric("Average Revenue Per Trip", value=f"{average_revenue:.2f} €")

col1, col2, col3 = st.columns(3)
# Chart 1: Bar chart of customers by country
with col1:
    st.subheader("Customers by City")
    country_counts = df['customer_city'].value_counts()
    st.bar_chart(country_counts)

# Chart 2 : Revenue by Car Model
with col2:
    st.subheader("Revenue by Car Model")
    revenue_by_car = df.groupby('car_model')['revenue'].sum()
    st.bar_chart(revenue_by_car)
# Chart 3 : Average Trip distance per city
with col3:
    st.subheader("Average Trip Distance per city")
    avg_distance_by_city = df.groupby('customer_city')['distance'].mean()
    st.bar_chart(avg_distance_by_city)
# Convert the pickup time to a date type column 
df['Trips Date'] = pd.to_datetime(df['pickup_time']).dt.date

# Chart 3: Revenue over time 
st.subheader("Revenue Over Time")
revenue_over_time = df.groupby('Trips Date')['revenue'].sum()
st.area_chart(revenue_over_time)

# Chart 4: Line chart of Trips over time
st.subheader("Trips Over Time")
Trips_Count = df["Trips Date"].value_counts()
st.line_chart(Trips_Count)

st.write(" Preview Uploaded data")
st.dataframe(df.head())