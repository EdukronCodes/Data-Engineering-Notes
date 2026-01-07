"""
Home Page - Welcome and Introduction
"""
import streamlit as st
from utils import load_data, get_summary_stats

def render():
    st.title("🏠 Welcome to Superstore Sales Analytics")
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("⚠️ Dataset not found! Please run `python download_dataset.py` first.")
        st.info("💡 After downloading, refresh this page to see the dashboard.")
        return
    
    # Key metrics
    stats = get_summary_stats(df)
    
    st.markdown("---")
    st.markdown("### 📊 Quick Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sales", f"${stats['total_sales']:,.2f}")
    
    with col2:
        st.metric("Total Profit", f"${stats['total_profit']:,.2f}")
    
    with col3:
        st.metric("Total Orders", f"{stats['total_orders']:,}")
    
    with col4:
        st.metric("Total Customers", f"{stats['total_customers']:,}")
    
    st.markdown("---")
    
    # Introduction
    st.markdown("""
    ### 🎯 About This Dashboard
    
    This comprehensive analytics dashboard provides deep insights into Superstore sales data. 
    Navigate through different pages using the dropdown menu above to explore:
    
    - **Overview Dashboard**: High-level metrics and KPIs
    - **Regional Analysis**: Sales performance by region
    - **Product Analysis**: Product performance and trends
    - **Customer Analysis**: Customer segmentation and behavior
    - **Time Series Analysis**: Temporal trends and patterns
    - **Profit Analysis**: Profitability insights
    - **Discount Impact**: Effect of discounts on sales
    - **Shipping Analysis**: Shipping mode performance
    - **Category Deep Dive**: Detailed category analysis
    - **Segment Analysis**: Business segment performance
    - **Performance Metrics**: Key performance indicators
    
    ### 📈 Dataset Information
    
    - **Total Records**: {:,}
    - **Date Range**: {} to {}
    - **Total Products**: {:,}
    """.format(
        stats['total_orders'],
        stats['date_range'][0].strftime('%Y-%m-%d') if stats['date_range'][0] else 'N/A',
        stats['date_range'][1].strftime('%Y-%m-%d') if stats['date_range'][1] else 'N/A',
        stats['total_products']
    ))
    
    # Sample data preview
    with st.expander("👀 Preview Dataset"):
        st.dataframe(df.head(10), use_container_width=True)

