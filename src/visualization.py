"""
Data Visualization Helper Module using Plotly with Centralized Dynamic Theme Support.
"""

import plotly.express as px
import plotly.graph_objects as gg
import pandas as pd
from dashboard.components.theme import apply_plotly_theme


def plot_revenue_and_profit_by_division(df_div: pd.DataFrame):
    """
    Creates an interactive grouped bar chart showing Revenue vs Gross Profit by Division.
    """
    fig = gg.Figure()
    fig.add_trace(gg.Bar(
        x=df_div["Division"],
        y=df_div["Total_Sales"],
        name="Total Revenue ($)",
        marker_color="#2563EB"
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
        yaxis_title="Amount ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return apply_plotly_theme(fig, title="Revenue vs Gross Profit by Division")


def plot_cost_vs_sales_scatter(df_prod: pd.DataFrame):
    """
    Creates an interactive scatter plot of Sales vs Cost colored by Division.
    """
    fig = px.scatter(
        df_prod,
        x="Total_Sales",
        y="Total_Cost",
        size="Total_Profit",
        color="Division",
        hover_name="Product Name",
        hover_data=["Gross_Margin_Pct", "Total_Units"],
        title="Product Sales vs. Cost Structure (Bubble size = Gross Profit)",
        labels={"Total_Sales": "Total Sales ($)", "Total_Cost": "Total Cost ($)"}
    )
    return apply_plotly_theme(fig, title="Product Sales vs. Cost Structure (Bubble size = Gross Profit)")


def plot_pareto_chart(df_pareto: pd.DataFrame, metric: str = "Profit"):
    """
    Creates a Pareto chart with dual axis: Bar for metric and Line for cumulative %.
    """
    col_val = "Gross Profit" if metric == "Profit" else "Sales"
    col_cum = "Cumulative_Profit_Pct" if metric == "Profit" else "Cumulative_Revenue_Pct"

    fig = gg.Figure()

    fig.add_trace(gg.Bar(
        x=df_pareto["Product Name"],
        y=df_pareto[col_val],
        name=f"Total {metric} ($)",
        marker_color="#3B82F6",
        yaxis="y"
    ))

    fig.add_trace(gg.Scatter(
        x=df_pareto["Product Name"],
        y=df_pareto[col_cum],
        name=f"Cumulative {metric} %",
        marker_color="#EF4444",
        mode="lines+markers",
        yaxis="y2"
    ))

    fig.update_layout(
        xaxis=dict(title="Product Name", tickangle=-45),
        yaxis=dict(title=f"Total {metric} ($)", side="left"),
        yaxis2=dict(title="Cumulative Contribution (%)", overlaying="y", side="right", range=[0, 105]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return apply_plotly_theme(fig, title=f"Pareto Analysis - Product {metric} Concentration")

