"""
Overview Dashboard - High-level metrics and KPIs
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

def render():
    st.title("📈 Overview Dashboard")
    
    df = load_data()
    if df is None:
        st.error("Dataset not loaded. Please run download_dataset.py first.")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        regions = ['All'] + sorted(df['Region'].unique().tolist())
        selected_region = st.selectbox("Select Region", regions)
    
    with col2:
        categories = ['All'] + sorted(df['Category'].unique().tolist())
        selected_category = st.selectbox("Select Category", categories)
    
    with col3:
        years = ['All'] + sorted(df['Order Date'].dt.year.unique().tolist())
        selected_year = st.selectbox("Select Year", years)
    
    # Filter data
    filtered_df = df.copy()
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    if selected_year != 'All':
        filtered_df = filtered_df[filtered_df['Order Date'].dt.year == selected_year]
    
    # Key Metrics
    st.markdown("### 📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_orders = len(filtered_df)
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    with col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with col2:
        st.metric("Total Profit", f"${total_profit:,.2f}")
    with col3:
        st.metric("Total Orders", f"{total_orders:,}")
    with col4:
        st.metric("Profit Margin", f"{profit_margin:.2f}%")
    with col5:
        st.metric("Avg Order Value", f"${avg_order_value:,.2f}")
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Sales by Region")
        region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
        fig = px.bar(region_sales, x='Region', y='Sales', 
                     color='Sales', color_continuous_scale='Blues')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Sales by Category")
        category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
        fig = px.pie(category_sales, values='Sales', names='Category',
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Monthly Sales Trend")
        filtered_df['Year-Month'] = filtered_df['Order Date'].dt.to_period('M').astype(str)
        monthly_sales = filtered_df.groupby('Year-Month')['Sales'].sum().reset_index()
        fig = px.line(monthly_sales, x='Year-Month', y='Sales', 
                     markers=True, color_discrete_sequence=['#667eea'])
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Profit vs Sales")
        fig = px.scatter(filtered_df.sample(min(1000, len(filtered_df))), 
                        x='Sales', y='Profit', color='Category',
                        size='Quantity', hover_data=['Product Name'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

