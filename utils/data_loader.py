import pandas as pd
import streamlit as st

# Cache the main data loading function
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    sales_url = 'https://api.iea.org/evs?parameters=EV%20sales&category=Historical&mode=Cars&csv=true'
    charging_points_url = 'https://api.iea.org/evs?parameters=EV%20charging%20points&category=Historical&mode=EV&csv=true'
    
    ev_sales_df = pd.read_csv(sales_url)
    ev_charging_points_df = pd.read_csv(charging_points_url)
    
    return ev_sales_df, ev_charging_points_df

# Cache the sales data processing
@st.cache_data
def load_sales_data():
    ev_sales_df, _ = load_data()
    
    sales_df = ev_sales_df[ev_sales_df['parameter'] == 'EV sales']    
    sales_df = sales_df[sales_df['powertrain'] == 'BEV']    
    
    cols_to_keep = ['region', 'year', 'value']
    sales_df = sales_df[cols_to_keep]
    
    return sales_df

# Cache the summary data processing
@st.cache_data
def load_summary_data():
    ev_sales_df, _ = load_data()

    summary_df = (ev_sales_df[ev_sales_df['parameter'] == 'EV sales']
                  .loc[:, ['region', 'year', 'powertrain', 'value']]
                  .rename(columns={'value': 'units_sold'})
                  .assign(units_sold=lambda x: x['units_sold'].astype(int)))
    
    return summary_df