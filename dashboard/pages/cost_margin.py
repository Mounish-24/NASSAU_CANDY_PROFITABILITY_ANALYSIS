"""
Dashboard Page: Cost & Margin Structure
"""

import streamlit as st
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from src.cost_margin_analysis import analyze_cost_structure, identify_high_cost_products
from src.visualization import plot_cost_vs_sales_scatter
from dashboard.components.filters import render_sidebar_filters

st.set_page_config(page_title="Cost & Margin | Nassau Candy", layout="wide")

st.title("💸 Cost Structure & Margin Analysis")

filtered_df = render_sidebar_filters()

if filtered_df.empty:
    st.warning("⚠️ No records match the current filter criteria.")
    st.stop()

cost_summary = analyze_cost_structure(filtered_df)
plotly_template = st.session_state.get("plotly_template", "plotly_white")

st.subheader("Interactive Cost vs. Sales Analysis")
fig_scatter = plot_cost_vs_sales_scatter(cost_summary)
fig_scatter.update_layout(template=plotly_template)
st.plotly_chart(fig_scatter, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top High-Cost Products ($)")
    high_cost = identify_high_cost_products(cost_summary, top_n=5)
    st.dataframe(high_cost[["Product Name", "Division", "Total_Sales", "Total_Cost", "Cost_Ratio_Pct"]], use_container_width=True)

with col2:
    st.subheader("Highest Cost Ratio Products (Cost / Sales %)")
    high_ratio = cost_summary.sort_values(by="Cost_Ratio_Pct", ascending=False).head(5)
    st.dataframe(high_ratio[["Product Name", "Division", "Total_Sales", "Total_Cost", "Cost_Ratio_Pct", "Gross_Margin_Pct"]], use_container_width=True)

