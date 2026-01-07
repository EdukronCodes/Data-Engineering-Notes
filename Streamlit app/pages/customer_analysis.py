"""
Customer Analysis - Customer segmentation and behavior
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

def render():
    st.title("👥 Customer Analysis")
    
    df = load_data()
    if df is None:
        st.error("Dataset not loaded. Please run download_dataset.py first.")
        return
    
    # Customer segments
    st.markdown("### 🎯 Customer Segment Performance")
    
    segment_stats = df.groupby('Segment').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Customer ID': 'nunique',
        'Order ID': 'nunique'
    }).reset_index()
    segment_stats.columns = ['Segment', 'Total Sales', 'Total Profit', 'Customers', 'Orders']
    segment_stats['Avg Order Value'] = (segment_stats['Total Sales'] / segment_stats['Orders']).round(2)
    segment_stats['Profit Margin'] = (segment_stats['Total Profit'] / segment_stats['Total Sales'] * 100).round(2)
    
    st.dataframe(segment_stats.style.background_gradient(subset=['Total Sales', 'Total Profit']), 
                 use_container_width=True)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Sales by Segment")
        fig = px.pie(segment_stats, values='Total Sales', names='Segment',
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Profit by Segment")
        fig = px.bar(segment_stats, x='Segment', y='Total Profit',
                     color='Total Profit', color_continuous_scale='Greens')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top customers
    st.markdown("---")
    st.markdown("### 🏆 Top Customers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        top_n = st.slider("Number of Top Customers", 10, 100, 20)
    
    with col2:
        customer_metric = st.selectbox("Rank Customers by", ['Sales', 'Profit', 'Orders'])
    
    customer_stats = df.groupby(['Customer ID', 'Customer Name', 'Segment']).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique',
        'Quantity': 'sum'
    }).reset_index()
    customer_stats.columns = ['Customer ID', 'Customer Name', 'Segment', 'Sales', 'Profit', 'Orders', 'Quantity']
    customer_stats['Avg Order Value'] = (customer_stats['Sales'] / customer_stats['Orders']).round(2)
    
    top_customers = customer_stats.nlargest(top_n, customer_metric)
    
    st.dataframe(top_customers[['Customer Name', 'Segment', 'Sales', 'Profit', 'Orders', 'Avg Order Value']]
                 .style.background_gradient(subset=[customer_metric]), 
                 use_container_width=True)
    
    # Customer distribution
    st.markdown("---")
    st.markdown("### 📊 Customer Value Distribution")
    
    # RFM-like analysis
    customer_stats['Customer Value'] = pd.cut(customer_stats['Sales'], 
                                               bins=[0, 1000, 5000, 10000, float('inf')],
                                               labels=['Low', 'Medium', 'High', 'Very High'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        value_dist = customer_stats['Customer Value'].value_counts().reset_index()
        value_dist.columns = ['Customer Value', 'Count']
        fig = px.bar(value_dist, x='Customer Value', y='Count',
                     color='Count', color_continuous_scale='Blues')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(customer_stats.sample(min(500, len(customer_stats))), 
                        x='Orders', y='Sales', color='Segment',
                        size='Profit', hover_data=['Customer Name'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Customer retention/behavior
    st.markdown("---")
    st.markdown("### 📈 Customer Purchase Patterns")
    
    customer_orders = df.groupby(['Customer ID', df['Order Date'].dt.to_period('M').astype(str)]).agg({
        'Sales': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    customer_orders.columns = ['Customer ID', 'Month', 'Sales', 'Orders']
    
    monthly_customer_activity = customer_orders.groupby('Month').agg({
        'Customer ID': 'nunique',
        'Sales': 'sum'
    }).reset_index()
    monthly_customer_activity.columns = ['Month', 'Active Customers', 'Total Sales']
    
    fig = px.line(monthly_customer_activity, x='Month', y='Active Customers',
                 secondary_y='Total Sales', markers=True)
    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

