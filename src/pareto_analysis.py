"""
Pareto (80/20 Rule) Concentration Analysis Module.
"""

import pandas as pd
import numpy as np


def calculate_revenue_pareto(df: pd.DataFrame, group_col: str = "Product Name") -> pd.DataFrame:
    """
    Calculates cumulative revenue contribution % by product and identifies 80% cutoff.
    """
    grouped = df.groupby(group_col)["Sales"].sum().reset_index()
    grouped = grouped.sort_values(by="Sales", ascending=False).reset_index(drop=True)
    
    total_sales = grouped["Sales"].sum()
    grouped["Revenue_Pct"] = np.where(total_sales > 0, (grouped["Sales"] / total_sales) * 100, 0.0)
    grouped["Cumulative_Revenue_Pct"] = grouped["Revenue_Pct"].cumsum()
    grouped["Rank"] = grouped.index + 1
    grouped["Product_Share_Pct"] = (grouped["Rank"] / len(grouped)) * 100
    grouped["In_Top_80_Pct_Revenue"] = grouped["Cumulative_Revenue_Pct"] <= 80.0
    
    # Include boundary product that crosses 80%
    boundary_idx = grouped[grouped["Cumulative_Revenue_Pct"] >= 80.0].index.min()
    if pd.notna(boundary_idx):
        grouped.loc[:boundary_idx, "In_Top_80_Pct_Revenue"] = True

    return grouped


def calculate_profit_pareto(df: pd.DataFrame, group_col: str = "Product Name") -> pd.DataFrame:
    """
    Calculates cumulative gross profit contribution % by product and identifies 80% cutoff.
    """
    grouped = df.groupby(group_col)["Gross Profit"].sum().reset_index()
    grouped = grouped.sort_values(by="Gross Profit", ascending=False).reset_index(drop=True)
    
    total_profit = grouped["Gross Profit"].sum()
    grouped["Profit_Pct"] = np.where(total_profit > 0, (grouped["Gross Profit"] / total_profit) * 100, 0.0)
    grouped["Cumulative_Profit_Pct"] = grouped["Profit_Pct"].cumsum()
    grouped["Rank"] = grouped.index + 1
    grouped["Product_Share_Pct"] = (grouped["Rank"] / len(grouped)) * 100
    grouped["In_Top_80_Pct_Profit"] = grouped["Cumulative_Profit_Pct"] <= 80.0
    
    # Include boundary product that crosses 80%
    boundary_idx = grouped[grouped["Cumulative_Profit_Pct"] >= 80.0].index.min()
    if pd.notna(boundary_idx):
        grouped.loc[:boundary_idx, "In_Top_80_Pct_Profit"] = True

    return grouped


def summarize_pareto_concentration(df: pd.DataFrame) -> dict:
    """
    Provides summary metrics of Pareto concentration for both Revenue and Profit.
    """
    rev_pareto = calculate_revenue_pareto(df)
    prof_pareto = calculate_profit_pareto(df)

    total_products = len(df["Product Name"].unique())
    rev_top_80_count = int(rev_pareto["In_Top_80_Pct_Revenue"].sum())
    prof_top_80_count = int(prof_pareto["In_Top_80_Pct_Profit"].sum())

    summary = {
        "total_products": total_products,
        "revenue_top_80_product_count": rev_top_80_count,
        "revenue_top_80_product_share_pct": round((rev_top_80_count / total_products) * 100, 2),
        "profit_top_80_product_count": prof_top_80_count,
        "profit_top_80_product_share_pct": round((prof_top_80_count / total_products) * 100, 2)
    }
    return summary
