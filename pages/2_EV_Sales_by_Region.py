import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title='EV Sales by Region',
    page_icon='🗺️'
)

st.title('🗺️ EV Sales by Region')
# st.text('EV Sales by Region')

# selectbox filter - region filter
regions = ['All Regions', 'North America', 'Europe', 'Asia Pacific', 'South America', 'Middle East & Africa']
selected_region = st.selectbox(
    'Select Region',
    options=regions,
    key='region_filter'
)

# Load and prepare data
@st.cache_data
def load_sales_data():
    # Replace this with your actual data loading logic
    df = pd.DataFrame({
        'Region': ['North America', 'North America', 'Europe', 'Europe', 'Asia Pacific', 'Asia Pacific'],
        'Country': ['USA', 'Canada', 'Germany', 'France', 'China', 'Japan'],
        'Sales': [500000, 200000, 800000, 400000, 1200000, 300000]
    })
    return df

df = load_sales_data()

# Filter data based on selected region
if selected_region != 'All Regions':
    filtered_df = df[df['Region'] == selected_region]
else:
    filtered_df = df

# Define color palette
color_scale = ['#095256', '#BB9F06', '#86A873']

# Create bar plot
fig = px.bar(
    filtered_df,
    x='Country',
    y='Sales',
    title=f'EV Sales by Country - {selected_region}',
    color='Country',
    height=500,
    color_discrete_sequence=color_scale
)

# Update layout
fig.update_layout(
    xaxis_title="Country",
    yaxis_title="Sales Volume",
    showlegend=False,
    font=dict(color='white'),
    title_font=dict(size=24, family='Manrope', color='white'),
    xaxis_title_font=dict(size=18, color='white'),
    yaxis_title_font=dict(size=18, color='white'),
)

# Display the plot
st.plotly_chart(fig, use_container_width=True)