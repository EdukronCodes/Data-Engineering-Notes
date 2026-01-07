"""
Product Analysis - Product performance and trends
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

def render():
    st.title("📦 Product Analysis")
    
    df = load_data()
    if df is None:
        st.error("Dataset not loaded. Please run download_dataset.py first.")
        return
    
    # Top products
    st.markdown("### 🏆 Top Performing Products")
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_n = st.slider("Number of Top Products", 5, 50, 20)
    
    with col2:
        metric = st.selectbox("Rank by", ['Sales', 'Profit', 'Quantity'])
    
    product_stats = df.groupby('Product Name').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    product_stats.columns = ['Product Name', 'Sales', 'Profit', 'Quantity', 'Orders']
    product_stats['Profit Margin'] = (product_stats['Profit'] / product_stats['Sales'] * 100).round(2)
    
    top_products = product_stats.nlargest(top_n, metric)
    
    st.dataframe(top_products.style.background_gradient(subset=[metric]), 
                 use_container_width=True)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### Top {top_n} Products by {metric}")
        fig = px.bar(top_products, x=metric, y='Product Name', orientation='h',
                     color=metric, color_continuous_scale='Blues')
        fig.update_layout(showlegend=False, height=600, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Profit vs Sales (Top Products)")
        fig = px.scatter(top_products, x='Sales', y='Profit', 
                        size='Quantity', color='Profit Margin',
                        hover_data=['Product Name', 'Orders'],
                        color_continuous_scale='RdYlGn')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    # Sub-category analysis
    st.markdown("---")
    st.markdown("### 📊 Sub-Category Performance")
    
    subcat_stats = df.groupby('Sub-Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    subcat_stats['Profit Margin'] = (subcat_stats['Profit'] / subcat_stats['Sales'] * 100).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.treemap(subcat_stats, path=['Sub-Category'], values='Sales',
                        color='Profit Margin', color_continuous_scale='RdYlGn')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(subcat_stats.sort_values('Sales', ascending=True), 
                    x='Sales', y='Sub-Category', orientation='h',
                    color='Profit Margin', color_continuous_scale='RdYlGn')
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Product trends over time
    st.markdown("---")
    st.markdown("### 📈 Product Trends Over Time")
    
    selected_category = st.selectbox("Select Category", 
                                    ['All'] + sorted(df['Category'].unique().tolist()))
    
    trend_df = df.copy()
    if selected_category != 'All':
        trend_df = trend_df[trend_df['Category'] == selected_category]
    
    trend_df['Year-Month'] = trend_df['Order Date'].dt.to_period('M').astype(str)
    monthly_trends = trend_df.groupby(['Year-Month', 'Sub-Category'])['Sales'].sum().reset_index()
    
    fig = px.line(monthly_trends, x='Year-Month', y='Sales', color='Sub-Category',
                  markers=True)
    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

