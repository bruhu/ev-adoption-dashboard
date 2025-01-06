import streamlit as st
from utils.data_loader import load_sales_data  # Importing from utils.py

# Load the external CSS file
css_file_path = './assets/styles.css'
with open(css_file_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# load sales data
sales_df = load_sales_data()

# Streamlit stuff
st.title('EV Sales Data')
st.write(sales_df)

