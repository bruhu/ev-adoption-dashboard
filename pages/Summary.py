import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from utils.data_loader import load_summary_data

st.title('Summary')
st.subheader('Subheader')
# expander: about and data source ref

# metrics

# Load sales data
summary_df = load_summary_data()

# interactive barplot 
if 'year' in summary_df.columns and 'units_sold' in summary_df.columns and 'powertrain' in summary_df.columns:
    # Aggregate the sales data by year and powertrain category
    sales_by_year_powertrain = summary_df.groupby(['year', 'powertrain'])['units_sold'].sum().reset_index()

    # Create the Plotly bar chart (interactive)
    fig = px.bar(sales_by_year_powertrain, 
                 x='year', 
                 y='units_sold', 
                 color='powertrain', 
                 title="Units Sold by Year and Powertrain",
                 labels={'units_sold': 'Units Sold', 'year': 'Year'},
                 hover_data={'year': True, 'units_sold': True, 'powertrain': True})

    # Show the plot in Streamlit
    st.plotly_chart(fig)
else:
    st.error("The required columns ('year', 'units_sold', 'powertrain') are not found in the data.")
