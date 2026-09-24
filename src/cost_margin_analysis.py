"""
Cost and Margin Structure Analysis Module.
"""

import pandas as pd
import numpy as np


def analyze_cost_structure(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes total sales, cost, profit, and cost ratio (Cost / Sales) at product level.
    """
    prod_cost = df.groupby("Product Name").agg(
        Total_Sales=("Sales", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum"),
        Division=("Division", "first")
    ).reset_index()

    prod_cost["Cost_Ratio_Pct"] = np.where(
        prod_cost["Total_Sales"] > 0, (prod_cost["Total_Cost"] / prod_cost["Total_Sales"]) * 100, 0.0
    )
    prod_cost["Gross_Margin_Pct"] = np.where(
        prod_cost["Total_Sales"] > 0, (prod_cost["Total_Profit"] / prod_cost["Total_Sales"]) * 100, 0.0
    )
    prod_cost["Unit_Cost"] = np.where(
        prod_cost["Total_Units"] > 0, prod_cost["Total_Cost"] / prod_cost["Total_Units"], 0.0
    )
    prod_cost["Unit_Price"] = np.where(
        prod_cost["Total_Units"] > 0, prod_cost["Total_Sales"] / prod_cost["Total_Units"], 0.0
    )

    return prod_cost.sort_values(by="Cost_Ratio_Pct", ascending=False)


def identify_high_cost_products(df_prod_cost: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """
    Returns products with highest cost ratios or highest absolute total cost.
    """
    return df_prod_cost.sort_values(by="Total_Cost", ascending=False).head(top_n)
