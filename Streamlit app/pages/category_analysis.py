"""
Category Deep Dive - Detailed category analysis
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

def render():
    st.title("📊 Category Deep Dive")
    
    df = load_data()
    if df is None:
        st.error("Dataset not loaded. Please run download_dataset.py first.")
        return
    
    # Category overview
    st.markdown("### 📈 Category Performance Overview")
    
    category_stats = df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique',
        'Customer ID': 'nunique'
    }).reset_index()
    category_stats.columns = ['Category', 'Sales', 'Profit', 'Quantity', 'Orders', 'Customers']
    category_stats['Profit Margin'] = (category_stats['Profit'] / category_stats['Sales'] * 100).round(2)
    category_stats['Avg Order Value'] = (category_stats['Sales'] / category_stats['Orders']).round(2)
    category_stats['Units per Order'] = (category_stats['Quantity'] / category_stats['Orders']).round(2)
    
    st.dataframe(category_stats.style.background_gradient(subset=['Sales', 'Profit', 'Profit Margin']), 
                 use_container_width=True)
    
    st.markdown("---")
    
    # Category selection for detailed analysis
    selected_category = st.selectbox("Select Category for Detailed Analysis", 
                                    sorted(df['Category'].unique().tolist()))
    
    category_df = df[df['Category'] == selected_category]
    
    # Sub-category analysis
    st.markdown(f"### 📦 Sub-Category Analysis: {selected_category}")
    
    subcat_stats = category_df.groupby('Sub-Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    subcat_stats.columns = ['Sub-Category', 'Sales', 'Profit', 'Quantity', 'Orders']
    subcat_stats['Profit Margin'] = (subcat_stats['Profit'] / subcat_stats['Sales'] * 100).round(2)
    subcat_stats = subcat_stats.sort_values('Sales', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(subcat_stats, x='Sub-Category', y='Sales',
                    color='Sales', color_continuous_scale='Blues',
                    title=f'Sales by Sub-Category ({selected_category})')
        fig.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(subcat_stats, x='Sub-Category', y='Profit Margin',
                    color='Profit Margin', color_continuous_scale='RdYlGn',
                    title=f'Profit Margin by Sub-Category ({selected_category})')
        fig.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    
    # Top products in category
    st.markdown("---")
    st.markdown(f"### 🏆 Top 15 Products in {selected_category}")
    
    top_products = category_df.groupby('Product Name').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index().nlargest(15, 'Sales')
    
    fig = px.bar(top_products, x='Sales', y='Product Name', orientation='h',
                color='Profit', color_continuous_scale='RdYlGn',
                hover_data=['Quantity'],
                title=f'Top Products by Sales ({selected_category})')
    fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Category trends over time
    st.markdown("---")
    st.markdown("### 📅 Category Trends Over Time")
    
    df['Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
    monthly_category = df.groupby(['Year-Month', 'Category']).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    monthly_category = monthly_category.sort_values('Year-Month')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(monthly_category, x='Year-Month', y='Sales', color='Category',
                     markers=True, title='Monthly Sales by Category')
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(monthly_category, x='Year-Month', y='Profit', color='Category',
                     markers=True, title='Monthly Profit by Category')
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Category comparison
    st.markdown("---")
    st.markdown("### 🔄 Category Comparison")
    
    comparison_metric = st.selectbox("Compare Categories by", 
                                    ['Sales', 'Profit', 'Profit Margin', 'Orders', 'Customers'])
    
    if comparison_metric == 'Profit Margin':
        fig = px.bar(category_stats, x='Category', y='Profit Margin',
                    color='Profit Margin', color_continuous_scale='RdYlGn',
                    title='Profit Margin Comparison')
    else:
        fig = px.bar(category_stats, x='Category', y=comparison_metric,
                    color=comparison_metric, color_continuous_scale='Blues',
                    title=f'{comparison_metric} Comparison')
    
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Category by region
    st.markdown("---")
    st.markdown("### 🌍 Category Performance by Region")
    
    region_category = df.groupby(['Region', 'Category']).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig = px.bar(region_category, x='Region', y='Sales', color='Category',
                barmode='group', color_discrete_sequence=px.colors.qualitative.Set2,
                title='Sales by Region and Category')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Category discount analysis
    st.markdown("---")
    st.markdown("### 🎯 Discount Usage by Category")
    
    category_discount = df.groupby('Category').agg({
        'Discount': 'mean',
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    category_discount['Avg Discount'] = (category_discount['Discount'] * 100).round(2)
    
    fig = px.scatter(category_discount, x='Avg Discount', y='Profit Margin',
                    size='Sales', color='Category',
                    hover_data=['Category'],
                    title='Discount vs Profit Margin by Category')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

