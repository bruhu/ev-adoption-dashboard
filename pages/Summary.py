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
data = {
    'year': [2023, 2022, 2021, 2020],
    'region': ['Global', 'Global', 'Global', 'Global'],
    'units_sold': [5000000, 4500000, 4000000, 3500000],
    'charging_points': [100000, 90000, 80000, 75000]
}

df = pd.DataFrame(data)

# load sales data
summary_df = load_summary_data()

# Metric 1: World EV Sales - Current Year and Delta from Previous Year
current_year_sales = df[df['year'] == 2023]['units_sold'].sum()
previous_year_sales = df[df['year'] == 2022]['units_sold'].sum()
delta_sales = current_year_sales - previous_year_sales

# Metric 2: World EV Sales Growth - Current Year and Delta from Previous Year
if previous_year_sales != 0:
    growth_sales = ((current_year_sales - previous_year_sales) / previous_year_sales) * 100  # Sales growth percentage
else:
    growth_sales = 0  # Handle case if previous year sales are zero

# Metric 3: World Charging Points - Current Year and Delta from Previous Year
current_year_charging_points = df[df['year'] == 2023]['charging_points'].sum()
previous_year_charging_points = df[df['year'] == 2022]['charging_points'].sum()
delta_charging_points = current_year_charging_points - previous_year_charging_points

# Create three columns for displaying the metrics side by side
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="World EV Sales (Sample Data)", value=f"{current_year_sales:,}", delta=f"{delta_sales:,}")

with col2:
    st.metric(label="World EV Sales Growth (Sample Data)", value=f"{growth_sales:.2f}%", delta=f"{growth_sales - ((previous_year_sales - current_year_sales) / previous_year_sales) * 100:.2f}%")

with col3:
    st.metric(label="World Charging Points (Sample Data)", value=f"{current_year_charging_points:,}", delta=f"{delta_charging_points:,}")



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
    st.error('The required columns (year, units_sold, powertrain) are not found in the data.')
    