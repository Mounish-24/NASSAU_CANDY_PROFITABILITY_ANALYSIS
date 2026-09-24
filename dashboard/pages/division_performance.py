"""
Dashboard Page: Division Performance
"""

import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from src.division_analysis import get_division_summary, compare_division_margins
from src.visualization import plot_revenue_and_profit_by_division
from dashboard.components.filters import render_sidebar_filters

st.set_page_config(page_title="Division Performance | Nassau Candy", layout="wide")

st.title("🏢 Division Performance & Comparative Analysis")

filtered_df = render_sidebar_filters()

if filtered_df.empty:
    st.warning("⚠️ No records match the selected filter criteria.")
    st.stop()

if "Division" not in filtered_df.columns or filtered_df["Division"].dropna().empty:
    st.info("No Division classification available in current dataset.")
    st.stop()

div_summary = get_division_summary(filtered_df)
margin_stats = compare_division_margins(filtered_df)

plotly_template = st.session_state.get("plotly_template", "plotly_white")

col1, col2 = st.columns([3, 2])

with col1:
    fig_div = plot_revenue_and_profit_by_division(div_summary)
    fig_div.update_layout(template=plotly_template)
    st.plotly_chart(fig_div, use_container_width=True)

with col2:
    st.subheader("Division Summary Metrics")
    st.dataframe(
        div_summary[["Division", "Total_Sales", "Total_Profit", "Gross_Margin_Pct", "Product_Count"]],
        use_container_width=True
    )

st.subheader("📊 Division Gross Margin % Box Plot Distribution")
fig_box = px.box(
    filtered_df,
    x="Division",
    y="Gross Margin %",
    color="Division",
    points="all",
    title="Gross Margin % Distribution Across Divisions",
    template=plotly_template
)
st.plotly_chart(fig_box, use_container_width=True)

st.subheader("Statistical Margin Breakdown")
st.dataframe(margin_stats, use_container_width=True)

