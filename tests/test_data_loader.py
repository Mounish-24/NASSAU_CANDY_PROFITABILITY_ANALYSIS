"""
Unit tests for src/data_loader.py
"""

import pytest
import pandas as pd
from pathlib import Path
from src.data_loader import load_raw_data, load_cleaned_data, inspect_dataset_summary


def test_load_raw_data():
    raw_path = Path(__file__).resolve().parent.parent / "data" / "raw" / "nassau_candy.csv"
    df = load_raw_data(raw_path)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "Sales" in df.columns
    assert "Gross Profit" in df.columns


def test_load_raw_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_raw_data("non_existent_file.csv")


def test_inspect_dataset_summary():
    raw_path = Path(__file__).resolve().parent.parent / "data" / "raw" / "nassau_candy.csv"
    df = load_raw_data(raw_path)
    summary = inspect_dataset_summary(df)
    assert summary["num_rows"] > 0
    assert summary["num_columns"] > 0
    assert "Sales" in summary["columns"]
