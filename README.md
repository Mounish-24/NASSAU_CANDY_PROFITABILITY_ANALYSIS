# Nassau Candy Distributor — Product Line Profitability & Margin Performance Analysis

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-red.svg)
![Pytest](https://img.shields.io/badge/Pytest-Passing-brightgreen.svg)

---

## 📌 Project Overview

This project provides an end-to-end Data Analytics, Business Intelligence (BI), and Financial Margin Analysis for **Nassau Candy Distributor**. It transforms 2,500 raw order transaction records into granular business insights and deploys an interactive multi-page Streamlit Dashboard to monitor gross profit, margin risks, division performance, cost drivers, and Pareto concentration curves.

---

## 🏢 Business Problem

Nassau Candy Distributor previously lacked clear visibility into:
1. Which product lines generate the highest gross profit vs. sales volume.
2. Whether high-sales products maintain healthy profit margins.
3. How profitability varies across operating divisions (Sugar, Chocolate, Other).
4. Which products represent margin risk.
5. How profit is concentrated across the product catalog (Pareto 80/20 Rule).

---

## 🛠️ Technology Stack

- **Core**: Python 3.10+, Pandas, NumPy
- **Visualization**: Plotly Express, Plotly Graph Objects, Matplotlib, Seaborn
- **Interactive Dashboard**: Streamlit
- **Environment & Notebooks**: Jupyter Notebook
- **Testing**: Pytest

---

## 📂 Project Structure

```text
NASSAU_CANDY_PROFITABILITY_ANALYSIS/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   └── nassau_candy.csv
│   └── processed/
│       └── cleaned_nassau_candy.csv
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_profitability_analysis.ipynb
│   ├── 05_product_analysis.ipynb
│   ├── 06_division_analysis.ipynb
│   ├── 07_cost_margin_analysis.ipynb
│   └── 08_pareto_analysis.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_cleaning.py
│   ├── metrics.py
│   ├── product_analysis.py
│   ├── division_analysis.py
│   ├── cost_margin_analysis.py
│   ├── pareto_analysis.py
│   └── visualization.py
│
├── dashboard/
│   ├── app.py
│   ├── pages/
│   │   ├── product_profitability.py
│   │   ├── division_performance.py
│   │   ├── cost_margin.py
│   │   └── profit_concentration.py
│   └── components/
│       ├── __init__.py
│       ├── kpi_cards.py
│       ├── charts.py
│       └── filters.py
│
├── reports/
│   ├── research_paper/
│   │   └── research_paper.md
│   └── executive_summary/
│       └── executive_summary.md
│
└── tests/
    ├── __init__.py
    ├── test_data_loader.py
    ├── test_data_cleaning.py
    └── test_metrics.py
```

---

## 🚀 Installation & Environment Setup

1. **Clone the Repository**:
   ```bash
   git clone <repo-url>
   cd NASSAU_CANDY_PROFITABILITY_ANALYSIS
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Data Cleaning & Processing Pipeline**:
   ```bash
   python -c "from src.data_loader import load_raw_data; from src.data_cleaning import clean_and_validate_data, save_processed_data; save_processed_data(clean_and_validate_data(load_raw_data()), 'data/processed/cleaned_nassau_candy.csv')"
   ```

---

## 🧪 Running Automated Tests

Run the Pytest suite to verify module functionality and financial calculations:

```bash
pytest
```

---

## 📊 Running the Streamlit Dashboard

Launch the interactive executive dashboard locally:

```bash
streamlit run dashboard/app.py
```

---

## 💡 Key Analytical Findings

- **Total Company Revenue**: **$485,739.06**
- **Total Gross Profit**: **$169,527.54** (Overall Gross Margin: **34.90%**)
- **Division Leader**: **Sugar Division** leads in revenue ($218,415.62) and gross profit ($76,585.22).
- **Top SKU**: `SweeTARTS` generates **$31,240.10** in profit at a **35.12%** gross margin.
- **Pareto Concentration**: **12 out of 15 products (80.0%)** account for 80% of total revenue and profit.
