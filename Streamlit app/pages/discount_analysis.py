"""
Discount Impact Analysis - Effect of discounts on sales
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

def render():
    st.title("🎯 Discount Impact Analysis")
    
    df = load_data()
    if df is None:
        st.error("Dataset not loaded. Please run download_dataset.py first.")
        return
    
    # Discount categories
    df['Discount Category'] = pd.cut(df['Discount'], 
                                     bins=[0, 0.1, 0.2, 0.3, 0.5, 1.0],
                                     labels=['0-10%', '10-20%', '20-30%', '30-50%', '50%+'])
    
    # Overall discount metrics
    st.markdown("### 📊 Discount Overview")
    
    total_discount_value = (df['Sales'] * df['Discount']).sum()
    avg_discount = df['Discount'].mean() * 100
    discounted_orders = len(df[df['Discount'] > 0])
    total_orders = len(df)
    discount_rate = (discounted_orders / total_orders * 100) if total_orders > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Discount Value", f"${total_discount_value:,.2f}")
    with col2:
        st.metric("Average Discount", f"{avg_discount:.2f}%")
    with col3:
        st.metric("Discounted Orders", f"{discounted_orders:,} ({discount_rate:.1f}%)")
    with col4:
        st.metric("Orders with No Discount", f"{total_orders - discounted_orders:,}")
    
    st.markdown("---")
    
    # Discount impact on sales and profit
    st.markdown("### 💰 Discount Impact on Sales & Profit")
    
    discount_impact = df.groupby('Discount Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    discount_impact['Profit Margin'] = (discount_impact['Profit'] / discount_impact['Sales'] * 100).round(2)
    discount_impact['Avg Order Value'] = (discount_impact['Sales'] / discount_impact['Order ID']).round(2)
    
    # Add no discount category
    no_discount = df[df['Discount'] == 0].agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique'
    })
    no_discount['Discount Category'] = 'No Discount'
    no_discount['Profit Margin'] = (no_discount['Profit'] / no_discount['Sales'] * 100) if no_discount['Sales'] > 0 else 0
    no_discount['Avg Order Value'] = (no_discount['Sales'] / no_discount['Order ID']) if no_discount['Order ID'] > 0 else 0
    
    discount_impact = pd.concat([pd.DataFrame([no_discount]), discount_impact], ignore_index=True)
    
    st.dataframe(discount_impact.style.background_gradient(subset=['Sales', 'Profit', 'Profit Margin']), 
                 use_container_width=True)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(discount_impact, x='Discount Category', y='Sales',
                    color='Sales', color_continuous_scale='Blues',
                    title='Total Sales by Discount Level')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(discount_impact, x='Discount Category', y='Profit',
                    color='Profit', color_continuous_scale='RdYlGn',
                    title='Total Profit by Discount Level')
        fig.update_layout(showlegend=False, height=400)
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    
    # Profit margin by discount
    st.markdown("---")
    st.markdown("### 📈 Profit Margin Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(discount_impact, x='Discount Category', y='Profit Margin',
                    color='Profit Margin', color_continuous_scale='RdYlGn',
                    title='Profit Margin by Discount Level (%)')
        fig.update_layout(showlegend=False, height=400)
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Discount vs Profit scatter
        sample_df = df.sample(min(2000, len(df)))
        fig = px.scatter(sample_df, x='Discount', y='Profit',
                        color='Category', size='Sales',
                        hover_data=['Product Name'],
                        title='Discount vs Profit by Category')
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Discount by category
    st.markdown("---")
    st.markdown("### 📦 Discount Usage by Category")
    
    category_discount = df.groupby(['Category', 'Discount Category']).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig = px.sunburst(category_discount, path=['Category', 'Discount Category'], 
                     values='Sales', color='Profit',
                     color_continuous_scale='RdYlGn',
                     title='Sales Distribution: Category × Discount Level')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Discount effectiveness
    st.markdown("---")
    st.markdown("### 🎯 Discount Effectiveness Analysis")
    
    # Compare discounted vs non-discounted
    comparison = df.groupby(df['Discount'] > 0).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    comparison.columns = ['Has Discount', 'Sales', 'Profit', 'Quantity', 'Orders']
    comparison['Has Discount'] = comparison['Has Discount'].map({True: 'With Discount', False: 'No Discount'})
    comparison['Profit Margin'] = (comparison['Profit'] / comparison['Sales'] * 100).round(2)
    comparison['Avg Order Value'] = (comparison['Sales'] / comparison['Orders']).round(2)
    
    st.dataframe(comparison.style.background_gradient(subset=['Sales', 'Profit', 'Profit Margin']), 
                 use_container_width=True)
    
    # Discount trends over time
    st.markdown("---")
    st.markdown("### 📅 Discount Trends Over Time")
    
    df['Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
    monthly_discount = df.groupby('Year-Month').agg({
        'Discount': 'mean',
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    monthly_discount['Discount'] = monthly_discount['Discount'] * 100
    monthly_discount = monthly_discount.sort_values('Year-Month')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_discount['Year-Month'],
        y=monthly_discount['Discount'],
        mode='lines+markers',
        name='Average Discount (%)',
        line=dict(color='#667eea', width=3),
        yaxis='y'
    ))
    fig.add_trace(go.Scatter(
        x=monthly_discount['Year-Month'],
        y=monthly_discount['Profit'],
        mode='lines+markers',
        name='Total Profit',
        line=dict(color='#4ecdc4', width=2, dash='dash'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        height=500,
        xaxis_title="Month",
        yaxis=dict(title="Average Discount (%)", side='left'),
        yaxis2=dict(title="Total Profit ($)", overlaying='y', side='right'),
        hovermode='x unified',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)

