"""
Business Metrics and Financial KPI Calculation Module for Nassau Candy Distributor.
"""

import pandas as pd
import numpy as np


def calculate_gross_margin_pct(profit: float | pd.Series, sales: float | pd.Series) -> float | pd.Series:
    """
    Calculates Gross Margin Percentage safely.
    Gross Margin % = (Gross Profit / Sales) * 100
    """
    if isinstance(sales, (int, float)):
        if sales == 0 or pd.isna(sales):
            return 0.0
        return float((profit / sales) * 100)
    
    # Pandas Series implementation
    margin = np.where(sales > 0, (profit / sales) * 100, 0.0)
    return pd.Series(margin, index=sales.index)


def calculate_profit_per_unit(profit: float | pd.Series, units: int | float | pd.Series) -> float | pd.Series:
    """
    Calculates Profit per Unit safely.
    Profit per Unit = Gross Profit / Units
    """
    if isinstance(units, (int, float)):
        if units == 0 or pd.isna(units):
            return 0.0
        return float(profit / units)
    
    ppu = np.where(units > 0, profit / units, 0.0)
    return pd.Series(ppu, index=units.index)


def calculate_contributions(df: pd.DataFrame, group_col: str = "Product Name") -> pd.DataFrame:
    """
    Calculates Revenue Contribution % and Profit Contribution % grouped by a given column.
    """
    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()

    grouped = df.groupby(group_col).agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Units=("Units", "sum"),
        Order_Count=("Order ID", "nunique")
    ).reset_index()

    grouped["Revenue_Contribution_Pct"] = np.where(
        total_sales > 0, (grouped["Total_Sales"] / total_sales) * 100, 0.0
    )
    grouped["Profit_Contribution_Pct"] = np.where(
        total_profit > 0, (grouped["Total_Profit"] / total_profit) * 100, 0.0
    )
    grouped["Gross_Margin_Pct"] = calculate_gross_margin_pct(
        grouped["Total_Profit"], grouped["Total_Sales"]
    )
    grouped["Profit_per_Unit"] = calculate_profit_per_unit(
        grouped["Total_Profit"], grouped["Total_Units"]
    )

    return grouped


def calculate_margin_volatility(df: pd.DataFrame, product_col: str = "Product Name", date_col: str = "Order Date") -> pd.DataFrame:
    """
    Measures Gross Margin % standard deviation over time at the product level.
    """
    df_temp = df.copy()
    df_temp["Margin_%"] = calculate_gross_margin_pct(df_temp["Gross Profit"], df_temp["Sales"])
    
    volatility = df_temp.groupby(product_col).agg(
        Margin_Std=("Margin_%", "std"),
        Margin_Mean=("Margin_%", "mean"),
        Transaction_Count=("Order ID", "count")
    ).reset_index()
    
    volatility["Margin_Std"] = volatility["Margin_Std"].fillna(0.0)
    return volatility
