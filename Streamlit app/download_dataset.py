"""
Script to download the Superstore Sales Dataset
"""
import pandas as pd
import os

def download_superstore_dataset():
    """Download Superstore dataset from a public URL"""
    # Using a public dataset URL - Superstore sample dataset
    url = "https://raw.githubusercontent.com/nileshely/SuperStore-Dataset-2019-2022/main/Superstore.csv"
    
    try:
        print("Downloading Superstore dataset...")
        df = pd.read_csv(url)
        df.to_csv("superstore.csv", index=False)
        print(f"Dataset downloaded successfully! Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error downloading from URL: {e}")
        print("Creating sample dataset...")
        # Create a sample dataset if download fails
        return create_sample_dataset()

def create_sample_dataset():
    """Create a sample Superstore dataset if download fails"""
    import random
    from datetime import datetime, timedelta
    
    # Generate sample data
    regions = ['West', 'East', 'Central', 'South']
    categories = ['Furniture', 'Office Supplies', 'Technology']
    subcategories = {
        'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
        'Office Supplies': ['Storage', 'Art', 'Binders', 'Appliances'],
        'Technology': ['Phones', 'Accessories', 'Machines', 'Copiers']
    }
    ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
    segments = ['Consumer', 'Corporate', 'Home Office']
    
    data = []
    start_date = datetime(2019, 1, 1)
    
    for i in range(10000):
        region = random.choice(regions)
        category = random.choice(categories)
        subcategory = random.choice(subcategories[category])
        ship_mode = random.choice(ship_modes)
        segment = random.choice(segments)
        
        order_date = start_date + timedelta(days=random.randint(0, 1460))
        sales = round(random.uniform(10, 5000), 2)
        quantity = random.randint(1, 10)
        discount = round(random.uniform(0, 0.5), 2)
        profit = round(sales * (1 - discount) * random.uniform(0.1, 0.3), 2)
        
        data.append({
            'Row ID': i + 1,
            'Order ID': f'US-{2019 + (i % 4)}-{100000 + i}',
            'Order Date': order_date.strftime('%Y-%m-%d'),
            'Ship Date': (order_date + timedelta(days=random.randint(1, 10))).strftime('%Y-%m-%d'),
            'Ship Mode': ship_mode,
            'Customer ID': f'CG-{10000 + (i % 1000)}',
            'Customer Name': f'Customer {i % 1000}',
            'Segment': segment,
            'Country': 'United States',
            'City': f'City {i % 50}',
            'State': f'State {i % 20}',
            'Postal Code': f'{10000 + (i % 90000)}',
            'Region': region,
            'Product ID': f'FUR-{category[:3].upper()}-{1000 + i}',
            'Category': category,
            'Sub-Category': subcategory,
            'Product Name': f'{subcategory} {i % 100}',
            'Sales': sales,
            'Quantity': quantity,
            'Discount': discount,
            'Profit': profit
        })
    
    df = pd.DataFrame(data)
    df.to_csv("superstore.csv", index=False)
    print(f"Sample dataset created! Shape: {df.shape}")
    return df

if __name__ == "__main__":
    download_superstore_dataset()

