"""
Dashboard Page: Product Profitability
"""

import streamlit as st
import sys
from pathlib import Path

# Add root directory to path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from src.product_analysis import (
    get_product_summary,
    identify_high_profit_products,
    identify_high_margin_products,
    identify_high_sales_low_margin_products,
    identify_margin_risk_products
)
from dashboard.components.filters import render_sidebar_filters

st.set_page_config(page_title="Product Profitability | Nassau Candy", layout="wide")

st.title("📦 Product Profitability Leaderboard & Margin Performance")

# Render Filters & get Active Dataset
filtered_df = render_sidebar_filters()

if filtered_df.empty:
    st.warning("⚠️ No records match the current filter criteria.")
    st.stop()

prod_summary = get_product_summary(filtered_df)

tab1, tab2, tab3 = st.tabs(["Leaderboards", "Margin Risk & High Sales/Low Margin", "Full Product Data"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 5 Products by Gross Profit ($)")
        high_profit = identify_high_profit_products(prod_summary, 5)
        st.dataframe(high_profit[["Product Name", "Division", "Total_Sales", "Total_Profit", "Gross_Margin_Pct"]], use_container_width=True)

    with col2:
        st.subheader("Top 5 Products by Gross Margin (%)")
        high_margin = identify_high_margin_products(prod_summary, top_n=5)
        st.dataframe(high_margin[["Product Name", "Division", "Total_Sales", "Total_Profit", "Gross_Margin_Pct"]], use_container_width=True)

with tab2:
    st.subheader("⚠️ High Sales / Low Margin Products")
    st.caption("Products with above-median sales volume but below-median gross margin percentage.")
    high_sales_low_margin = identify_high_sales_low_margin_products(prod_summary)
    st.dataframe(high_sales_low_margin[["Product Name", "Division", "Total_Sales", "Total_Profit", "Gross_Margin_Pct"]], use_container_width=True)

    st.subheader("🚨 Margin Risk Products (< 20% Gross Margin)")
    margin_risk = identify_margin_risk_products(prod_summary, margin_cutoff_pct=20.0)
    st.dataframe(margin_risk[["Product Name", "Division", "Total_Sales", "Total_Profit", "Gross_Margin_Pct"]], use_container_width=True)

with tab3:
    st.subheader("Complete Product Financial Table")
    st.dataframe(prod_summary, use_container_width=True)

