"""
Reusable KPI Summary Cards Component for Streamlit Dashboard.
"""

import streamlit as st


def format_smart_currency(val: float) -> str:
    """
    Formats currency values cleanly to fit KPI cards without truncation.
    """
    if abs(val) >= 1_000_000:
        return f"${val / 1_000_000:,.2f}M"
    elif abs(val) >= 100_000:
        return f"${val / 1_000:,.1f}K"
    else:
        return f"${val:,.2f}"


def render_kpi_cards(total_sales: float, total_cost: float, total_profit: float, gross_margin_pct: float, total_units: int, product_count: int):
    """
    Renders 6 styled KPI cards in a 6-column layout with smart formatting.
    """
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric(label="Total Revenue", value=format_smart_currency(total_sales))
    with col2:
        st.metric(label="Total Cost", value=format_smart_currency(total_cost))
    with col3:
        st.metric(label="Gross Profit", value=format_smart_currency(total_profit))
    with col4:
        st.metric(label="Gross Margin %", value=f"{gross_margin_pct:.2f}%")
    with col5:
        st.metric(label="Total Units", value=f"{total_units:,}")
    with col6:
        st.metric(label="Product Count", value=f"{product_count:,}")

