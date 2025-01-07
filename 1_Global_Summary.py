import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from utils.data_loader import load_summary_data

# Load the external CSS file
css_file_path = './assets/styles.css'
st.set_page_config(page_title="Global Summary", page_icon="🌍")

with open(css_file_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.title('🌍 Global Summary')
st.subheader('Subheader')
    
# expander: about and data source ref
with st.expander('Click to expand for more details'):
    st.write('Add information about data sources.')
    st.write('You can also add charts, data tables, or any other Streamlit widgets!')

# metrics
# Read the CSV files
sales_df = pd.read_csv('data/raw/IEA-EV-dataEV salesHistoricalCars.csv')
charging_df = pd.read_csv('data/raw/IEA-EV-dataEV charging pointsHistoricalEV.csv')

# load sales data
summary_df = load_summary_data()

# Process sales data
sales_df = sales_df[sales_df['parameter'] == 'EV sales']
sales_by_year = sales_df.groupby('year')['value'].sum().reset_index()

# Process charging points data
charging_df = charging_df.groupby('year')['value'].sum().reset_index()

# Metric 1: World EV Sales - Current Year and Delta from Previous Year
current_year_sales = sales_by_year[sales_by_year['year'] == 2023]['value'].sum()
previous_year_sales = sales_by_year[sales_by_year['year'] == 2022]['value'].sum()
delta_sales = current_year_sales - previous_year_sales

# Metric 2: World EV Sales Growth - Current Year and Delta from Previous Year
if previous_year_sales != 0:
    growth_sales = ((current_year_sales - previous_year_sales) / previous_year_sales) * 100
else:
    growth_sales = 0

# Metric 3: World Charging Points - Current Year and Delta from Previous Year
current_year_charging = charging_df[charging_df['year'] == 2023]['value'].sum()
previous_year_charging = charging_df[charging_df['year'] == 2022]['value'].sum()
delta_charging = current_year_charging - previous_year_charging

# Create three columns for displaying the metrics side by side
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="World EV Sales", value=f"{int(current_year_sales):,}", delta=f"{int(delta_sales):,}")

with col2:
    st.metric(label="World EV Sales Growth", value=f"{growth_sales:.2f}%", delta=f"{growth_sales - ((previous_year_sales - current_year_sales) / previous_year_sales) * 100:.2f}%")

with col3:
    st.metric(label="World Charging Points", value=f"{int(current_year_charging):,}", delta=f"{int(delta_charging):,}")

# After loading the external CSS file and before the metrics
st.markdown("""
    <style>
    /* For positive values */
    [data-testid="stMetricDelta"] svg {
        color: #86A873 !important;
    }
    
    [data-testid="stMetricDelta"] div {
        color: #86A873 !important;
    }

    /* Ensure the value itself uses the yellow color when positive */
    .css-1wivap2 {
        color: #86A873 !important;
    }
    
    /* Additional class for positive metrics */
    .css-1yk9tp8 {
        color: #86A873 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.subheader('Sales Summary')

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
    