"""
Script to create the 8 Jupyter notebooks for Nassau Candy Distributor Profitability Analysis.
"""

import json
from pathlib import Path

NOTEBOOKS_DIR = Path(__file__).resolve().parent.parent / "notebooks"
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)


def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python", "version": "3.10"},
            "orig_nbformat": 4
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }


def make_markdown_cell(source_lines):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source_lines]
    }


def make_code_cell(source_lines):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source_lines]
    }


# 1. 01_data_understanding.ipynb
nb1_cells = [
    make_markdown_cell([
        "# Phase 1: Data Understanding & Initial Inspection",
        "**Project**: Product Line Profitability & Margin Performance Analysis for Nassau Candy Distributor",
        "",
        "### Objectives:",
        "- Inspect the raw dataset `data/raw/nassau_candy.csv`.",
        "- Examine shape, schema, datatypes, missing values, duplicates, and key statistics."
    ]),
    make_code_cell([
        "import pandas as pd",
        "import sys",
        "from pathlib import Path",
        "sys.path.append(str(Path.cwd().parent))",
        "from src.data_loader import load_raw_data, inspect_dataset_summary",
        "",
        "df_raw = load_raw_data(Path.cwd().parent / 'data' / 'raw' / 'nassau_candy.csv')",
        "summary = inspect_dataset_summary(df_raw)",
        "print(f'Total Rows: {summary[\"num_rows\"]}')",
        "print(f'Total Columns: {summary[\"num_columns\"]}')",
        "print(f'Duplicate Rows: {summary[\"duplicate_rows\"]}')",
        "print('Columns:', summary['columns'])"
    ]),
    make_code_cell([
        "df_raw.head()"
    ]),
    make_code_cell([
        "df_raw.info()"
    ]),
    make_code_cell([
        "df_raw.describe()"
    ])
]

# 2. 02_data_cleaning.ipynb
nb2_cells = [
    make_markdown_cell([
        "# Phase 2: Data Cleaning & Financial Validation",
        "**Project**: Nassau Candy Distributor Profitability Analysis",
        "",
        "### Objectives:",
        "- Parse dates, enforce numeric datatypes, and handle missing values.",
        "- Validate financial integrity: `Gross Profit = Sales - Cost`.",
        "- Save cleaned dataset to `data/processed/cleaned_nassau_candy.csv`."
    ]),
    make_code_cell([
        "import pandas as pd",
        "import sys",
        "from pathlib import Path",
        "sys.path.append(str(Path.cwd().parent))",
        "from src.data_loader import load_raw_data",
        "from src.data_cleaning import clean_and_validate_data, save_processed_data",
        "",
        "df_raw = load_raw_data(Path.cwd().parent / 'data' / 'raw' / 'nassau_candy.csv')",
        "df_cleaned = clean_and_validate_data(df_raw)",
        "output_path = Path.cwd().parent / 'data' / 'processed' / 'cleaned_nassau_candy.csv'",
        "save_processed_data(df_cleaned, output_path)",
        "print(f'Data cleaned successfully! Final row count: {len(df_cleaned)}')"
    ]),
    make_code_cell([
        "# Verify Financial Logic",
        "profit_diff = (df_cleaned['Sales'] - df_cleaned['Cost']) - df_cleaned['Gross Profit']",
        "print('Max absolute discrepancy between Sales - Cost and Gross Profit:', profit_diff.abs().max())"
    ])
]

# 3. 03_eda.ipynb
nb3_cells = [
    make_markdown_cell([
        "# Phase 3: Exploratory Data Analysis (EDA)",
        "**Project**: Nassau Candy Distributor Profitability Analysis",
        "",
        "### Objectives:",
        "- Analyze financial performance metrics across time, geography, and product categories."
    ]),
    make_code_cell([
        "import pandas as pd",
        "import plotly.express as px",
        "import sys",
        "from pathlib import Path",
        "sys.path.append(str(Path.cwd().parent))",
        "from src.data_loader import load_cleaned_data",
        "",
        "df = load_cleaned_data(Path.cwd().parent / 'data' / 'processed' / 'cleaned_nassau_candy.csv')"
    ]),
    make_code_cell([
        "# Monthly Sales & Profit Trend",
        "df_monthly = df.set_index('Order Date').resample('ME').agg({'Sales': 'sum', 'Gross Profit': 'sum'}).reset_index()",
        "fig = px.line(df_monthly, x='Order Date', y=['Sales', 'Gross Profit'], title='Monthly Sales & Profit Trend')",
        "fig.show()"
    ]),
    make_code_cell([
        "# Sales by Division",
        "fig_div = px.bar(df.groupby('Division')[['Sales', 'Gross Profit']].sum().reset_index(), x='Division', y=['Sales', 'Gross Profit'], barmode='group', title='Sales & Profit by Division')",
        "fig_div.show()"
    ])
]

