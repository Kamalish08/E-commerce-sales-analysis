import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# ---------------------------
# Database Setup (Edit this)
# ---------------------------
# Example for PostgreSQL
engine = create_engine('postgresql://username:password@localhost:5432/ecommerce_db')

# ---------------------------
# Data Queries
# ---------------------------
@st.cache_data
def get_data():
    sales = pd.read_sql("SELECT * FROM sales", engine)
    products = pd.read_sql("SELECT * FROM products", engine)
    customers = pd.read_sql("SELECT * FROM customers", engine)
    return sales, products, customers

sales, products, customers = get_data()

# Merge for analysis
sales['revenue'] = sales['quantity'] * sales['price']
sales['sale_date'] = pd.to_datetime(sales['sale_date'])
merged = sales.merge(products, on='product_id').merge(customers, on='customer_id')

# ---------------------------
# Dashboard UI
# ---------------------------
st.title("🛍️ E-commerce Sales Analysis Dashboard")

# Top Products
st.header("Top 10 Products by Revenue")
top_products = merged.groupby('product_name')['revenue'].sum().nlargest(10)
st.bar_chart(top_products)

# Monthly Revenue Trend
st.header("Monthly Sales Trend")
monthly = merged.resample('M', on='sale_date')['revenue'].sum()
st.line_chart(monthly)

# Customer Segmentation
st.header("Customer Segmentation by CLV")
clv = merged.groupby('customer_id')['revenue'].sum()
top_clv = clv.sort_values(ascending=False)
top_15 = top_clv.head(int(len(clv) * 0.15))
percent_revenue = round(top_15.sum() / clv.sum() * 100, 2)
st.metric(label="Revenue from Top 15% Customers", value=f"{percent_revenue}%")

# Category Performance
st.header("Sales by Category")
category_rev = merged.groupby('category')['revenue'].sum().sort_values(ascending=False)
st.bar_chart(category_rev)

# Regional Trends
st.header("Sales by Region")
region_rev = merged.groupby('region')['revenue'].sum().sort_values(ascending=False)
st.bar_chart(region_rev)

# ---------------------------
# Optional Stockout Warning
# ---------------------------
st.header("Low Sales, High Stock (Potential Overstock)")
stock_issues = merged.groupby('product_name').agg({
    'revenue': 'sum',
    'stock_quantity': 'max'
}).query('revenue < 1000 and stock_quantity > 0').sort_values(by='stock_quantity', ascending=False)

st.dataframe(stock_issues.head(10))

