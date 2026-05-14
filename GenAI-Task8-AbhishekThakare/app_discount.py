# This program demonstrates a price discount calculator using Streamlit

import streamlit as st

st.title("Price Calculator App")

price = st.number_input("Enter Product Price", min_value=0)

discount = st.slider("Select Discount Percentage", 0, 50)

discount_amount = (price * discount) / 100
final_price = price - discount_amount

if st.button("Calculate Price"):
    st.success("Discount Calculated Successfully")

    st.write("Original Price:", price)
    st.write("Discount:", discount, "%")
    st.write("Final Price:", final_price)

    table_data = {
        "Type": ["Before Discount", "After Discount"],
        "Price": [price, final_price]
    }

    st.table(table_data)
