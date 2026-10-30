import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define base parameters
num_orders = 2000
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

# Categories and products
categories = {
    'Electronics': ['Laptop', 'Smartphone', 'Headphones', 'Monitor', 'Keyboard'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Hat'],
    'Home & Kitchen': ['Blender', 'Coffee Maker', 'Pan Set', 'Toaster', 'Knife Set'],
    'Books': ['Fiction Novel', 'Biography', 'Cookbook', 'Self-Help', 'History Book']
}

regions = ['North America', 'Europe', 'Asia', 'South America', 'Australia']

# Generate data
data = []
for i in range(num_orders):
    order_id = f"ORD-{10000 + i}"
    
    # Random date
    random_days = random.randint(0, (end_date - start_date).days)
    order_date = start_date + timedelta(days=random_days)
    
    # Random category and product
    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category])
    
    # Quantity and pricing logic
    quantity = random.randint(1, 5)
    
    # Base prices per category (to simulate realistic variation)
    base_price = {
        'Electronics': random.uniform(100, 1500),
        'Clothing': random.uniform(15, 100),
        'Home & Kitchen': random.uniform(20, 200),
        'Books': random.uniform(10, 50)
    }[category]
    
    unit_price = round(base_price, 2)
    sales = round(unit_price * quantity, 2)
    
    # Cost is typically 40% to 70% of sales (simulating profit margins)
    cost_ratio = random.uniform(0.4, 0.7)
    cost = round(sales * cost_ratio, 2)
    profit = round(sales - cost, 2)
    
    # Customer and region
    customer = f"CUST-{random.randint(1000, 5000)}"
    region = random.choice(regions)
    
    data.append({
        'Order ID': order_id,
        'Order Date': order_date.strftime('%Y-%m-%d'),
        'Category': category,
        'Product': product,
        'Quantity': quantity,
        'Unit Price': unit_price,
        'Sales': sales,
        'Cost': cost,
        'Profit': profit,
        'Customer': customer,
        'Region': region
    })

# Create DataFrame
df = pd.DataFrame(data)

# Ensure data folder exists
os.makedirs('data', exist_ok=True)

# Save to CSV
output_path = 'data/synthetic_ecommerce_data.csv'
df.to_csv(output_path, index=False)

print(f"Successfully generated {len(df)} rows of synthetic data.")
print(f"File saved to: {output_path}")
print("\nFirst 5 rows of the dataset:")
print(df.head())
