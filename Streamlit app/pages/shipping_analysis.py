"""
Shipping Analysis - Shipping mode performance
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

def render():
    st.title("🚚 Shipping Analysis")
    
    df = load_data()
    if df is None:
        st.error("Dataset not loaded. Please run download_dataset.py first.")
        return
    
    # Shipping metrics
    st.markdown("### 📊 Shipping Mode Overview")
    
    shipping_stats = df.groupby('Ship Mode').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique',
        'Quantity': 'sum'
    }).reset_index()
    shipping_stats.columns = ['Ship Mode', 'Total Sales', 'Total Profit', 'Orders', 'Quantity']
    shipping_stats['Avg Order Value'] = (shipping_stats['Total Sales'] / shipping_stats['Orders']).round(2)
    shipping_stats['Profit Margin'] = (shipping_stats['Total Profit'] / shipping_stats['Total Sales'] * 100).round(2)
    
    # Calculate shipping days
    df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    shipping_days = df.groupby('Ship Mode')['Shipping Days'].mean().reset_index()
    shipping_stats = shipping_stats.merge(shipping_days, on='Ship Mode')
    shipping_stats['Avg Shipping Days'] = shipping_stats['Shipping Days'].round(1)
    
    st.dataframe(shipping_stats[['Ship Mode', 'Orders', 'Total Sales', 'Total Profit', 
                                 'Profit Margin', 'Avg Order Value', 'Avg Shipping Days']]
                 .style.background_gradient(subset=['Total Sales', 'Total Profit']), 
                 use_container_width=True)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Orders by Shipping Mode")
        fig = px.pie(shipping_stats, values='Orders', names='Ship Mode',
                    color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Sales by Shipping Mode")
        fig = px.bar(shipping_stats, x='Ship Mode', y='Total Sales',
                    color='Total Sales', color_continuous_scale='Blues')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Shipping performance
    st.markdown("---")
    st.markdown("### ⚡ Shipping Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(shipping_stats, x='Ship Mode', y='Avg Shipping Days',
                    color='Avg Shipping Days', color_continuous_scale='RdYlGn_r',
                    title='Average Shipping Days by Mode')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(shipping_stats, x='Ship Mode', y='Profit Margin',
                    color='Profit Margin', color_continuous_scale='RdYlGn',
                    title='Profit Margin by Shipping Mode (%)')
        fig.update_layout(showlegend=False, height=400)
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    
    # Shipping by region
    st.markdown("---")
    st.markdown("### 🌍 Shipping Mode Usage by Region")
    
    region_ship = df.groupby(['Region', 'Ship Mode']).agg({
        'Order ID': 'nunique',
        'Sales': 'sum'
    }).reset_index()
    region_ship.columns = ['Region', 'Ship Mode', 'Orders', 'Sales']
    
    fig = px.bar(region_ship, x='Region', y='Orders', color='Ship Mode',
                barmode='group', color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Shipping by category
    st.markdown("---")
    st.markdown("### 📦 Shipping Mode by Product Category")
    
    category_ship = df.groupby(['Category', 'Ship Mode']).agg({
        'Order ID': 'nunique',
        'Profit': 'sum'
    }).reset_index()
    category_ship.columns = ['Category', 'Ship Mode', 'Orders', 'Profit']
    
    fig = px.sunburst(category_ship, path=['Category', 'Ship Mode'], 
                     values='Orders', color='Profit',
                     color_continuous_scale='RdYlGn',
                     title='Order Distribution: Category × Shipping Mode')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Shipping trends
    st.markdown("---")
    st.markdown("### 📅 Shipping Trends Over Time")
    
    df['Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
    monthly_ship = df.groupby(['Year-Month', 'Ship Mode']).agg({
        'Order ID': 'nunique',
        'Shipping Days': 'mean'
    }).reset_index()
    monthly_ship.columns = ['Year-Month', 'Ship Mode', 'Orders', 'Avg Shipping Days']
    monthly_ship = monthly_ship.sort_values('Year-Month')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(monthly_ship, x='Year-Month', y='Orders', color='Ship Mode',
                     markers=True, title='Monthly Orders by Shipping Mode')
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(monthly_ship, x='Year-Month', y='Avg Shipping Days', color='Ship Mode',
                     markers=True, title='Average Shipping Days Over Time')
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Shipping efficiency
    st.markdown("---")
    st.markdown("### 🎯 Shipping Efficiency Analysis")
    
    # Calculate shipping efficiency (profit per shipping day)
    shipping_stats['Efficiency'] = (shipping_stats['Total Profit'] / shipping_stats['Avg Shipping Days']).round(2)
    shipping_stats = shipping_stats.sort_values('Efficiency', ascending=False)
    
    fig = px.bar(shipping_stats, x='Ship Mode', y='Efficiency',
                color='Efficiency', color_continuous_scale='Greens',
                title='Profit Efficiency (Profit per Shipping Day)')
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

