"""
Unit tests for src/metrics.py
"""

import pytest
import pandas as pd
import numpy as np
from src.metrics import (
    calculate_gross_margin_pct,
    calculate_profit_per_unit,
    calculate_contributions,
    calculate_margin_volatility
)


def test_calculate_gross_margin_pct_scalar():
    assert calculate_gross_margin_pct(20.0, 100.0) == 20.0
    assert calculate_gross_margin_pct(10.0, 0.0) == 0.0
    assert calculate_gross_margin_pct(0.0, 100.0) == 0.0


def test_calculate_gross_margin_pct_series():
    profit = pd.Series([20.0, 50.0, 0.0])
    sales = pd.Series([100.0, 200.0, 0.0])
    margin = calculate_gross_margin_pct(profit, sales)
    assert margin.iloc[0] == 20.0
    assert margin.iloc[1] == 25.0
    assert margin.iloc[2] == 0.0


def test_calculate_profit_per_unit():
    assert calculate_profit_per_unit(50.0, 10) == 5.0
    assert calculate_profit_per_unit(50.0, 0) == 0.0


def test_calculate_contributions():
    data = {
        "Product Name": ["Product A", "Product B"],
        "Sales": [100.0, 300.0],
        "Cost": [60.0, 150.0],
        "Gross Profit": [40.0, 150.0],
        "Units": [10, 30],
        "Order ID": ["O1", "O2"]
    }
    df = pd.DataFrame(data)
    contrib = calculate_contributions(df, "Product Name")

    assert "Revenue_Contribution_Pct" in contrib.columns
    assert "Profit_Contribution_Pct" in contrib.columns

    prod_a = contrib[contrib["Product Name"] == "Product A"].iloc[0]
    assert pytest.approx(prod_a["Revenue_Contribution_Pct"]) == 25.0
    assert pytest.approx(prod_a["Profit_Contribution_Pct"]) == 21.0526315
