"""
Reusable Interactive Sidebar Filters & Global Settings Component for Streamlit Dashboard.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from src.data_loader import (
    load_uploaded_dataset,
    get_active_dataset,
    set_active_dataset,
    load_cleaned_data,
    DEFAULT_PROCESSED_PATH
)
from dashboard.components.theme import render_top_appearance_selector, apply_theme


def render_sidebar_filters(df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Renders sidebar controls:
    1. Top Appearance Selector (☀️ Light | 🌙 Dark)
    2. Navigation & Dataset Upload
    3. Analytics Filters (Date Range, Division, Region, Product Search & Margin Slider)
    Returns filtered DataFrame.
    """
    # 1. TOP APPEARANCE SELECTOR
    render_top_appearance_selector()
    apply_theme()

    # 2. File Uploader Section
    st.sidebar.subheader("📁 Dataset Management")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Custom Data (.csv, .xlsx)",
        type=["csv", "xlsx", "xls"],
        help="Upload your own profitability sales records dataset"
    )

    if uploaded_file is not None:
        try:
            custom_df = load_uploaded_dataset(uploaded_file)
            set_active_dataset(custom_df, dataset_name=f"Uploaded: {uploaded_file.name}")
            st.sidebar.success(f"Loaded {len(custom_df):,} records!")
        except Exception as e:
            st.sidebar.error(f"Error reading uploaded file: {e}")

    # Dataset status indicator & Reset Button
    active_dataset_name = st.session_state.get("dataset_name", "Nassau Candy Default")
    st.sidebar.caption(f"📊 **Active Dataset**: `{active_dataset_name}`")
    
    if st.sidebar.button("↺ Reset to Default Dataset"):
        default_df = load_cleaned_data(DEFAULT_PROCESSED_PATH)
        set_active_dataset(default_df, "Nassau Candy Default (2,500 records)")
        st.rerun()

    st.sidebar.markdown("---")

    # Retrieve current active DataFrame
    active_df = get_active_dataset() if df is None else df

    st.sidebar.subheader("🔍 Filter Analytics")

    # 3. Safe Date Picker Handling
    filtered_df = active_df.copy()

    if "Order Date" in filtered_df.columns and not filtered_df["Order Date"].dropna().empty:
        min_date = filtered_df["Order Date"].min().date()
        max_date = filtered_df["Order Date"].max().date()

        date_result = st.sidebar.date_input(
            "Order Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        # Handle tuple of 1, 2, or single date output safely to prevent unpack errors
        if isinstance(date_result, (tuple, list)):
            if len(date_result) == 2:
                start_date, end_date = date_result
            elif len(date_result) == 1:
                start_date = end_date = date_result[0]
            else:
                start_date, end_date = min_date, max_date
        else:
            start_date = end_date = date_result

        filtered_df = filtered_df[
            (filtered_df["Order Date"].dt.date >= start_date) &
            (filtered_df["Order Date"].dt.date <= end_date)
        ]

    # 4. Division Filter
    if "Division" in filtered_df.columns:
        divisions = ["All"] + sorted([str(x) for x in filtered_df["Division"].dropna().unique().tolist()])
        selected_div = st.sidebar.selectbox("Division", options=divisions, index=0)
        if selected_div != "All":
            filtered_df = filtered_df[filtered_df["Division"] == selected_div]

    # 5. Region Filter
    if "Region" in filtered_df.columns:
        regions = ["All"] + sorted([str(x) for x in filtered_df["Region"].dropna().unique().tolist()])
        selected_region = st.sidebar.selectbox("Region", options=regions, index=0)
        if selected_region != "All":
            filtered_df = filtered_df[filtered_df["Region"] == selected_region]

    # 6. Specific Product Selectbox / Search
    if "Product Name" in filtered_df.columns:
        product_list = ["All Products"] + sorted(filtered_df["Product Name"].dropna().unique().tolist())
        selected_product = st.sidebar.selectbox("Select Specific Product", options=product_list, index=0)
        if selected_product != "All Products":
            filtered_df = filtered_df[filtered_df["Product Name"] == selected_product]

        # Text Search box as extra refinement
        product_search = st.sidebar.text_input("Product Search (Text)", value="").strip()
        if product_search:
            filtered_df = filtered_df[filtered_df["Product Name"].str.contains(product_search, case=False, na=False)]

    # 7. Minimum Gross Margin Slider
    if "Gross Margin %" in filtered_df.columns:
        min_margin = st.sidebar.slider("Min Gross Margin %", min_value=-50, max_value=100, value=-50, step=5)
        filtered_df = filtered_df[filtered_df["Gross Margin %"] >= min_margin]

    return filtered_df


