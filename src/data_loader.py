"""
Data Loading Module for Nassau Candy Distributor Profitability Analysis.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st

DEFAULT_RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "nassau_candy.csv"
DEFAULT_PROCESSED_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "cleaned_nassau_candy.csv"


def load_raw_data(file_path: Path | str = DEFAULT_RAW_PATH) -> pd.DataFrame:
    """
    Loads raw CSV dataset into a pandas DataFrame.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found at: {path}")
    df = pd.read_csv(path)
    return df


def load_cleaned_data(file_path: Path | str = DEFAULT_PROCESSED_PATH) -> pd.DataFrame:
    """
    Loads processed/cleaned CSV dataset into a pandas DataFrame.
    Ensures datetime columns are properly parsed.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Cleaned data file not found at: {path}")
    df = pd.read_csv(path)
    return prepare_dataframe(df)


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes column names, parses dates, fills missing fields, and calculates metrics.
    Works for both default datasets and user-uploaded datasets.
    """
    cleaned = df.copy()
    cleaned.columns = [str(col).strip() for col in cleaned.columns]

    # Flexible column mapping dictionary
    column_mapping = {
        "product": "Product Name",
        "product_name": "Product Name",
        "item": "Product Name",
        "item_name": "Product Name",
        "sales_amount": "Sales",
        "revenue": "Sales",
        "cost_amount": "Cost",
        "cogs": "Cost",
        "profit": "Gross Profit",
        "gross_profit": "Gross Profit",
        "qty": "Units",
        "quantity": "Units",
        "units_sold": "Units",
        "order_date": "Order Date",
        "date": "Order Date",
        "ship_date": "Ship Date",
        "div": "Division",
        "category": "Division",
        "state": "State/Province",
        "country": "Country/Region"
    }

    # Rename lower-cased matches
    rename_dict = {}
    for col in cleaned.columns:
        col_lower = col.lower().replace(" ", "_")
        if col_lower in column_mapping and col not in column_mapping.values():
            rename_dict[col] = column_mapping[col_lower]
    if rename_dict:
        cleaned = cleaned.rename(columns=rename_dict)

    # Standardize essential text fields
    if "Product Name" not in cleaned.columns:
        # Fallback if no product column found
        possible_text = [c for c in cleaned.columns if cleaned[c].dtype == "object"]
        cleaned["Product Name"] = cleaned[possible_text[0]] if possible_text else "Generic Product"

    if "Division" not in cleaned.columns:
        cleaned["Division"] = "General"

    if "Region" not in cleaned.columns:
        cleaned["Region"] = "All Regions"

    if "Units" not in cleaned.columns:
        cleaned["Units"] = 1

    # Date parsing
    date_cols = [c for c in ["Order Date", "Ship Date", "Date"] if c in cleaned.columns]
    if not date_cols and any("date" in c.lower() for c in cleaned.columns):
        date_cols = [c for c in cleaned.columns if "date" in c.lower()]
        cleaned["Order Date"] = pd.to_datetime(cleaned[date_cols[0]], errors="coerce")
    else:
        for col in date_cols:
            cleaned[col] = pd.to_datetime(cleaned[col], errors="coerce")
        if "Order Date" not in cleaned.columns and date_cols:
            cleaned["Order Date"] = cleaned[date_cols[0]]

    # If still no Order Date, generate synthetic dates for time-series visualization
    if "Order Date" not in cleaned.columns or cleaned["Order Date"].isnull().all():
        cleaned["Order Date"] = pd.date_range(start="2024-01-01", periods=len(cleaned), freq="D")

    # Numeric conversions & financial metric calculations
    for num_col in ["Sales", "Cost", "Gross Profit", "Units"]:
        if num_col in cleaned.columns:
            cleaned[num_col] = pd.to_numeric(cleaned[num_col], errors="coerce").fillna(0.0)

    if "Sales" not in cleaned.columns and "Cost" in cleaned.columns and "Gross Profit" in cleaned.columns:
        cleaned["Sales"] = cleaned["Cost"] + cleaned["Gross Profit"]
    elif "Cost" not in cleaned.columns and "Sales" in cleaned.columns and "Gross Profit" in cleaned.columns:
        cleaned["Cost"] = cleaned["Sales"] - cleaned["Gross Profit"]
    elif "Gross Profit" not in cleaned.columns and "Sales" in cleaned.columns and "Cost" in cleaned.columns:
        cleaned["Gross Profit"] = cleaned["Sales"] - cleaned["Cost"]
    elif "Sales" not in cleaned.columns:
        cleaned["Sales"] = 0.0
        cleaned["Cost"] = 0.0
        cleaned["Gross Profit"] = 0.0

    # Recalculate Gross Margin %
    cleaned["Gross Margin %"] = np.where(
        cleaned["Sales"] > 0,
        (cleaned["Gross Profit"] / cleaned["Sales"]) * 100,
        0.0
    )
    cleaned["Gross Margin %"] = np.round(cleaned["Gross Margin %"], 2)

    return cleaned


def load_uploaded_dataset(file_buffer) -> pd.DataFrame:
    """
    Reads user uploaded CSV or Excel file into a standardized pandas DataFrame.
    """
    filename = getattr(file_buffer, "name", "").lower()
    if filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file_buffer)
    else:
        df = pd.read_csv(file_buffer)
    return prepare_dataframe(df)


def get_active_dataset() -> pd.DataFrame:
    """
    Retrieves active dataset from Streamlit session state or loads default processed dataset.
    """
    if "active_df" in st.session_state and isinstance(st.session_state["active_df"], pd.DataFrame):
        return st.session_state["active_df"]
    
    # Load default processed dataset
    df = load_cleaned_data(DEFAULT_PROCESSED_PATH)
    st.session_state["active_df"] = df
    st.session_state["dataset_name"] = "Nassau Candy Default (2,500 records)"
    return df


def set_active_dataset(df: pd.DataFrame, dataset_name: str = "Uploaded Dataset"):
    """
    Sets active dataset in Streamlit session state.
    """
    st.session_state["active_df"] = df
    st.session_state["dataset_name"] = dataset_name


def inspect_dataset_summary(df: pd.DataFrame) -> dict:
    """
    Returns a comprehensive structural summary of the dataset.
    """
    summary = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "columns": df.columns.tolist(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": df.duplicated().sum(),
        "numeric_summary": df.describe().to_dict(),
        "unique_counts": df.nunique().to_dict()
    }
    return summary

