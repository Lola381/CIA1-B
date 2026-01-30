import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

# Load datasets
hist_df = pd.read_csv('historical_silver_price.csv')
hist_df['Date'] = pd.to_datetime(hist_df['Year'].astype(str) + '-' + hist_df['Month'], format='%Y-%b')
hist_df = hist_df.sort_values('Date')

sales_df = pd.read_csv('state_wise_silver_purchased_kg.csv')

st.title("Silver Price Calculator & Silver Sales Analysis")

# Tabs for different sections
tab1, tab2 = st.tabs(["Silver Price Calculator", "Silver Sales Dashboard"])

with tab1:
    st.header("Silver Price Calculator")
    
    # Inputs
    unit = st.selectbox("Unit for weight", ["grams", "kilograms"])
    weight = st.number_input(f"Weight of silver ({unit})", min_value=0.0, value=1.0)













    price_per_gram = st.number_input("Current price per gram (INR)", min_value=0.0, value=50.0)
    
    if unit == "kilograms":
        weight_in_grams = weight * 1000
    else:
        weight_in_grams = weight
    
    # Calculate total cost
    total_cost = weight_in_grams * price_per_gram
    st.write(f"Total cost: {total_cost:.2f} INR")
    
    # Currency conversion
    usd_rate = 0.012  # Approximate INR to USD rate
    total_usd = total_cost * usd_rate
    st.write(f"Total cost in USD: {total_usd:.2f} USD")
    
    # Historical price chart
    st.subheader("Historical Silver Price Chart")
    
    # Filter options
    filter_option = st.selectbox("Filter by price range", ["All", "≤ 20,000 INR per kg", "20,000 - 30,000 INR per kg", "≥ 30,000 INR per kg"])
    
    if filter_option == "≤ 20,000 INR per kg":
        filtered_df = hist_df[hist_df['Silver_Price_INR_per_kg'] <= 20000]
    elif filter_option == "20,000 - 30,000 INR per kg":
        filtered_df = hist_df[(hist_df['Silver_Price_INR_per_kg'] > 20000) & (hist_df['Silver_Price_INR_per_kg'] <= 30000)]
    elif filter_option == "≥ 30,000 INR per kg":
        filtered_df = hist_df[hist_df['Silver_Price_INR_per_kg'] >= 30000]
    else:
        filtered_df = hist_df
    
    fig, ax = plt.figure(figsize=(10, 5)), plt.gca()
    ax.plot(filtered_df['Date'], filtered_df['Silver_Price_INR_per_kg'])
    ax.set_title('Historical Silver Prices')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price per kg (INR)')
    st.pyplot(fig)

with tab2:
    st.header("Silver Sales Dashboard")
    
    # Top 5 states bar chart
    st.subheader("Top 5 States with Highest Silver Purchases")
    top5 = sales_df.nlargest(5, 'Silver_Purchased_kg')
    fig, ax = plt.figure(figsize=(10, 5)), plt.gca()
    ax.bar(top5['State'], top5['Silver_Purchased_kg'])
    ax.set_title('Top 5 States')
    ax.set_xlabel('State')
    ax.set_ylabel('Purchases (kg)')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # January month silver sales
    st.subheader("January Month Silver Sales")
    # Filter historical data for January
    jan_data = hist_df[hist_df['Date'].dt.month == 1]
    fig, ax = plt.figure(figsize=(10, 5)), plt.gca()
    ax.plot(jan_data['Date'].dt.year, jan_data['Silver_Price_INR_per_kg'])
    ax.set_title('January Silver Prices Over Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Price per kg (INR)')
    st.pyplot(fig)
    
    # India map using GeoPandas
    st.subheader("India State-wise Silver Purchases Map")

        # Load India states shapefile
    india_gdf = gpd.read_file('India-State-and-Country-Shapefile-Updated-Jan-2020-master/India_State_Boundary.shp')
        # Merge with sales data (assuming state name column is 'State_Name')
    india_gdf = india_gdf.merge(sales_df, left_on='State_Name', right_on='State', how='left')
        # Plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    india_gdf.plot(column='Silver_Purchased_kg', ax=ax, legend=True, cmap='Blues', missing_kwds={'color': 'lightgrey'})
    ax.set_title('Silver Purchases by State (kg)')
    ax.axis('off')
    st.pyplot(fig)


