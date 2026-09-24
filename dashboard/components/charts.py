"""
Reusable Plotly Chart Wrappers for Dashboard Integration with Theme Support.
"""

import plotly.express as px
import plotly.graph_objects as gg
import pandas as pd
from dashboard.components.theme import apply_plotly_theme


def render_monthly_financial_trend(df: pd.DataFrame):
    """
    Renders monthly sales and profit line chart.
    """
    df_monthly = df.set_index("Order Date").resample("ME").agg({
        "Sales": "sum",
        "Gross Profit": "sum"
    }).reset_index()

    fig = px.line(
        df_monthly,
        x="Order Date",
        y=["Sales", "Gross Profit"],
        title="Monthly Sales & Gross Profit Trend",
        labels={"value": "Amount ($)", "Order Date": "Month", "variable": "Metric"},
        color_discrete_map={"Sales": "#2563EB", "Gross Profit": "#10B981"}
    )
    return apply_plotly_theme(fig, title="Monthly Sales & Gross Profit Trend")


def render_division_bar_chart(df_div: pd.DataFrame):
    """
    Renders Division performance grouped bar chart.
    """
    fig = gg.Figure()
    fig.add_trace(gg.Bar(
        x=df_div["Division"],
        y=df_div["Total_Sales"],
        name="Total Sales ($)",
        marker_color="#3B82F6"
    ))
    fig.add_trace(gg.Bar(
        x=df_div["Division"],
        y=df_div["Total_Profit"],
        name="Gross Profit ($)",
        marker_color="#10B981"
    ))
    fig.update_layout(
        barmode="group",
        xaxis_title="Division",
        yaxis_title="Amount ($)"
    )
    return apply_plotly_theme(fig, title="Revenue & Gross Profit by Division")


def render_product_deep_dive_charts(df_product: pd.DataFrame, product_name: str):
    """
    Generates time-series line chart and regional breakdown for a single selected product.
    """
    # 1. Monthly trend chart
    df_product_monthly = df_product.set_index("Order Date").resample("ME").agg({
        "Sales": "sum",
        "Gross Profit": "sum"
    }).reset_index()

    fig_trend = px.line(
        df_product_monthly,
        x="Order Date",
        y=["Sales", "Gross Profit"],
        title=f"📈 Monthly Performance Trend for {product_name}",
        labels={"value": "Amount ($)", "Order Date": "Month", "variable": "Metric"},
        color_discrete_map={"Sales": "#2563EB", "Gross Profit": "#10B981"}
    )
    apply_plotly_theme(fig_trend, title=f"📈 Monthly Performance Trend for {product_name}")

    # 2. Regional Breakdown
    reg_summary = df_product.groupby("Region").agg({
        "Sales": "sum",
        "Gross Profit": "sum"
    }).reset_index()

    fig_reg = px.bar(
        reg_summary,
        x="Region",
        y=["Sales", "Gross Profit"],
        barmode="group",
        title=f"🗺️ Regional Sales & Profit for {product_name}",
        labels={"value": "Amount ($)"},
        color_discrete_map={"Sales": "#3B82F6", "Gross Profit": "#10B981"}
    )
    apply_plotly_theme(fig_reg, title=f"🗺️ Regional Sales & Profit for {product_name}")

    return fig_trend, fig_reg


