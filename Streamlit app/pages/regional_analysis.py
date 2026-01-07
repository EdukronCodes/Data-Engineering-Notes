"""
Regional Analysis - Sales performance by region
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

def render():
    st.title("🌍 Regional Analysis")
    
    df = load_data()
    if df is None:
        st.error("Dataset not loaded. Please run download_dataset.py first.")
        return
    
    # Regional metrics
    regional_stats = df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique',
        'Customer ID': 'nunique'
    }).reset_index()
    regional_stats.columns = ['Region', 'Total Sales', 'Total Profit', 'Orders', 'Customers']
    regional_stats['Profit Margin'] = (regional_stats['Total Profit'] / regional_stats['Total Sales'] * 100).round(2)
    regional_stats['Avg Order Value'] = (regional_stats['Total Sales'] / regional_stats['Orders']).round(2)
    
    st.markdown("### 📊 Regional Performance Summary")
    st.dataframe(regional_stats.style.background_gradient(subset=['Total Sales', 'Total Profit']), 
                 use_container_width=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Sales by Region")
        fig = px.bar(regional_stats, x='Region', y='Total Sales',
                     color='Total Sales', color_continuous_scale='Viridis')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Profit by Region")
        fig = px.bar(regional_stats, x='Region', y='Total Profit',
                     color='Total Profit', color_continuous_scale='Plasma')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # State-level analysis
    st.markdown("---")
    st.markdown("### 🗺️ State-Level Analysis")
    
    selected_region = st.selectbox("Select Region for State Analysis", 
                                   ['All'] + sorted(df['Region'].unique().tolist()))
    
    state_df = df.copy()
    if selected_region != 'All':
        state_df = state_df[state_df['Region'] == selected_region]
    
    state_stats = state_df.groupby('State').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index().sort_values('Sales', ascending=False).head(15)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top 15 States by Sales")
        fig = px.bar(state_stats, x='Sales', y='State', orientation='h',
                     color='Sales', color_continuous_scale='Blues')
        fig.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Top 15 States by Profit")
        state_profit = state_stats.sort_values('Profit', ascending=False)
        fig = px.bar(state_profit, x='Profit', y='State', orientation='h',
                     color='Profit', color_continuous_scale='Greens')
        fig.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Category performance by region
    st.markdown("---")
    st.markdown("### 📦 Category Performance by Region")
    
    region_category = df.groupby(['Region', 'Category']).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig = px.sunburst(region_category, path=['Region', 'Category'], values='Sales',
                      color='Profit', color_continuous_scale='RdBu')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

