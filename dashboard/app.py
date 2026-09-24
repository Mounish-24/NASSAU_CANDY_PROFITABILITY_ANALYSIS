"""
Main Executive Streamlit Dashboard Application for Nassau Candy Distributor.
"""

import streamlit as st
import sys
from pathlib import Path

# Add root directory to path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from src.data_loader import get_active_dataset
from src.division_analysis import get_division_summary
from src.product_analysis import get_product_summary
from dashboard.components.kpi_cards import render_kpi_cards
from dashboard.components.charts import (
    render_monthly_financial_trend,
    render_division_bar_chart,
    render_product_deep_dive_charts
)
from dashboard.components.filters import render_sidebar_filters

st.set_page_config(
    page_title="Nassau Candy Profitability Analysis",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.markdown('<div class="main-header">🍬 Nassau Candy Distributor — Profitability & Margin Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Executive Business Intelligence, Data File Upload & Product Search Analytics</div>', unsafe_allow_html=True)

# Render Global Filters & File Upload
filtered_df = render_sidebar_filters()

if filtered_df.empty:
    st.warning("⚠️ No records match the selected dataset filter combination. Try resetting filters in the sidebar.")
    st.stop()

# Aggregate Key Overview Metrics
total_sales = float(filtered_df["Sales"].sum())
total_cost = float(filtered_df["Cost"].sum())
total_profit = float(filtered_df["Gross Profit"].sum())
overall_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0
total_units = int(filtered_df["Units"].sum()) if "Units" in filtered_df.columns else 0
product_count = int(filtered_df["Product Name"].nunique()) if "Product Name" in filtered_df.columns else 0

# Render Executive KPI Cards
st.subheader("📌 Key Financial Overview")
render_kpi_cards(
    total_sales=total_sales,
    total_cost=total_cost,
    total_profit=total_profit,
    gross_margin_pct=overall_margin,
    total_units=total_units,
    product_count=product_count
)

st.markdown("---")

# Main Dashboard Navigation Tabs
tab_overview, tab_product_search = st.tabs(["📊 Executive Overview", "🔎 Individual Product Search & Analysis"])

with tab_overview:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(render_monthly_financial_trend(filtered_df), use_container_width=True)

    with col2:
        if "Division" in filtered_df.columns and filtered_df["Division"].nunique() > 0:
            div_summary = get_division_summary(filtered_df)
            st.plotly_chart(render_division_bar_chart(div_summary), use_container_width=True)
        else:
            st.info("No division hierarchy found in uploaded dataset.")

    st.markdown("---")

    # Quick Insights Summary
    st.subheader("💡 Business Intelligence Summary")
    prod_summary = get_product_summary(filtered_df)
    if not prod_summary.empty:
        top_product = prod_summary.iloc[0]["Product Name"]
        top_product_profit = prod_summary.iloc[0]["Total_Profit"]
        st.info(f"""
        - **Top Profit Generator**: `{top_product}` generated **${top_product_profit:,.2f}** in gross profit.
        - **Overall Gross Margin**: The business operates at an overall gross margin of **{overall_margin:.2f}%**.
        - **Active Dataset**: Analyzing `{product_count}` distinct products across `{len(filtered_df):,}` order transactions.
        - **Theme & Upload**: Use the sidebar to upload custom data (`.csv` or `.xlsx`) and switch between **Light Mode** and **Dark Mode**.
        """)

with tab_product_search:
    st.subheader("🔎 Individual Product Detail Search & Deep Dive")
    st.caption("Search and select any product from the active dataset to inspect detailed financial metrics, margin trends, and order history.")

    all_products = sorted(filtered_df["Product Name"].dropna().unique().tolist()) if "Product Name" in filtered_df.columns else []

    if not all_products:
        st.warning("No products found in current filtered dataset.")
    else:
        selected_prod = st.selectbox("Select Product to Inspect:", options=all_products, index=0)
        df_single_prod = filtered_df[filtered_df["Product Name"] == selected_prod]

        prod_sales = float(df_single_prod["Sales"].sum())
        prod_cost = float(df_single_prod["Cost"].sum())
        prod_profit = float(df_single_prod["Gross Profit"].sum())
        prod_margin = (prod_profit / prod_sales * 100) if prod_sales > 0 else 0.0
        prod_units = int(df_single_prod["Units"].sum()) if "Units" in df_single_prod.columns else 0
        prod_orders = len(df_single_prod)

        # Single product metrics
        pcol1, pcol2, pcol3, pcol4, pcol5 = st.columns(5)
        pcol1.metric("Product Revenue", f"${prod_sales:,.2f}")
        pcol2.metric("Product Cost", f"${prod_cost:,.2f}")
        pcol3.metric("Gross Profit", f"${prod_profit:,.2f}")
        pcol4.metric("Gross Margin %", f"{prod_margin:.2f}%")
        pcol5.metric("Total Units / Orders", f"{prod_units:,} u / {prod_orders} ord")

        st.markdown("---")

        # Charts for selected product
        fig_prod_trend, fig_prod_reg = render_product_deep_dive_charts(df_single_prod, selected_prod)
        cc1, cc2 = st.columns(2)
        with cc1:
            st.plotly_chart(fig_prod_trend, use_container_width=True)
        with cc2:
            st.plotly_chart(fig_prod_reg, use_container_width=True)

        st.subheader(f"📋 Transaction Records for {selected_prod}")
        cols_to_show = [c for c in ["Order ID", "Order Date", "Division", "Region", "Sales", "Cost", "Gross Profit", "Gross Margin %", "Units"] if c in df_single_prod.columns]
        st.dataframe(df_single_prod[cols_to_show], use_container_width=True)

