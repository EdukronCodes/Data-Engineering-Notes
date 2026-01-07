# Superstore Sales Analytics Dashboard

A comprehensive Streamlit multi-page application for analyzing Superstore sales data with custom navigation (no sidebar).

## Features

- **12 Different Analysis Pages**:
  1. 🏠 Home - Welcome page with quick statistics
  2. 📈 Overview Dashboard - High-level metrics and KPIs
  3. 🌍 Regional Analysis - Sales performance by region
  4. 📦 Product Analysis - Product performance and trends
  5. 👥 Customer Analysis - Customer segmentation and behavior
  6. 📅 Time Series Analysis - Temporal trends and patterns
  7. 💰 Profit Analysis - Profitability insights
  8. 🎯 Discount Impact - Effect of discounts on sales
  9. 🚚 Shipping Analysis - Shipping mode performance
  10. 📊 Category Deep Dive - Detailed category analysis
  11. 🏢 Segment Analysis - Business segment performance
  12. ⚡ Performance Metrics - Key performance indicators

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Download the dataset:
```bash
python download_dataset.py
```

This will either download the Superstore dataset from a public source or create a sample dataset if the download fails.

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default web browser. Use the dropdown menu at the top to navigate between different analysis pages.

## Navigation

- **No Sidebar Navigation**: All navigation happens through the dropdown menu in the main content area
- **Custom Styling**: Modern, clean interface with gradient headers
- **Interactive Visualizations**: All charts are interactive using Plotly

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── utils.py              # Utility functions for data loading
├── download_dataset.py   # Script to download/create dataset
├── requirements.txt      # Python dependencies
├── superstore.csv        # Dataset file (created after running download_dataset.py)
└── pages/                # Page modules
    ├── __init__.py
    ├── home.py
    ├── overview.py
    ├── regional_analysis.py
    ├── product_analysis.py
    ├── customer_analysis.py
    ├── time_series.py
    ├── profit_analysis.py
    ├── discount_analysis.py
    ├── shipping_analysis.py
    ├── category_analysis.py
    ├── segment_analysis.py
    └── performance_metrics.py
```

## Features of Each Page

### Home
- Quick statistics overview
- Dataset information
- Data preview

### Overview Dashboard
- Key performance indicators
- Filterable by region, category, and year
- Multiple chart visualizations

### Regional Analysis
- Regional performance comparison
- State-level analysis
- Category performance by region

### Product Analysis
- Top performing products
- Sub-category analysis
- Product trends over time

### Customer Analysis
- Customer segment performance
- Top customers
- Customer value distribution
- Purchase patterns

### Time Series Analysis
- Multiple time granularities (daily, weekly, monthly, etc.)
- Moving averages
- Seasonal patterns
- Growth rate analysis

### Profit Analysis
- Profit distribution
- Profit by various dimensions
- Top and bottom performers
- Profit trends

### Discount Impact
- Discount usage analysis
- Impact on sales and profit
- Discount effectiveness
- Trends over time

### Shipping Analysis
- Shipping mode performance
- Shipping efficiency metrics
- Regional shipping patterns
- Shipping trends

### Category Deep Dive
- Detailed category analysis
- Sub-category breakdown
- Top products by category
- Category trends

### Segment Analysis
- Business segment performance
- Segment comparison
- Trends over time
- Top customers by segment

### Performance Metrics
- Overall KPIs
- Performance scorecard
- Efficiency metrics
- Performance by dimension

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computations

## Notes

- The dataset is cached for better performance
- All visualizations are interactive
- Filters can be applied on most pages
- The app uses custom CSS to hide the default sidebar

