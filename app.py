import streamlit as st
import pandas as pd 
import numpy as np

st.title("Manipulate Streamlit Chart")
#Generate Randomn Data
bar_data = pd.DataFrame(np.random.randn(20, 3),columns=["a", "b", "c"])
st.bar_chart(bar_data)
#Generate random data for line chart
line_data = pd.DataFrame(np.random.randn(20, 3),columns=["a", "b", "c"])
st.line_chart(line_data)

#Generate random data for scatter chart 
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.scatter_chart(chart_data)