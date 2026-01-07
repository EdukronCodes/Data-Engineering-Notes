"""
Profit Analysis - Profitability insights
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

def render():
    st.title("💰 Profit Analysis")
    
    df = load_data()
    if df is None:
        st.error("Dataset not loaded. Please run download_dataset.py first.")
        return
    
    # Overall profit metrics
    st.markdown("### 📊 Profit Overview")
    
    total_profit = df['Profit'].sum()
    total_sales = df['Sales'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    profitable_orders = len(df[df['Profit'] > 0])
    total_orders = len(df)
    profitability_rate = (profitable_orders / total_orders * 100) if total_orders > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Profit", f"${total_profit:,.2f}")
    with col2:
        st.metric("Profit Margin", f"{profit_margin:.2f}%")
    with col3:
        st.metric("Profitable Orders", f"{profitable_orders:,} ({profitability_rate:.1f}%)")
    with col4:
        st.metric("Average Profit per Order", f"${(total_profit / total_orders):,.2f}")
    
    st.markdown("---")
    
    # Profit distribution
    st.markdown("### 📈 Profit Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Profit histogram
        fig = px.histogram(df, x='Profit', nbins=50,
                          title='Distribution of Profit per Order',
                          labels={'Profit': 'Profit ($)', 'count': 'Number of Orders'})
        fig.update_layout(height=400)
        fig.add_vline(x=0, line_dash="dash", line_color="red", 
                     annotation_text="Break-even")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Profit vs Sales
        sample_df = df.sample(min(2000, len(df)))
        fig = px.scatter(sample_df, x='Sales', y='Profit',
                        color='Category', size='Quantity',
                        hover_data=['Product Name'],
                        title='Profit vs Sales by Category')
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Profit by different dimensions
    st.markdown("---")
    st.markdown("### 🎯 Profit by Dimension")
    
    dimension = st.selectbox("Analyze Profit by", 
                            ['Region', 'Category', 'Sub-Category', 'Segment', 'Ship Mode'])
    
    profit_by_dim = df.groupby(dimension).agg({
        'Profit': 'sum',
        'Sales': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    profit_by_dim['Profit Margin'] = (profit_by_dim['Profit'] / profit_by_dim['Sales'] * 100).round(2)
    profit_by_dim = profit_by_dim.sort_values('Profit', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(profit_by_dim, x=dimension, y='Profit',
                    color='Profit', color_continuous_scale='RdYlGn',
                    title=f'Total Profit by {dimension}')
        fig.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(profit_by_dim, x=dimension, y='Profit Margin',
                    color='Profit Margin', color_continuous_scale='RdYlGn',
                    title=f'Profit Margin by {dimension} (%)')
        fig.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    
    # Top and bottom performers
    st.markdown("---")
    st.markdown("### 🏆 Top & Bottom Profit Performers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top 10 Most Profitable Products")
        top_profit = df.groupby('Product Name')['Profit'].sum().nlargest(10).reset_index()
        fig = px.bar(top_profit, x='Profit', y='Product Name', orientation='h',
                    color='Profit', color_continuous_scale='Greens')
        fig.update_layout(showlegend=False, height=400, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Bottom 10 Least Profitable Products")
        bottom_profit = df.groupby('Product Name')['Profit'].sum().nsmallest(10).reset_index()
        fig = px.bar(bottom_profit, x='Profit', y='Product Name', orientation='h',
                    color='Profit', color_continuous_scale='Reds')
        fig.update_layout(showlegend=False, height=400, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Profit trends over time
    st.markdown("---")
    st.markdown("### 📅 Profit Trends Over Time")
    
    df['Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
    monthly_profit = df.groupby('Year-Month').agg({
        'Profit': 'sum',
        'Sales': 'sum'
    }).reset_index()
    monthly_profit['Profit Margin'] = (monthly_profit['Profit'] / monthly_profit['Sales'] * 100).round(2)
    monthly_profit = monthly_profit.sort_values('Year-Month')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_profit['Year-Month'],
        y=monthly_profit['Profit'],
        mode='lines+markers',
        name='Total Profit',
        line=dict(color='#4ecdc4', width=3),
        yaxis='y'
    ))
    fig.add_trace(go.Scatter(
        x=monthly_profit['Year-Month'],
        y=monthly_profit['Profit Margin'],
        mode='lines+markers',
        name='Profit Margin (%)',
        line=dict(color='#ff6b6b', width=2, dash='dash'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        height=500,
        xaxis_title="Month",
        yaxis=dict(title="Total Profit ($)", side='left'),
        yaxis2=dict(title="Profit Margin (%)", overlaying='y', side='right'),
        hovermode='x unified',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

