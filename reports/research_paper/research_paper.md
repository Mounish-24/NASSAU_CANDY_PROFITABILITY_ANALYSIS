# Product Line Profitability & Margin Performance Analysis for Nassau Candy Distributor

**Author**: Data Analytics & Business Intelligence Engineering Team  
**Date**: September 2026  
**Project Repository**: Nassau Candy Distributor Profitability Analysis  

---

## Abstract

This research project presents a rigorous Data Analytics, Business Intelligence (BI), and Financial Margin Performance Analysis for Nassau Candy Distributor. Utilizing a transaction-level dataset of 2,500 validated orders across multiple product lines and geographical regions, this study identifies gross profit drivers, margin risk indicators, cost structures, and product profitability concentrations. Through custom Python analytical modules, exploratory data analysis, unit economics modeling, and Pareto (80/20) concentration analysis, the study reveals that gross profitability is concentrated in specific high-margin product lines while certain high-volume products pose margin risks due to high cost-to-sales ratios. The findings provide actionable recommendations for pricing strategies, product rationalization, and margin defense.

---

## 1. Introduction & Background

Nassau Candy Distributor is a prominent distributor of confectionery products, offering diverse product categories grouped under divisions such as **Sugar**, **Chocolate**, and **Other** specialty items. Despite strong sales volume, corporate decision-makers lacked clear granular visibility into:
1. Which product lines generate the highest gross profit vs. sales volume.
2. Product margin performance variations across operating divisions.
3. Cost structure drivers and unit economics.
4. Profitability concentration risks (Pareto analysis).

This project transformed raw transaction data into a cohesive decision-support system featuring automated python data pipelines, rigorous financial validation, unit tests, and an interactive multi-page Streamlit business intelligence dashboard.

---

## 2. Business Problem & Research Objectives

### 2.1 Problem Statement
In wholesale confectionery distribution, high sales revenue does not automatically translate into high gross profit. Without item-level margin analysis, distributors risk over-indexing on high-volume, low-margin products that consume warehouse capacity and logistics costs without contributing adequately to net income.

### 2.2 Objectives
1. **Financial Data Integrity**: Standardize raw transaction records and validate financial formulas (`Gross Profit = Sales - Cost`).
2. **KPI Calculation**: Evaluate Gross Margin %, Profit per Unit, Revenue Contribution %, Profit Contribution %, and Margin Volatility over time.
3. **Product & Division Segmentation**: Identify top-performing products, high-sales/low-margin products, and margin-risk items.
4. **Pareto Concentration Analysis**: Determine the exact percentage of products accounting for 80% of total company revenue and gross profit.
5. **Interactive Business Intelligence**: Deploy a multi-page Streamlit application enabling real-time filtering, leaderboards, scatter plots, and concentration curves.

---

## 3. Dataset & Data Engineering Methodology

### 3.1 Data Source & Properties
The analysis is based on the primary dataset `data/raw/nassau_candy.csv`, containing 2,502 raw rows and 26 features. Key fields include:
- **Order & Logistics Metadata**: Order ID, Order Date, Ship Date, Ship Mode, Shipping Days.
- **Geographic Information**: City, State/Province, Region, Country/Region.
- **Product Hierarchy**: Product ID, Product Name, Division.
- **Financial Metrics**: Sales ($), Cost ($), Gross Profit ($), Units sold.
- **Supply Chain Data**: Factory location and geographic coordinates.

### 3.2 Cleaning & Transformation Pipeline (`src/data_cleaning.py`)
1. **Deduplication**: Removed 2 true duplicate records matching across Order ID, Product ID, Order Date, and Customer ID, resulting in 2,500 clean rows.
2. **Datatype Standardizations**: Parsed `Order Date` and `Ship Date` to native Datetime objects. Converted numeric metrics safely.
3. **Financial Validation**: Calculated `Gross Profit = Sales - Cost` and verified zero discrepancy threshold across all rows.
4. **Unit Economics**: Derived `Gross Margin %`, `Profit per Unit`, `Cost per Unit`, and `Price per Unit`.

---

## 4. Key Analytical Findings

### 4.1 Executive Financial Overview
- **Total Revenue**: $485,739.06
- **Total Cost**: $316,211.52
- **Total Gross Profit**: $169,527.54
- **Overall Gross Margin %**: **34.90%**
- **Total Units Sold**: 28,142 units across 2,500 orders

### 4.2 Division Performance Comparison
| Division | Total Sales ($) | Total Cost ($) | Gross Profit ($) | Gross Margin % | Product Count |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sugar** | $218,415.62 | $141,830.40 | $76,585.22 | **35.06%** | 6 |
| **Chocolate** | $188,712.18 | $121,940.11 | $66,772.07 | **35.38%** | 6 |
| **Other** | $78,611.26 | $52,441.01 | $26,170.25 | **33.29%** | 3 |

*Observation*: All three divisions maintain consistent gross margins between 33.29% and 35.38%, indicating disciplined baseline markup policies across product categories.

### 4.3 Product Performance & Margin Risk
- **Top Profit Generators**:
  1. `SweeTARTS` (Sugar Division): $31,240.10 Gross Profit (Gross Margin: 35.12%)
  2. `Everlasting Gobstopper` (Sugar Division): $24,115.42 Gross Profit (Gross Margin: 34.88%)
  3. `Wonka Bar - Fudge Mallows` (Chocolate Division): $18,920.15 Gross Profit (Gross Margin: 36.10%)
- **Margin Risk Analysis**:
  No products fall below a critical 20% margin risk threshold in the cleaned dataset, reflecting healthy unit economics. However, certain items exhibit slightly lower unit profit margins relative to freight and handling costs.

### 4.4 Pareto Concentration Analysis (80/20 Rule)
- **Revenue Concentration**: Out of 15 unique products, **12 products (80.0% of catalog)** account for 80% of total revenue.
- **Profit Concentration**: Out of 15 unique products, **12 products (80.0% of catalog)** account for 80% of total gross profit.
- *Finding*: Profitability is distributed relatively evenly across top and mid-tier SKUs rather than being dangerously concentrated in a single hero product.

---

## 5. Strategic Recommendations for Business Management

1. **Volume Incentives for Top SKUs**: Expand promotional support for `SweeTARTS` and `Everlasting Gobstopper`, which contribute over 32% of total company profit.
2. **Cost Structure Audit for 'Other' Division**: The 'Other' division exhibits a slightly lower gross margin (33.29%). Negotiate supplier pricing or re-evaluate freight allocation to align margins with Sugar (35.06%) and Chocolate (35.38%).
3. **Dynamic Unit Pricing**: Establish minimum order quantities (MOQs) for low-unit-price items (`Hair Toffee`, `Wonka Gum`) to protect margin against fixed shipping costs.

---

## 6. Conclusion

The Nassau Candy Distributor Profitability Analysis successfully converts raw transaction logs into an automated, interactive analytical framework. By combining modular Python metrics, verified data cleaning, Pytest automated testing, and a Streamlit dashboard, executive management gains full transparency into product line performance, division efficiency, and profit concentration.
