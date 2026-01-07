"""
Segment Analysis - Business segment performance
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

def render():
    st.title("🏢 Segment Analysis")
    
    df = load_data()
    if df is None:
        st.error("Dataset not loaded. Please run download_dataset.py first.")
        return
    
    # Segment overview
    st.markdown("### 📊 Segment Performance Overview")
    
    segment_stats = df.groupby('Segment').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique',
        'Customer ID': 'nunique'
    }).reset_index()
    segment_stats.columns = ['Segment', 'Sales', 'Profit', 'Quantity', 'Orders', 'Customers']
    segment_stats['Profit Margin'] = (segment_stats['Profit'] / segment_stats['Sales'] * 100).round(2)
    segment_stats['Avg Order Value'] = (segment_stats['Sales'] / segment_stats['Orders']).round(2)
    segment_stats['Orders per Customer'] = (segment_stats['Orders'] / segment_stats['Customers']).round(2)
    segment_stats['Avg Customer Value'] = (segment_stats['Sales'] / segment_stats['Customers']).round(2)
    
    st.dataframe(segment_stats.style.background_gradient(subset=['Sales', 'Profit', 'Profit Margin']), 
                 use_container_width=True)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Sales Distribution by Segment")
        fig = px.pie(segment_stats, values='Sales', names='Segment',
                    color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Customer Distribution by Segment")
        fig = px.pie(segment_stats, values='Customers', names='Segment',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Segment comparison
    st.markdown("---")
    st.markdown("### 🔄 Segment Comparison")
    
    comparison_metric = st.selectbox("Compare Segments by", 
                                    ['Sales', 'Profit', 'Profit Margin', 'Orders', 
                                     'Customers', 'Avg Order Value', 'Avg Customer Value'])
    
    fig = px.bar(segment_stats, x='Segment', y=comparison_metric,
                color=comparison_metric, 
                color_continuous_scale='Blues' if comparison_metric != 'Profit Margin' else 'RdYlGn',
                title=f'{comparison_metric} by Segment')
    fig.update_layout(showlegend=False, height=400)
    if comparison_metric == 'Profit Margin':
        fig.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)
    
    # Segment by category
    st.markdown("---")
    st.markdown("### 📦 Segment Performance by Category")
    
    segment_category = df.groupby(['Segment', 'Category']).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(segment_category, x='Segment', y='Sales', color='Category',
                    barmode='group', color_discrete_sequence=px.colors.qualitative.Set2,
                    title='Sales by Segment and Category')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(segment_category, x='Segment', y='Profit', color='Category',
                    barmode='group', color_discrete_sequence=px.colors.qualitative.Set2,
                    title='Profit by Segment and Category')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Segment trends over time
    st.markdown("---")
    st.markdown("### 📅 Segment Trends Over Time")
    
    df['Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
    monthly_segment = df.groupby(['Year-Month', 'Segment']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    monthly_segment.columns = ['Year-Month', 'Segment', 'Sales', 'Profit', 'Orders']
    monthly_segment = monthly_segment.sort_values('Year-Month')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(monthly_segment, x='Year-Month', y='Sales', color='Segment',
                     markers=True, title='Monthly Sales by Segment')
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(monthly_segment, x='Year-Month', y='Orders', color='Segment',
                     markers=True, title='Monthly Orders by Segment')
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Segment by region
    st.markdown("---")
    st.markdown("### 🌍 Segment Performance by Region")
    
    region_segment = df.groupby(['Region', 'Segment']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Customer ID': 'nunique'
    }).reset_index()
    region_segment.columns = ['Region', 'Segment', 'Sales', 'Profit', 'Customers']
    
    fig = px.sunburst(region_segment, path=['Region', 'Segment'], values='Sales',
                     color='Profit', color_continuous_scale='RdYlGn',
                     title='Sales Distribution: Region × Segment')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Top customers by segment
    st.markdown("---")
    st.markdown("### 🏆 Top Customers by Segment")
    
    selected_segment = st.selectbox("Select Segment", sorted(df['Segment'].unique().tolist()))
    top_n = st.slider("Number of Top Customers", 5, 30, 10)
    
    segment_customers = df[df['Segment'] == selected_segment].groupby(['Customer ID', 'Customer Name']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    segment_customers.columns = ['Customer ID', 'Customer Name', 'Sales', 'Profit', 'Orders']
    segment_customers['Avg Order Value'] = (segment_customers['Sales'] / segment_customers['Orders']).round(2)
    top_customers = segment_customers.nlargest(top_n, 'Sales')
    
    st.dataframe(top_customers.style.background_gradient(subset=['Sales', 'Profit']), 
                 use_container_width=True)
    
    # Segment discount behavior
    st.markdown("---")
    st.markdown("### 🎯 Discount Usage by Segment")
    
    segment_discount = df.groupby('Segment').agg({
        'Discount': 'mean',
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    segment_discount['Avg Discount'] = (segment_discount['Discount'] * 100).round(2)
    
    fig = px.bar(segment_discount, x='Segment', y='Avg Discount',
                color='Avg Discount', color_continuous_scale='Oranges',
                title='Average Discount by Segment (%)')
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

