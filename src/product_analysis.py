"""
Product Performance and Profitability Analysis Module.
"""

import pandas as pd
import numpy as np
from src.metrics import calculate_contributions


def get_product_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates product-level aggregation of key financial and operational metrics.
    """
    prod_metrics = calculate_contributions(df, group_col="Product Name")
    
    # Merge division mapping
    div_map = df.groupby("Product Name")["Division"].first().reset_index()
    prod_metrics = prod_metrics.merge(div_map, on="Product Name", how="left")
    
    # Reorder columns
    cols = [
        "Product Name", "Division", "Total_Sales", "Total_Cost", "Total_Profit",
        "Gross_Margin_Pct", "Total_Units", "Profit_per_Unit",
        "Revenue_Contribution_Pct", "Profit_Contribution_Pct", "Order_Count"
    ]
    return prod_metrics[cols].sort_values(by="Total_Profit", ascending=False)


def identify_high_profit_products(df_prod: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Returns top N products by total gross profit.
    """
    return df_prod.sort_values(by="Total_Profit", ascending=False).head(top_n)


def identify_high_margin_products(df_prod: pd.DataFrame, min_sales: float = 1000.0, top_n: int = 5) -> pd.DataFrame:
    """
    Returns top N products by gross margin % amongst products with meaningful sales volume.
    """
    filtered = df_prod[df_prod["Total_Sales"] >= min_sales]
    if filtered.empty:
        filtered = df_prod
    return filtered.sort_values(by="Gross_Margin_Pct", ascending=False).head(top_n)


def identify_high_sales_low_margin_products(
    df_prod: pd.DataFrame,
    sales_quantile: float = 0.5,
    margin_quantile: float = 0.5
) -> pd.DataFrame:
    """
    Identifies products with above-median sales volume but below-median gross margin percentage.
    """
    sales_threshold = df_prod["Total_Sales"].quantile(sales_quantile)
    margin_threshold = df_prod["Gross_Margin_Pct"].quantile(margin_quantile)

    risk_products = df_prod[
        (df_prod["Total_Sales"] >= sales_threshold) & 
        (df_prod["Gross_Margin_Pct"] <= margin_threshold)
    ].copy()
    
    risk_products["Sales_Threshold"] = sales_threshold
    risk_products["Margin_Threshold"] = margin_threshold
    return risk_products.sort_values(by="Total_Sales", ascending=False)


def identify_margin_risk_products(df_prod: pd.DataFrame, margin_cutoff_pct: float = 20.0) -> pd.DataFrame:
    """
    Identifies products with gross margin below a specific risk cutoff percentage.
    """
    risk_df = df_prod[df_prod["Gross_Margin_Pct"] < margin_cutoff_pct].copy()
    return risk_df.sort_values(by="Gross_Margin_Pct", ascending=True)
