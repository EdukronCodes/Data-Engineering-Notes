"""
Performance Metrics - Key performance indicators
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

def render():
    st.title("⚡ Performance Metrics")
    
    df = load_data()
    if df is None:
        st.error("Dataset not loaded. Please run download_dataset.py first.")
        return
    
    # Calculate key metrics
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = len(df)
    total_customers = df['Customer ID'].nunique()
    total_products = df['Product ID'].nunique()
    
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    orders_per_customer = total_orders / total_customers if total_customers > 0 else 0
    customer_lifetime_value = total_sales / total_customers if total_customers > 0 else 0
    
    # Overall KPIs
    st.markdown("### 📊 Overall Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with col2:
        st.metric("Total Profit", f"${total_profit:,.2f}")
    with col3:
        st.metric("Profit Margin", f"{profit_margin:.2f}%")
    with col4:
        st.metric("Avg Order Value", f"${avg_order_value:,.2f}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", f"{total_orders:,}")
    with col2:
        st.metric("Total Customers", f"{total_customers:,}")
    with col3:
        st.metric("Orders per Customer", f"{orders_per_customer:.2f}")
    with col4:
        st.metric("Customer Lifetime Value", f"${customer_lifetime_value:,.2f}")
    
    st.markdown("---")
    
    # Performance scorecard
    st.markdown("### 🎯 Performance Scorecard")
    
    # Calculate performance scores (normalized 0-100)
    region_sales = df.groupby('Region')['Sales'].sum()
    category_sales = df.groupby('Category')['Sales'].sum()
    segment_sales = df.groupby('Segment')['Sales'].sum()
    
    # Diversity scores (how balanced is the distribution)
    def calculate_diversity(series):
        """Calculate diversity score using entropy"""
        proportions = series / series.sum()
        entropy = -(proportions * proportions.apply(lambda x: 0 if x == 0 else np.log2(x))).sum()
        max_entropy = np.log2(len(series))
        return (entropy / max_entropy * 100) if max_entropy > 0 else 0
    
    region_diversity = calculate_diversity(region_sales)
    category_diversity = calculate_diversity(category_sales)
    segment_diversity = calculate_diversity(segment_sales)
    
    # Growth metrics
    df['Year'] = df['Order Date'].dt.year
    yearly_sales = df.groupby('Year')['Sales'].sum()
    if len(yearly_sales) > 1:
        sales_growth = ((yearly_sales.iloc[-1] / yearly_sales.iloc[-2]) - 1) * 100
    else:
        sales_growth = 0
    
    yearly_profit = df.groupby('Year')['Profit'].sum()
    if len(yearly_profit) > 1:
        profit_growth = ((yearly_profit.iloc[-1] / yearly_profit.iloc[-2]) - 1) * 100
    else:
        profit_growth = 0
    
    # Create scorecard
    scorecard_data = {
        'Metric': ['Sales Growth', 'Profit Growth', 'Profit Margin', 
                  'Region Diversity', 'Category Diversity', 'Segment Diversity',
                  'Customer Retention', 'Order Frequency'],
        'Value': [f"{sales_growth:.1f}%", f"{profit_growth:.1f}%", f"{profit_margin:.2f}%",
                 f"{region_diversity:.1f}", f"{category_diversity:.1f}", f"{segment_diversity:.1f}",
                 f"{orders_per_customer:.2f}", f"{total_orders / (df['Order Date'].max() - df['Order Date'].min()).days * 30:.1f}"]
    }
    
    scorecard_df = pd.DataFrame(scorecard_data)
    st.dataframe(scorecard_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Performance trends
    st.markdown("### 📈 Performance Trends")
    
    df['Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
    monthly_metrics = df.groupby('Year-Month').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique',
        'Customer ID': 'nunique'
    }).reset_index()
    monthly_metrics.columns = ['Year-Month', 'Sales', 'Profit', 'Orders', 'Customers']
    monthly_metrics['Profit Margin'] = (monthly_metrics['Profit'] / monthly_metrics['Sales'] * 100).round(2)
    monthly_metrics['Avg Order Value'] = (monthly_metrics['Sales'] / monthly_metrics['Orders']).round(2)
    monthly_metrics = monthly_metrics.sort_values('Year-Month')
    
    # Calculate rolling averages
    monthly_metrics['Sales MA'] = monthly_metrics['Sales'].rolling(window=3, center=True).mean()
    monthly_metrics['Profit MA'] = monthly_metrics['Profit'].rolling(window=3, center=True).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_metrics['Year-Month'],
        y=monthly_metrics['Sales'],
        mode='lines+markers',
        name='Sales',
        line=dict(color='#667eea', width=2),
        yaxis='y'
    ))
    fig.add_trace(go.Scatter(
        x=monthly_metrics['Year-Month'],
        y=monthly_metrics['Sales MA'],
        mode='lines',
        name='Sales MA (3 months)',
        line=dict(color='#667eea', width=2, dash='dash'),
        yaxis='y'
    ))
    fig.add_trace(go.Scatter(
        x=monthly_metrics['Year-Month'],
        y=monthly_metrics['Profit'],
        mode='lines+markers',
        name='Profit',
        line=dict(color='#4ecdc4', width=2),
        yaxis='y2'
    ))
    fig.add_trace(go.Scatter(
        x=monthly_metrics['Year-Month'],
        y=monthly_metrics['Profit MA'],
        mode='lines',
        name='Profit MA (3 months)',
        line=dict(color='#4ecdc4', width=2, dash='dash'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        height=500,
        xaxis_title="Month",
        yaxis=dict(title="Sales ($)", side='left'),
        yaxis2=dict(title="Profit ($)", overlaying='y', side='right'),
        hovermode='x unified',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Efficiency metrics
    st.markdown("---")
    st.markdown("### ⚡ Efficiency Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Sales per product
        sales_per_product = total_sales / total_products if total_products > 0 else 0
        st.metric("Sales per Product", f"${sales_per_product:,.2f}")
    
    with col2:
        # Profit per order
        profit_per_order = total_profit / total_orders if total_orders > 0 else 0
        st.metric("Profit per Order", f"${profit_per_order:,.2f}")
    
    with col3:
        # Conversion rate (profitable orders)
        profitable_orders = len(df[df['Profit'] > 0])
        conversion_rate = (profitable_orders / total_orders * 100) if total_orders > 0 else 0
        st.metric("Profitable Order Rate", f"{conversion_rate:.1f}%")
    
    # Performance by dimension
    st.markdown("---")
    st.markdown("### 🎯 Performance by Dimension")
    
    dimension = st.selectbox("Analyze Performance by", 
                            ['Region', 'Category', 'Segment', 'Ship Mode'])
    
    dim_metrics = df.groupby(dimension).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'nunique',
        'Customer ID': 'nunique'
    }).reset_index()
    dim_metrics.columns = [dimension, 'Sales', 'Profit', 'Orders', 'Customers']
    dim_metrics['Profit Margin'] = (dim_metrics['Profit'] / dim_metrics['Sales'] * 100).round(2)
    dim_metrics['Avg Order Value'] = (dim_metrics['Sales'] / dim_metrics['Orders']).round(2)
    dim_metrics['Efficiency Score'] = ((dim_metrics['Profit Margin'] / 100) * 
                                       (dim_metrics['Sales'] / dim_metrics['Sales'].max()) * 100).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(dim_metrics, x=dimension, y='Efficiency Score',
                    color='Efficiency Score', color_continuous_scale='RdYlGn',
                    title=f'Efficiency Score by {dimension}')
        fig.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(dim_metrics, x='Sales', y='Profit Margin',
                        size='Orders', color=dimension,
                        hover_data=[dimension, 'Avg Order Value'],
                        title=f'Sales vs Profit Margin by {dimension}')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance summary table
    st.markdown("---")
    st.markdown("### 📋 Detailed Performance Summary")
    st.dataframe(dim_metrics.style.background_gradient(subset=['Sales', 'Profit', 'Profit Margin', 'Efficiency Score']), 
                 use_container_width=True)

