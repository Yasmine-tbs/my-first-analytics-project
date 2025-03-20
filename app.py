import streamlit as st
import pandas as pd

st.title("Import a CSV File and Visualize with Streamlit Charts ")

df = pd.read_csv("Datasets/trips_data_1000.csv")
st.write(" Preview Uploaded data")
st.dataframe(df.head())

# Chart 1: Bar chart of customers by country
st.subheader("Customers by City")
country_counts = df['customer_city'].value_counts()
st.write(country_counts)
st.bar_chart(country_counts)

# Chart 2: Line chart of Tripvcs over time
st.subheader("Subscriptions Over Time")
df['Trips Date'] = pd.to_datetime(df['pickup_time']).dt.date
subscriptions_by_date = df.groupby('Trips Date').size().reset_index(name='Count')
st.write(subscriptions_by_date)
st.line_chart(subscriptions_by_date, x="Trips Date", y="Count")
