"""
Time Series Analysis - Temporal trends and patterns
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data

def render():
    st.title("📅 Time Series Analysis")
    
    df = load_data()
    if df is None:
        st.error("Dataset not loaded. Please run download_dataset.py first.")
        return
    
    # Time period selection
    col1, col2 = st.columns(2)
    
    with col1:
        time_granularity = st.selectbox("Time Granularity", 
                                       ['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly'])
    
    with col2:
        metric = st.selectbox("Metric", ['Sales', 'Profit', 'Quantity', 'Orders'])
    
    # Prepare time series data
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    
    if time_granularity == 'Daily':
        df['Time Period'] = df['Order Date'].dt.date
    elif time_granularity == 'Weekly':
        df['Time Period'] = df['Order Date'].dt.to_period('W').astype(str)
    elif time_granularity == 'Monthly':
        df['Time Period'] = df['Order Date'].dt.to_period('M').astype(str)
    elif time_granularity == 'Quarterly':
        df['Time Period'] = df['Order Date'].dt.to_period('Q').astype(str)
    else:
        df['Time Period'] = df['Order Date'].dt.year.astype(str)
    
    if metric == 'Orders':
        time_series = df.groupby('Time Period')['Order ID'].nunique().reset_index()
        time_series.columns = ['Time Period', metric]
    else:
        time_series = df.groupby('Time Period')[metric].sum().reset_index()
    
    time_series = time_series.sort_values('Time Period')
    
    # Main time series chart
    st.markdown(f"### {metric} Over Time ({time_granularity})")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_series['Time Period'],
        y=time_series[metric],
        mode='lines+markers',
        name=metric,
        line=dict(color='#667eea', width=3),
        marker=dict(size=8)
    ))
    
    # Add moving average
    window = st.slider("Moving Average Window", 2, 12, 3)
    time_series[f'{metric} MA'] = time_series[metric].rolling(window=window, center=True).mean()
    
    fig.add_trace(go.Scatter(
        x=time_series['Time Period'],
        y=time_series[f'{metric} MA'],
        mode='lines',
        name=f'Moving Average ({window})',
        line=dict(color='#ff6b6b', width=2, dash='dash')
    ))
    
    fig.update_layout(
        height=500,
        xaxis_title="Time Period",
        yaxis_title=metric,
        hovermode='x unified',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Multiple metrics comparison
    st.markdown("### 📊 Multiple Metrics Comparison")
    
    multi_metric = df.groupby('Time Period').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    multi_metric.columns = ['Time Period', 'Sales', 'Profit', 'Quantity', 'Orders']
    multi_metric = multi_metric.sort_values('Time Period')
    
    selected_metrics = st.multiselect("Select Metrics to Compare", 
                                    ['Sales', 'Profit', 'Quantity', 'Orders'],
                                    default=['Sales', 'Profit'])
    
    if selected_metrics:
        fig = go.Figure()
        colors = ['#667eea', '#ff6b6b', '#4ecdc4', '#ffe66d']
        
        for i, metric_name in enumerate(selected_metrics):
            # Normalize for better comparison
            normalized = (multi_metric[metric_name] - multi_metric[metric_name].min()) / \
                        (multi_metric[metric_name].max() - multi_metric[metric_name].min())
            
            fig.add_trace(go.Scatter(
                x=multi_metric['Time Period'],
                y=normalized,
                mode='lines+markers',
                name=metric_name,
                line=dict(color=colors[i % len(colors)], width=2)
            ))
        
        fig.update_layout(
            height=500,
            xaxis_title="Time Period",
            yaxis_title="Normalized Value",
            hovermode='x unified',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Seasonal analysis
    st.markdown("---")
    st.markdown("### 🗓️ Seasonal Patterns")
    
    df['Month'] = df['Order Date'].dt.month_name()
    df['Year'] = df['Order Date'].dt.year
    
    monthly_pattern = df.groupby('Month')['Sales'].mean().reset_index()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_pattern['Month'] = pd.Categorical(monthly_pattern['Month'], categories=month_order, ordered=True)
    monthly_pattern = monthly_pattern.sort_values('Month')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(monthly_pattern, x='Month', y='Sales',
                     color='Sales', color_continuous_scale='Blues')
        fig.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Year-over-year comparison
        yearly_monthly = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
        yearly_monthly['Month'] = pd.Categorical(yearly_monthly['Month'], categories=month_order, ordered=True)
        yearly_monthly = yearly_monthly.sort_values(['Year', 'Month'])
        
        fig = px.line(yearly_monthly, x='Month', y='Sales', color='Year',
                     markers=True)
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Trend analysis
    st.markdown("---")
    st.markdown("### 📈 Trend Analysis")
    
    # Calculate growth rates
    time_series['Growth Rate'] = time_series[metric].pct_change() * 100
    time_series['Cumulative Growth'] = ((time_series[metric] / time_series[metric].iloc[0]) - 1) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(time_series, x='Time Period', y='Growth Rate',
                     color='Growth Rate', color_continuous_scale='RdYlGn',
                     title='Period-over-Period Growth Rate (%)')
        fig.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(time_series, x='Time Period', y='Cumulative Growth',
                     markers=True, title='Cumulative Growth from Start (%)')
        fig.update_layout(height=400, xaxis_tickangle=-45)
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig, use_container_width=True)

