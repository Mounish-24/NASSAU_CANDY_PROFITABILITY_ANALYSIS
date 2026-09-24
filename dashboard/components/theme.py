"""
Centralized Theme Manager for Nassau Candy Profitability Analysis Dashboard.
Supports Light and Dark Mode with full UI consistency across pages, sidebar, metrics, inputs, tables, and Plotly charts.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

LIGHT_THEME = "☀️ Light"
DARK_THEME = "🌙 Dark"


def init_theme():
    """Initializes theme in session state if not already set."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = LIGHT_THEME


def get_current_theme() -> str:
    """Returns current active theme string."""
    return st.session_state.get("theme", LIGHT_THEME)


def is_dark_mode() -> bool:
    """Returns True if dark mode is active."""
    return get_current_theme() == DARK_THEME


def render_top_appearance_selector():
    """
    Renders the Appearance selector at the VERY TOP of the sidebar.
    """
    init_theme()

    st.sidebar.markdown("### 🍬 Nassau Candy")
    st.sidebar.markdown("<p style='margin-top:-15px; margin-bottom:15px; font-weight:600; opacity:0.8;'>Profitability Dashboard</p>", unsafe_allow_html=True)
    
    st.sidebar.write("**Appearance**")
    
    current_index = 0 if get_current_theme() == LIGHT_THEME else 1
    selected_theme = st.sidebar.radio(
        "Appearance Mode",
        options=[LIGHT_THEME, DARK_THEME],
        index=current_index,
        horizontal=True,
        label_visibility="collapsed",
        key="global_appearance_radio"
    )

    if selected_theme != st.session_state["theme"]:
        st.session_state["theme"] = selected_theme
        st.rerun()

    st.sidebar.markdown("---")


def apply_theme():
    """
    Injects global CSS targeting all Streamlit DOM components for 100% theme consistency.
    """
    dark = is_dark_mode()

    bg_color = "#0E1117" if dark else "#F8FAFC"
    sidebar_bg = "#161B22" if dark else "#FFFFFF"
    text_color = "#F0F6FC" if dark else "#0F172A"
    subtext_color = "#94A3B8" if dark else "#475569"
    card_bg = "#1E293B" if dark else "#FFFFFF"
    card_border = "#334155" if dark else "#E2E8F0"
    metric_val_color = "#38BDF8" if dark else "#1E40AF"
    input_bg = "#1E293B" if dark else "#FFFFFF"
    input_text = "#F0F6FC" if dark else "#0F172A"
    input_border = "#475569" if dark else "#CBD5E1"
    table_header_bg = "#1E293B" if dark else "#F1F5F9"
    
    css = f"""
    <style>
        /* 1. Global App & Background */
        html, body, [data-testid="stAppViewContainer"], .stApp {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }}
        
        [data-testid="stHeader"] {{
            background-color: {bg_color} !important;
        }}

        /* 2. Sidebar Styling */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 1px solid {card_border} !important;
        }}
        [data-testid="stSidebar"] * {{
            color: {text_color} !important;
        }}
        [data-testid="stSidebar"] hr {{
            border-color: {card_border} !important;
        }}

        /* 3. Main Headers & Typography */
        .main-header {{
            font-size: 2.1rem !important;
            color: {text_color} !important;
            font-weight: 700 !important;
            margin-bottom: 0.2rem !important;
        }}
        .sub-header {{
            font-size: 1.05rem !important;
            color: {subtext_color} !important;
            margin-bottom: 1.2rem !important;
        }}
        h1, h2, h3, h4, h5, h6, label, p, span {{
            color: {text_color} !important;
        }}
        .stCaption, caption {{
            color: {subtext_color} !important;
        }}

        /* 4. KPI Cards Styling */
        div[data-testid="stMetric"] {{
            background-color: {card_bg} !important;
            border: 1px solid {card_border} !important;
            border-radius: 10px !important;
            padding: 14px 16px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        }}
        [data-testid="stMetricLabel"] p, [data-testid="stMetricLabel"] div {{
            color: {subtext_color} !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }}
        [data-testid="stMetricValue"] div {{
            color: {metric_val_color} !important;
            font-size: 1.45rem !important;
            font-weight: 700 !important;
            white-space: nowrap !important;
        }}

        /* 5. Inputs, Selectboxes, Date Pickers, File Uploader */
        div[data-baseweb="select"] > div,
        input[type="text"],
        div[data-baseweb="input"] > div {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {input_border} !important;
            border-radius: 6px !important;
        }}
        [data-testid="stFileUploader"] {{
            background-color: {card_bg} !important;
            border: 1px dashed {input_border} !important;
            border-radius: 8px !important;
            padding: 10px !important;
        }}

        /* 6. Tabs Styling */
        button[data-baseweb="tab"] {{
            color: {subtext_color} !important;
            font-weight: 600 !important;
            background-color: transparent !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {metric_val_color} !important;
            border-bottom-color: {metric_val_color} !important;
        }}

        /* 7. Tables & DataFrames */
        [data-testid="stDataFrame"], div[data-baseweb="table"] {{
            background-color: {card_bg} !important;
            border: 1px solid {card_border} !important;
            border-radius: 8px !important;
        }}
        
        /* 8. Radio Buttons & Buttons */
        div[role="radiogroup"] label {{
            background-color: {card_bg} !important;
            padding: 6px 12px !important;
            border-radius: 6px !important;
            border: 1px solid {card_border} !important;
            margin-right: 6px !important;
        }}
        .stButton button {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border: 1px solid {card_border} !important;
            border-radius: 6px !important;
        }}
        .stButton button:hover {{
            border-color: {metric_val_color} !important;
            color: {metric_val_color} !important;
        }}

        /* 9. Alert Info Boxes */
        div.stAlert {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
            border: 1px solid {card_border} !important;
            border-radius: 8px !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def apply_plotly_theme(fig, title: str = None):
    """
    Applies active theme layout to any Plotly figure.
    Sets backgrounds, font colors, gridlines, and margins.
    """
    dark = is_dark_mode()

    paper_bg = "#0E1117" if dark else "#FFFFFF"
    plot_bg = "#161B22" if dark else "#F8FAFC"
    text_color = "#F0F6FC" if dark else "#0F172A"
    grid_color = "#30363D" if dark else "#E2E8F0"
    zero_line_color = "#485563" if dark else "#CBD5E1"

    layout_update = dict(
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(color=text_color, family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"),
        xaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=zero_line_color,
            tickfont=dict(color=text_color),
            title=dict(font=dict(color=text_color))
        ),
        yaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=zero_line_color,
            tickfont=dict(color=text_color),
            title=dict(font=dict(color=text_color))
        ),
        legend=dict(
            font=dict(color=text_color),
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=30, r=30, t=45 if title else 25, b=35)
    )

    if title:
        layout_update["title"] = dict(text=title, font=dict(color=text_color, size=16))

    fig.update_layout(**layout_update)

    # For dual axis (yaxis2) if present
    if hasattr(fig.layout, "yaxis2") and fig.layout.yaxis2:
        fig.update_layout(yaxis2=dict(
            gridcolor=grid_color,
            zerolinecolor=zero_line_color,
            tickfont=dict(color=text_color),
            title=dict(font=dict(color=text_color))
        ))

    return fig
