import streamlit as st
import pandas as pd

st.title("CSV File Uploader")

uploaded_file = st.file_uploader("upload a csv file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)  # Use the uploaded file variable directly
    st.write("### Preview of Uploaded Data:")
    st.dataframe(df.head())