# 4. 04_profitability_analysis.ipynb
nb4_cells = [
    make_markdown_cell([
        "# Phase 4: Profitability Analysis & Financial KPIs",
        "**Project**: Nassau Candy Distributor Profitability Analysis"
    ]),
    make_code_cell([
        "import pandas as pd",
        "import sys",
        "from pathlib import Path",
        "sys.path.append(str(Path.cwd().parent))",
        "from src.data_loader import load_cleaned_data",
        "from src.metrics import calculate_gross_margin_pct, calculate_contributions, calculate_margin_volatility",
        "",
        "df = load_cleaned_data(Path.cwd().parent / 'data' / 'processed' / 'cleaned_nassau_candy.csv')",
        "contrib = calculate_contributions(df, 'Product Name')",
        "contrib.head(10)"
    ]),
    make_code_cell([
        "volatility = calculate_margin_volatility(df)",
        "volatility.sort_values(by='Margin_Std', ascending=False).head(10)"
    ])
]

# 5. 05_product_analysis.ipynb
nb5_cells = [
    make_markdown_cell([
        "# Phase 5: Product Performance Analysis",
        "**Project**: Nassau Candy Distributor Profitability Analysis"
    ]),
    make_code_cell([
        "import pandas as pd",
        "import sys",
        "from pathlib import Path",
        "sys.path.append(str(Path.cwd().parent))",
        "from src.data_loader import load_cleaned_data",
        "from src.product_analysis import get_product_summary, identify_high_profit_products, identify_high_sales_low_margin_products, identify_margin_risk_products",
        "",
        "df = load_cleaned_data(Path.cwd().parent / 'data' / 'processed' / 'cleaned_nassau_candy.csv')",
        "prod_summary = get_product_summary(df)",
        "print('Top 5 High Profit Products:')",
        "display(identify_high_profit_products(prod_summary, 5))"
    ]),
    make_code_cell([
        "print('High Sales / Low Margin Risk Products:')",
        "display(identify_high_sales_low_margin_products(prod_summary))"
    ])
]

# 6. 06_division_analysis.ipynb
nb6_cells = [
    make_markdown_cell([
        "# Phase 6: Division Performance Analysis",
        "**Project**: Nassau Candy Distributor Profitability Analysis"
    ]),
    make_code_cell([
        "import pandas as pd",
        "import sys",
        "from pathlib import Path",
        "sys.path.append(str(Path.cwd().parent))",
        "from src.data_loader import load_cleaned_data",
        "from src.division_analysis import get_division_summary, compare_division_margins",
        "",
        "df = load_cleaned_data(Path.cwd().parent / 'data' / 'processed' / 'cleaned_nassau_candy.csv')",
        "div_summary = get_division_summary(df)",
        "display(div_summary)",
        "margin_stats = compare_division_margins(df)",
        "display(margin_stats)"
    ])
]

# 7. 07_cost_margin_analysis.ipynb
nb7_cells = [
    make_markdown_cell([
        "# Phase 7: Cost & Margin Structure Analysis",
        "**Project**: Nassau Candy Distributor Profitability Analysis"
    ]),
    make_code_cell([
        "import pandas as pd",
        "import sys",
        "from pathlib import Path",
        "sys.path.append(str(Path.cwd().parent))",
        "from src.data_loader import load_cleaned_data",
        "from src.cost_margin_analysis import analyze_cost_structure",
        "from src.visualization import plot_cost_vs_sales_scatter",
        "",
        "df = load_cleaned_data(Path.cwd().parent / 'data' / 'processed' / 'cleaned_nassau_candy.csv')",
        "cost_summary = analyze_cost_structure(df)",
        "display(cost_summary.head(10))",
        "fig = plot_cost_vs_sales_scatter(cost_summary)",
        "fig.show()"
    ])
]

# 8. 08_pareto_analysis.ipynb
nb8_cells = [
    make_markdown_cell([
        "# Phase 8: Pareto (80/20) Concentration Analysis",
        "**Project**: Nassau Candy Distributor Profitability Analysis"
    ]),
    make_code_cell([
        "import pandas as pd",
        "import sys",
        "from pathlib import Path",
        "sys.path.append(str(Path.cwd().parent))",
        "from src.data_loader import load_cleaned_data",
        "from src.pareto_analysis import calculate_revenue_pareto, calculate_profit_pareto, summarize_pareto_concentration",
        "from src.visualization import plot_pareto_chart",
        "",
        "df = load_cleaned_data(Path.cwd().parent / 'data' / 'processed' / 'cleaned_nassau_candy.csv')",
        "summary = summarize_pareto_concentration(df)",
        "print('Pareto Summary:', summary)",
        "prof_pareto = calculate_profit_pareto(df)",
        "fig = plot_pareto_chart(prof_pareto, metric='Profit')",
        "fig.show()"
    ])
]

notebook_map = {
    "01_data_understanding.ipynb": nb1_cells,
    "02_data_cleaning.ipynb": nb2_cells,
    "03_eda.ipynb": nb3_cells,
    "04_profitability_analysis.ipynb": nb4_cells,
    "05_product_analysis.ipynb": nb5_cells,
    "06_division_analysis.ipynb": nb6_cells,
    "07_cost_margin_analysis.ipynb": nb7_cells,
    "08_pareto_analysis.ipynb": nb8_cells,
}

if __name__ == "__main__":
    for name, cells in notebook_map.items():
        nb_json = make_notebook(cells)
        file_path = NOTEBOOKS_DIR / name
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(nb_json, f, indent=2)
        print(f"Created notebook: {name}")
