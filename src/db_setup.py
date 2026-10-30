import pandas as pd
import sqlite3
import os

# Define paths
csv_path = 'data/synthetic_ecommerce_data.csv'
db_path = 'data/ecommerce.db'

# Check if CSV exists
if not os.path.exists(csv_path):
    print(f"Error: Could not find {csv_path}. Please run the data generator first.")
    exit()

# Load data
df = pd.read_csv(csv_path)

# Create/Connect to SQLite database
conn = sqlite3.connect(db_path)

# Load data into a SQL table named 'sales'
# if_exists='replace' ensures we don't duplicate data if we run this script twice
df.to_sql('sales', conn, if_exists='replace', index=False)
print(f"Successfully loaded {len(df)} rows into the 'sales' table in {db_path}")

# --- SQL QUERIES ---

# Query 1: Top 5 Products by Revenue
print("\n--- Top 5 Products by Revenue ---")
query1 = """
SELECT Product, ROUND(SUM(Sales), 2) as Total_Revenue
FROM sales
GROUP BY Product
ORDER BY Total_Revenue DESC
LIMIT 5;
"""
result1 = pd.read_sql_query(query1, conn)
print(result1.to_string(index=False))

# Query 2: Revenue and Profit by Region
print("\n--- Revenue and Profit by Region ---")
query2 = """
SELECT Region, 
       ROUND(SUM(Sales), 2) as Total_Revenue, 
       ROUND(SUM(Profit), 2) as Total_Profit
FROM sales
GROUP BY Region
ORDER BY Total_Revenue DESC;
"""
result2 = pd.read_sql_query(query2, conn)
print(result2.to_string(index=False))

# Query 3: Monthly Sales Trend (using SQLite date functions)
print("\n--- Monthly Sales Trend (First 5 Months) ---")
query3 = """
SELECT strftime('%Y-%m', "Order Date") as Month, 
       ROUND(SUM(Sales), 2) as Total_Revenue
FROM sales
GROUP BY Month
ORDER BY Month ASC
LIMIT 5;
"""
result3 = pd.read_sql_query(query3, conn)
print(result3.to_string(index=False))

# Close connection
conn.close()
print("\nDatabase connection closed successfully.")
