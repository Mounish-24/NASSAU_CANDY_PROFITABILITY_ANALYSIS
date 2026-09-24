"""
Unit tests for src/data_cleaning.py
"""

import pytest
import pandas as pd
from pathlib import Path
from src.data_loader import load_raw_data
from src.data_cleaning import clean_and_validate_data, REQUIRED_COLUMNS


def test_clean_and_validate_data():
    raw_path = Path(__file__).resolve().parent.parent / "data" / "raw" / "nassau_candy.csv"
    df_raw = load_raw_data(raw_path)
    df_cleaned = clean_and_validate_data(df_raw)

    assert isinstance(df_cleaned, pd.DataFrame)
    assert not df_cleaned.empty
    
    # Financial logic check
    profit_diff = (df_cleaned["Sales"] - df_cleaned["Cost"]) - df_cleaned["Gross Profit"]
    assert profit_diff.abs().max() < 0.05
    
    # Check calculated columns exist
    assert "Gross Margin %" in df_cleaned.columns
    assert "Profit per Unit" in df_cleaned.columns


def test_clean_missing_columns():
    invalid_df = pd.DataFrame({"Sales": [100], "Cost": [50]})
    with pytest.raises(KeyError):
        clean_and_validate_data(invalid_df)
