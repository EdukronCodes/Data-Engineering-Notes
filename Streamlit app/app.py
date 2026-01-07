"""
Main Streamlit App - Superstore Sales Analysis
Custom navigation without sidebar
"""
import streamlit as st
from pages import (
    home, overview, regional_analysis, product_analysis, 
    customer_analysis, time_series, profit_analysis, 
    discount_analysis, shipping_analysis, category_analysis,
    segment_analysis, performance_metrics
)

# Page configuration
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide the default Streamlit sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .nav-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation dictionary
PAGES = {
    "🏠 Home": home,
    "📈 Overview Dashboard": overview,
    "🌍 Regional Analysis": regional_analysis,
    "📦 Product Analysis": product_analysis,
    "👥 Customer Analysis": customer_analysis,
    "📅 Time Series Analysis": time_series,
    "💰 Profit Analysis": profit_analysis,
    "🎯 Discount Impact": discount_analysis,
    "🚚 Shipping Analysis": shipping_analysis,
    "📊 Category Deep Dive": category_analysis,
    "🏢 Segment Analysis": segment_analysis,
    "⚡ Performance Metrics": performance_metrics,
}

def main():
    # Header
    st.markdown('<div class="main-header"><h1>📊 Superstore Sales Analytics Dashboard</h1></div>', unsafe_allow_html=True)
    
    # Navigation container
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    # Create navigation using columns
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_page = st.selectbox(
            "Navigate to Page:",
            options=list(PAGES.keys()),
            key="page_selector",
            label_visibility="visible"
        )
    
    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Render selected page
    if selected_page in PAGES:
        PAGES[selected_page].render()

if __name__ == "__main__":
    main()

