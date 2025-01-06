import streamlit as st
from utils.data_loader import load_sales_data  # Importing from utils.py

# load sales data
sales_df = load_sales_data()

# Streamlit stuff
st.title('EV Sales Data')
st.write(sales_df)

