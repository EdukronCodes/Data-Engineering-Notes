"""
Utility functions for data loading and processing
"""
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Load the Superstore dataset"""
    try:
        df = pd.read_csv("superstore.csv")
        # Convert date columns
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        if 'Ship Date' in df.columns:
            df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error("Dataset not found! Please run download_dataset.py first.")
        return None

def get_summary_stats(df):
    """Get summary statistics for the dataset"""
    if df is None or df.empty:
        return {}
    
    return {
        'total_sales': df['Sales'].sum() if 'Sales' in df.columns else 0,
        'total_profit': df['Profit'].sum() if 'Profit' in df.columns else 0,
        'total_orders': len(df),
        'total_customers': df['Customer ID'].nunique() if 'Customer ID' in df.columns else 0,
        'total_products': df['Product ID'].nunique() if 'Product ID' in df.columns else 0,
        'date_range': (df['Order Date'].min(), df['Order Date'].max()) if 'Order Date' in df.columns else (None, None)
    }

