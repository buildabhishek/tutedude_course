# This program demonstrates a simple product form using Streamlit

import streamlit as st

st.title("Product Form")

st.sidebar.header("Enter Product Details")

product_name = st.sidebar.text_input("Product Name")

category = st.sidebar.selectbox(
    "Select Category",
    ["Electronics", "Clothing", "Books", "Furniture", "Sports"]
)

price = st.sidebar.number_input("Enter Product Price", min_value=0)

if st.sidebar.button("Add Product"):

    st.success("Product Added Successfully")

    st.write("### Product Details")
    st.write("Product Name:", product_name)
    st.write("Category:", category)
    st.write("Price:", price)
