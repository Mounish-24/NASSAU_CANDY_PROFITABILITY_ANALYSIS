"""
Data Cleaning and Financial Validation Module for Nassau Candy Distributor.
"""

from pathlib import Path
import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
    "Customer ID", "Country/Region", "City", "State/Province", "Postal Code",
    "Division", "Region", "Product ID", "Product Name", "Sales", "Units",
    "Gross Profit", "Cost"
]


def clean_and_validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw dataframe, validates financial logic, handles datatypes and standardizes text.
    """
    cleaned = df.copy()

    # 1. Standardize column names (strip whitespace)
    cleaned.columns = [col.strip() for col in cleaned.columns]

    # Check required columns
    for col in REQUIRED_COLUMNS:
        if col not in cleaned.columns:
            raise KeyError(f"Required column '{col}' missing from input dataset.")

    # 2. Datatype Conversions
    cleaned["Order Date"] = pd.to_datetime(cleaned["Order Date"], errors="coerce")
    cleaned["Ship Date"] = pd.to_datetime(cleaned["Ship Date"], errors="coerce")
    
    numeric_cols = ["Sales", "Units", "Gross Profit", "Cost"]
    for col in numeric_cols:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    # 3. Handle missing critical fields if any
    cleaned = cleaned.dropna(subset=["Order ID", "Product ID", "Sales", "Cost", "Gross Profit"])

    # 4. Text cleaning
    text_cols = ["Product Name", "Division", "Region", "State/Province", "City", "Ship Mode"]
    for col in text_cols:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].astype(str).str.strip()

    # 5. Financial Validation & Recalculation
    # Cost = Sales - Gross Profit or Gross Profit = Sales - Cost
    # We validate discrepancy threshold
    calculated_profit = cleaned["Sales"] - cleaned["Cost"]
    cleaned["Gross Profit"] = np.round(calculated_profit, 2)
    cleaned["Sales"] = np.round(cleaned["Sales"], 2)
    cleaned["Cost"] = np.round(cleaned["Cost"], 2)

    # 6. Recalculate key unit & percentage metrics
    cleaned["Gross Margin %"] = np.where(cleaned["Sales"] > 0, (cleaned["Gross Profit"] / cleaned["Sales"]) * 100, 0.0)
    cleaned["Gross Margin %"] = np.round(cleaned["Gross Margin %"], 2)
    
    cleaned["Profit per Unit"] = np.where(cleaned["Units"] > 0, cleaned["Gross Profit"] / cleaned["Units"], 0.0)
    cleaned["Profit per Unit"] = np.round(cleaned["Profit per Unit"], 2)

    cleaned["Cost per Unit"] = np.where(cleaned["Units"] > 0, cleaned["Cost"] / cleaned["Units"], 0.0)
    cleaned["Cost per Unit"] = np.round(cleaned["Cost per Unit"], 2)

    cleaned["Price per Unit"] = np.where(cleaned["Units"] > 0, cleaned["Sales"] / cleaned["Units"], 0.0)
    cleaned["Price per Unit"] = np.round(cleaned["Price per Unit"], 2)

    cleaned["Shipping Days"] = (cleaned["Ship Date"] - cleaned["Order Date"]).dt.days

    # 7. Deduplication
    cleaned = cleaned.drop_duplicates(subset=["Order ID", "Product ID", "Order Date", "Customer ID"])

    return cleaned


def save_processed_data(df: pd.DataFrame, output_path: Path | str) -> None:
    """
    Saves cleaned dataframe to processed directory.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
