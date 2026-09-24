"""
Dashboard Page: Profit Concentration (Pareto Analysis)
"""

import streamlit as st
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from src.pareto_analysis import calculate_revenue_pareto, calculate_profit_pareto, summarize_pareto_concentration
from src.visualization import plot_pareto_chart
from dashboard.components.filters import render_sidebar_filters

st.set_page_config(page_title="Profit Concentration | Nassau Candy", layout="wide")

st.title("🎯 Profit & Revenue Concentration (Pareto Analysis)")

filtered_df = render_sidebar_filters()

if filtered_df.empty:
    st.warning("⚠️ No records match the current filter criteria.")
    st.stop()

summary = summarize_pareto_concentration(filtered_df)
plotly_template = st.session_state.get("plotly_template", "plotly_white")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Active Products", summary["total_products"])
col2.metric("Products Generating 80% Revenue", f"{summary['revenue_top_80_product_count']} ({summary['revenue_top_80_product_share_pct']}%)")
col3.metric("Products Generating 80% Profit", f"{summary['profit_top_80_product_count']} ({summary['profit_top_80_product_share_pct']}%)")
col4.metric("Pareto Ratio (Profit)", f"{summary['profit_top_80_product_share_pct']}% / 80%")

tab1, tab2 = st.tabs(["Profit Pareto", "Revenue Pareto"])

with tab1:
    prof_pareto = calculate_profit_pareto(filtered_df)
    fig_prof = plot_pareto_chart(prof_pareto, metric="Profit")
    fig_prof.update_layout(template=plotly_template)
    st.plotly_chart(fig_prof, use_container_width=True)
    st.dataframe(prof_pareto, use_container_width=True)

with tab2:
    rev_pareto = calculate_revenue_pareto(filtered_df)
    fig_rev = plot_pareto_chart(rev_pareto, metric="Revenue")
    fig_rev.update_layout(template=plotly_template)
    st.plotly_chart(fig_rev, use_container_width=True)
    st.dataframe(rev_pareto, use_container_width=True)

