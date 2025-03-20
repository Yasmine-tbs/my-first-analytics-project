import streamlit as st

st.title("My Streamlit Web App")
st.header("Data Exploration Section")

# Contents in  a sidebar
with st.sidebar:
    st.header("This is a sidebar header")
    user_input = st.text_input("Enter your name")
    st.write("Your provided name is ", user_input)
    option = st.selectbox("Choose an option", ["Choice A", "Choice B", "Choice C"])

# Contents in the main window
# Display user input
st.write(f"Hello, {user_input}! You selected option {option}.")

# Adding Contents in multiple columns
col1, col2 = st.columns(2)
with col1:
    st.subheader("Column 1")
    st.button("Click me!")
    st.write("This is some text in column 1")

with col2:
    st.subheader("Column 2")
    st.line_chart({"data": [1, 5, 2, 6, 2, 1]})

# Expandable section
with st.expander("See explanation"):
    st.write("This is an expandable section with additional information.")