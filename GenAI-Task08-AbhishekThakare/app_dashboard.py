# This program demonstrates a mini sales dashboard using Streamlit

import streamlit as st

st.title("Simple Sales Dashboard")

st.write("A simple dashboard showing monthly sales")

months = ["January", "February", "March", "April"]

sales_data = {
    "January": 1200,
    "February": 1500,
    "March": 900,
    "April": 2000
}

selected_month = st.selectbox("Select Month", months)

st.write(
    "Sales in",
    selected_month + ":",
    sales_data[selected_month]
)

st.bar_chart(list(sales_data.values()))
