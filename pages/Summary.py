import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from utils.data_loader import load_summary_data

st.title('Summary')
st.subheader('Subheader')

# expander: about and data source ref
with st.expander('Click to expand for more details'):
    st.write('Add information about data sources.')
    st.write('You can also add charts, data tables, or any other Streamlit widgets!')

# metrics

# load sales data
summary_df = load_summary_data()

# interactive barplot 
if 'year' in summary_df.columns and 'units_sold' in summary_df.columns and 'powertrain' in summary_df.columns:
    sales_by_year_powertrain = summary_df.groupby(['year', 'powertrain'])['units_sold'].sum().reset_index() # aggregate sales data by year and powertrain

    color_scale = ['#BB9F06', '#86A873', '#095256'] # custom color palette

    fig = px.bar(sales_by_year_powertrain, 
                 x='year', 
                 y='units_sold', 
                 color='powertrain', 
                 title='Units Sold by Year and Powertrain',
                 labels={'units_sold': 'Units Sold', 'year': 'Year'},
                 hover_data={'year': True, 'units_sold': True, 'powertrain': True},
                 color_discrete_sequence=color_scale)
    
    # hover text
    fig.update_traces(
        customdata=sales_by_year_powertrain['powertrain'],
        hovertemplate=
        '<b>Powertrain:</b> %{customdata}<br>'   # Use customdata for powertrain name
        + '<b>Year:</b> %{x}<br>'
        + '<b>Units Sold:</b> %{y}<br>'
        + '<extra></extra>'
    )

    fig.update_layout(
        font=dict(color='white'),
        title_font=dict(size=24, family='Manrope', color='white'),
        xaxis_title_font=dict(size=18, color='white'),
        yaxis_title_font=dict(size=18, color='white'),
    )

    st.plotly_chart(fig)
else:
    st.error("The required columns ('year', 'units_sold', 'powertrain') are not found in the data.")