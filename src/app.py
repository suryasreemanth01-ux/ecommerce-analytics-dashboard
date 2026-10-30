import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os
import numpy as np
from sklearn.linear_model import LinearRegression

# Set page configuration
st.set_page_config(page_title="E-commerce Analytics Dashboard", page_icon="📊", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .kpi-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: #1f77b4;
    }
    .kpi-label {
        font-size: 14px;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection function
def get_data_from_db():
    db_path = 'data/ecommerce.db'
    if not os.path.exists(db_path):
        st.error(f"Database not found at {db_path}. Please run db_setup.py first.")
        st.stop()
        
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM sales"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Convert date column to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

# Load data
df = get_data_from_db()

# Sidebar Filters
st.sidebar.header("Filter Options")

# Date Range Filter
min_date = df['Order Date'].min()
max_date = df['Order Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Category Filter
categories = df['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", options=categories, default=categories)

# Region Filter
regions = df['Region'].unique()
selected_regions = st.sidebar.multiselect("Select Regions", options=regions, default=regions)

# Apply filters
filtered_df = df[
    (df['Order Date'].dt.date >= start_date) & 
    (df['Order Date'].dt.date <= end_date) &
    (df['Category'].isin(selected_categories)) &
    (df['Region'].isin(selected_regions))
]

# Main Dashboard Title
st.title("📊 E-commerce Business Analytics Dashboard")
st.markdown("Interactive dashboard to analyze sales, profit, and customer behavior.")

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your criteria.")
    st.stop()

# KPI Calculations
total_revenue = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order ID'].nunique()
aov = total_revenue / total_orders if total_orders > 0 else 0

# Display KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Revenue</div><div class="kpi-value">${total_revenue:,.2f}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Profit</div><div class="kpi-value">${total_profit:,.2f}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Orders</div><div class="kpi-value">{total_orders:,}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Avg Order Value</div><div class="kpi-value">${aov:,.2f}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Monthly Sales Trend")
    monthly_sales = filtered_df.set_index('Order Date').resample('M')['Sales'].sum().reset_index()
    fig_line = px.line(monthly_sales, x='Order Date', y='Sales', markers=True, template="plotly_white")
    st.plotly_chart(fig_line, width='stretch')

with col_right:
    st.subheader("Sales by Category")
    category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
    fig_pie = px.pie(category_sales, values='Sales', names='Category', hole=0.3, template="plotly_white")
    st.plotly_chart(fig_pie, width='stretch')

# Top Products
st.subheader("Top 10 Products by Revenue (Filtered View)")
top_products = filtered_df.groupby('Product')['Sales'].sum().nlargest(10).reset_index()
fig_bar = px.bar(top_products, x='Sales', y='Product', orientation='h', template="plotly_white", color='Sales', color_continuous_scale='Blues')
st.plotly_chart(fig_bar, width='stretch')

st.markdown("---")

# Machine Learning: Sales Forecasting
st.subheader("🔮 Sales Forecasting (Machine Learning)")
st.markdown("Using Linear Regression on the filtered monthly data to predict the next 3 months of revenue.")

if len(monthly_sales) > 3:
    # Prepare data for ML
    monthly_sales['Month_Num'] = range(len(monthly_sales))
    
    X = monthly_sales[['Month_Num']]
    y = monthly_sales['Sales']
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next 3 months
    last_month_num = monthly_sales['Month_Num'].max()
    future_months = np.array([[last_month_num + 1], [last_month_num + 2], [last_month_num + 3]])
    predictions = model.predict(future_months)
    
    # Create future dates for plotting
    last_date = monthly_sales['Order Date'].max()
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=3, freq='M')
    
    # Create forecast dataframe
    forecast_df = pd.DataFrame({'Order Date': future_dates, 'Sales': predictions})
    
    # Plot historical + forecast
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(x=monthly_sales['Order Date'], y=monthly_sales['Sales'], mode='lines+markers', name='Historical Sales'))
    fig_forecast.add_trace(go.Scatter(x=forecast_df['Order Date'], y=forecast_df['Sales'], mode='lines+markers', name='Forecast', line=dict(dash='dash', color='red')))
    
    fig_forecast.update_layout(title="Revenue Forecast (Next 3 Months)", xaxis_title="Date", yaxis_title="Revenue", template="plotly_white")
    st.plotly_chart(fig_forecast, width='stretch')
    
    st.info("Note: This is a simple linear trend forecast based on the filtered data. Real-world forecasts should account for seasonality and external factors.")
else:
    st.warning("Not enough data points to generate a forecast. Please widen your date filters.")

st.markdown("---")

# SQL Analytics Section
st.subheader("🗄️ Raw SQL Analytics (Entire Database)")
st.markdown("These tables demonstrate direct SQL queries executed against the database (ignoring the UI filters above).")

# Run a specific SQL query for the dashboard
conn = sqlite3.connect('data/ecommerce.db')
query_sql = """
SELECT Product, ROUND(SUM(Sales), 2) as Total_Revenue, ROUND(SUM(Profit), 2) as Total_Profit
FROM sales
GROUP BY Product
ORDER BY Total_Revenue DESC
LIMIT 5;
"""
sql_result = pd.read_sql_query(query_sql, conn)
conn.close()

st.dataframe(sql_result, width='stretch')

st.markdown("---")

# Download Filtered Data
st.subheader("📥 Download Filtered Data")
st.markdown("Click the button below to download the data based on your current filters as a CSV file.")

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_df)

st.download_button(
    label="Download Data as CSV",
    data=csv,
    file_name='filtered_ecommerce_data.csv',
    mime='text/csv',
)
