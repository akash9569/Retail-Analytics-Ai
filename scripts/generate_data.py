import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_retail_data(start_date='2021-01-01', end_date='2024-12-31', num_orders=15000):
    """
    Generates a synthetic retail sales dataset with realistic patterns.
    """
    print("Generating synthetic retail sales data...")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Date range
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    date_range = (end - start).days
    
    # Definitions
    categories = {
        'Furniture': ['Bookcases', 'Chairs', 'Tables', 'Furnishings'],
        'Office Supplies': ['Labels', 'Storage', 'Art', 'Binders', 'Appliances', 'Paper', 'Accessories', 'Envelopes', 'Fasteners', 'Supplies'],
        'Technology': ['Phones', 'Accessories', 'Copiers', 'Machines'],
        'Clothing': ['T-Shirts', 'Trousers', 'Jackets', 'Dresses'],
        'Home & Garden': ['Garden Tools', 'Plants', 'Decor', 'Kitchenware']
    }
    
    regions = {
        'West': ['California', 'Washington', 'Oregon', 'Arizona'],
        'East': ['New York', 'Pennsylvania', 'Ohio', 'Massachusetts'],
        'Central': ['Texas', 'Illinois', 'Michigan', 'Indiana'],
        'South': ['Florida', 'North Carolina', 'Virginia', 'Tennessee']
    }
    
    segments = ['Consumer', 'Corporate', 'Home Office']
    ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
    
    data = []
    
    # Seasonal weights (Month 1-12) - Higher sales in Q4 (Holiday season)
    seasonal_weights = [0.8, 0.8, 0.9, 0.9, 1.0, 1.0, 1.1, 1.1, 1.2, 1.1, 1.3, 1.5]
    
    for order_id in range(1, num_orders + 1):
        # Generate Order Date with seasonality
        days_offset = np.random.randint(0, date_range)
        order_date = start + timedelta(days=days_offset)
        
        # Adjust probability based on month (seasonality)
        month_idx = order_date.month - 1
        if np.random.random() > (seasonal_weights[month_idx] / 2.0): # Simple rejection sampling for seasonality
             days_offset = np.random.randint(0, date_range)
             order_date = start + timedelta(days=days_offset)
        
        # Generate Ship Date (0-5 days after Order Date)
        ship_date = order_date + timedelta(days=np.random.randint(0, 6))
        
        # Category & Product
        category = np.random.choice(list(categories.keys()))
        subcategory = np.random.choice(categories[category])
        product_name = f"{np.random.choice(['Acme', 'Global', 'Best', 'Value', 'Premium'])} {subcategory} {np.random.randint(100, 999)}"
        
        # Region & Location
        region = np.random.choice(list(regions.keys()))
        state = np.random.choice(regions[region])
        city = f"{state} City {np.random.randint(1, 5)}"
        
        # Customer
        segment = np.random.choice(segments, p=[0.5, 0.3, 0.2])
        customer_id = f"C-{np.random.randint(1000, 5000)}"
        customer_name = f"Customer {customer_id}"
        
        # Sales Details
        quantity = np.random.randint(1, 10)
        
        # Base price depends on category
        if category == 'Technology':
            base_price = np.random.uniform(100, 2000)
        elif category == 'Furniture':
            base_price = np.random.uniform(50, 1000)
        elif category == 'Office Supplies':
            base_price = np.random.uniform(5, 100)
        elif category == 'Clothing':
            base_price = np.random.uniform(20, 200)
        else: # Home & Garden
            base_price = np.random.uniform(10, 300)
            
        unit_price = round(base_price, 2)
        
        # Discount
        discount = 0.0
        if np.random.random() < 0.3: # 30% chance of discount
            discount = np.random.choice([0.1, 0.2, 0.3, 0.4, 0.5])
            
        # Holiday spike (Black Friday / Christmas)
        if (order_date.month == 11 and order_date.day > 20) or (order_date.month == 12 and order_date.day < 25):
             quantity += np.random.randint(1, 5)
             discount = max(discount, 0.2) # Minimum 20% discount during holidays
        
        total_sales = round(unit_price * quantity * (1 - discount), 2)
        
        # Profit (Random margin between -10% to 40% depending on discount)
        margin = np.random.uniform(0.2, 0.4) - discount
        profit = round(total_sales * margin, 2)
        
        data.append([
            order_id, order_date, ship_date, ship_modes[np.random.randint(0, 4)],
            customer_id, customer_name, segment,
            city, state, region,
            category, subcategory, product_name,
            unit_price, quantity, discount, total_sales, profit
        ])
        
    columns = [
        'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
        'Customer ID', 'Customer Name', 'Segment',
        'City', 'State', 'Region',
        'Category', 'Sub-Category', 'Product Name',
        'Unit Price', 'Quantity', 'Discount', 'Total Sales', 'Profit'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    
    # Sort by Order Date
    df = df.sort_values('Order Date').reset_index(drop=True)
    
    # Add some outliers
    print("Adding outliers...")
    indices = np.random.choice(df.index, size=int(num_orders * 0.005), replace=False) # 0.5% outliers
    df.loc[indices, 'Total Sales'] = df.loc[indices, 'Total Sales'] * np.random.uniform(3, 5)
    df.loc[indices, 'Profit'] = df.loc[indices, 'Profit'] * np.random.uniform(2, 4)
    
    # Save to CSV
    output_path = os.path.join('data', 'raw', 'retail_sales_dataset.csv')
    df.to_csv(output_path, index=False)
    print(f"Dataset generated successfully: {output_path}")
    print(f"Shape: {df.shape}")
    print(f"Date Range: {df['Order Date'].min()} to {df['Order Date'].max()}")
    
    return df

if __name__ == "__main__":
    generate_retail_data()
