"""
Division Performance and Profitability Analysis Module.
"""

import pandas as pd
import numpy as np
from src.metrics import calculate_contributions, calculate_gross_margin_pct


def get_division_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates division-level financial metrics and product count breakdown.
    """
    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()

    div_summary = df.groupby("Division").agg(
        Total_Sales=("Sales", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum"),
        Product_Count=("Product Name", "nunique"),
        Order_Count=("Order ID", "nunique")
    ).reset_index()

    div_summary["Gross_Margin_Pct"] = calculate_gross_margin_pct(
        div_summary["Total_Profit"], div_summary["Total_Sales"]
    )
    div_summary["Revenue_Contribution_Pct"] = np.where(
        total_sales > 0, (div_summary["Total_Sales"] / total_sales) * 100, 0.0
    )
    div_summary["Profit_Contribution_Pct"] = np.where(
        total_profit > 0, (div_summary["Total_Profit"] / total_profit) * 100, 0.0
    )
    div_summary["Avg_Profit_per_Order"] = np.where(
        div_summary["Order_Count"] > 0, div_summary["Total_Profit"] / div_summary["Order_Count"], 0.0
    )

    return div_summary.sort_values(by="Total_Profit", ascending=False)


def compare_division_margins(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates statistical margin distribution metrics (mean, median, std, min, max) for each division.
    """
    df_temp = df.copy()
    df_temp["Margin_%"] = calculate_gross_margin_pct(df_temp["Gross Profit"], df_temp["Sales"])

    stats = df_temp.groupby("Division")["Margin_%"].agg(
        Mean_Margin="mean",
        Median_Margin="median",
        Std_Margin="std",
        Min_Margin="min",
        Max_Margin="max"
    ).reset_index()

    return stats
