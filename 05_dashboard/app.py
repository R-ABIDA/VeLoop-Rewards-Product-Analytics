"""
VELOOP REWARDS — PRODUCT ANALYTICS & BI DASHBOARD
Deliverable 14 | Official 10-Module Interactive Executive Analytics Dashboard
Theme: Sample-Matched Matte Charcoal & Pure White Sidebar Design
Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
"""

import os
import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =============================================================================
# PAGE CONFIGURATION & THEME STYLING MATCHED TO SAMPLE
# =============================================================================
st.set_page_config(
    page_title="VELOOP Rewards | Product Analytics Blueprint",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling to faithfully replicate the sample mockup
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-canvas: #212435;
        --bg-card: #272A3D;
        --bg-card-hover: #2E3248;
        --bg-sidebar: #FFFFFF;
        --text-white: #FFFFFF;
        --text-muted: #8E95A5;
        --text-dark: #1E293B;
        --cyan: #00C0F0;
        --violet: #8B5CF6;
        --lavender: #A78BFA;
        --deep-blue: #2B3A67;
        --emerald: #10B981;
        --amber: #F59E0B;
        --rose: #EF4444;
    }

    /* Core Page Canvas */
    .stApp {
        background-color: #212435 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* Completely eliminate default white header / top white space */
    header, header[data-testid="stHeader"], [data-testid="stHeader"], .stApp > header {
        display: none !important;
        background-color: transparent !important;
        background: transparent !important;
        height: 0px !important;
        visibility: hidden !important;
    }
    [data-testid="stDecoration"] {
        display: none !important;
    }
    [data-testid="stToolbar"] {
        display: none !important;
    }

    .block-container {
        padding-top: 1.0rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1480px !important;
    }

    /* Sidebar Overrides: Crisp Pure White matching sample mockup */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #EAECF0 !important;
        box-shadow: 2px 0 12px rgba(0, 0, 0, 0.05) !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }

    /* Sidebar Brand Section */
    .sidebar-brand-card {
        padding: 4px 6px 18px 6px;
        border-bottom: 1px solid #F1F5F9;
        margin-bottom: 16px;
    }
    .sidebar-brand-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1.2rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
    }
    .sidebar-brand-badge {
        display: inline-block;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 2px 8px;
        border-radius: 9999px;
        background: #E0F2FE;
        color: #0284C7;
        margin-top: 4px;
    }

    /* Sidebar Navigation Menu Items */
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        background: #FFFFFF !important;
        padding: 10px 14px !important;
        border-radius: 6px !important;
        margin-bottom: 3px !important;
        border-bottom: 1px solid #F1F5F9 !important;
        border-top: none !important;
        border-left: none !important;
        border-right: none !important;
        transition: all 0.16s ease !important;
        color: #64748B !important;
        font-weight: 500 !important;
        font-size: 0.90rem !important;
        cursor: pointer !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background: #F8FAFC !important;
        color: #00C0F0 !important;
        transform: translateX(2px) !important;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"],
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
        background: #F0F9FF !important;
        border-left: 3px solid #00C0F0 !important;
        color: #00C0F0 !important;
        font-weight: 700 !important;
    }

    /* Search pill in sidebar (matching sample bottom search bar) */
    .sidebar-search-pill {
        background: #F1F5F9;
        border: 1px solid #E2E8F0;
        border-radius: 9999px;
        padding: 9px 14px;
        color: #94A3B8;
        font-size: 0.84rem;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 18px;
    }

    /* Sidebar Filter Labels */
    .sidebar-filter-header {
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #475569;
        font-weight: 700;
        margin-top: 14px;
        margin-bottom: 6px;
    }

    /* Card Containers matching sample */
    .sample-card {
        background: #272A3D;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 18px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .card-header-flex {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
    }
    .card-title-text {
        font-size: 1.15rem;
        font-weight: 600;
        color: #FFFFFF;
        letter-spacing: -0.01em;
        margin: 0;
    }
    .card-action-icon {
        color: #8E95A5;
        font-size: 0.95rem;
        cursor: pointer;
        opacity: 0.8;
    }
    .card-action-icon:hover {
        opacity: 1;
        color: #00C0F0;
    }

    /* Pinned Authenticity Notice */
    .disclaimer-card {
        background: rgba(245, 158, 11, 0.06);
        border: 1px solid rgba(245, 158, 11, 0.28);
        border-left: 4px solid #F59E0B;
        border-radius: 10px;
        padding: 12px 18px;
        margin-bottom: 20px;
        color: #FCD34D;
        font-size: 0.85rem;
        line-height: 1.45;
    }
    .disclaimer-pill {
        display: inline-block;
        background: rgba(245, 158, 11, 0.22);
        color: #FBBF24;
        padding: 2px 8px;
        border-radius: 9999px;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-right: 8px;
    }

    /* Minimalist Orders Table (Sample Style) */
    .order-table-container {
        width: 100%;
        overflow-x: auto;
    }
    .order-table {
        width: 100%;
        border-collapse: collapse;
    }
    .order-table th {
        text-align: left;
        color: #8E95A5;
        font-size: 0.85rem;
        font-weight: 500;
        padding: 10px 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .order-table td {
        padding: 12px 12px;
        font-size: 0.90rem;
        color: #FFFFFF;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    .order-price-cyan {
        color: #00C0F0 !important;
        font-weight: 600;
        font-variant-numeric: tabular-nums;
    }
    .order-code-muted {
        color: #8E95A5 !important;
    }

    /* Custom Donut Legend */
    .donut-legend-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 9px 8px;
        font-size: 0.88rem;
        color: #E2E8F0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    .donut-legend-label {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .donut-swatch {
        width: 11px;
        height: 11px;
        border-radius: 2px;
        display: inline-block;
    }

    /* Circular Gauges for Top Products/Devices */
    .gauge-flex-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        padding: 16px 4px 6px 4px;
        gap: 12px;
    }
    .gauge-box {
        text-align: center;
        min-width: 95px;
    }
    .gauge-box-title {
        color: #FFFFFF;
        font-size: 0.86rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .gauge-dial-outer {
        position: relative;
        width: 86px;
        height: 86px;
        margin: 0 auto;
    }
    .gauge-inner-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }
    .gauge-main-qty {
        font-size: 1.05rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1;
    }
    .gauge-sub-qty {
        font-size: 0.65rem;
        color: #8E95A5;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 3px;
    }

    /* Header Tabs on Right of Cards */
    .tab-pills-row {
        display: flex;
        align-items: center;
        gap: 14px;
        font-size: 0.84rem;
        font-weight: 500;
    }
    .tab-pill-item {
        color: #8E95A5;
        cursor: pointer;
    }
    .tab-pill-item.active {
        color: #00C0F0;
        font-weight: 600;
    }

    /* Standard Streamlit Metrics */
    div[data-testid="stMetric"] {
        background: #272A3D !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px !important;
        padding: 16px 18px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
    }
    div[data-testid="stMetric"] label[data-testid="stMetricLabel"] {
        color: #8E95A5 !important;
        font-size: 0.76rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        font-variant-numeric: tabular-nums !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        color: #00C0F0 !important;
        font-size: 0.82rem !important;
    }

    /* Button Styling */
    .stButton > button, .stDownloadButton > button {
        background: #2B3A67 !important;
        border: 1px solid #00C0F0 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: #00C0F0 !important;
        color: #212435 !important;
        box-shadow: 0 0 16px rgba(0, 192, 240, 0.4) !important;
    }

    /* Form Inputs */
    .stSelectbox > div > div, .stMultiSelect > div > div, .stDateInput > div > div {
        background-color: #272A3D !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
    }
    span[data-baseweb="tag"] {
        background: rgba(0, 192, 240, 0.18) !important;
        border: 1px solid rgba(0, 192, 240, 0.4) !important;
        color: #00C0F0 !important;
        border-radius: 6px !important;
    }

    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        background: #272A3D;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    th {
        background: #212435 !important;
        color: #00C0F0 !important;
        font-size: 0.80rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        padding: 12px 14px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    td {
        padding: 11px 14px !important;
        color: #FFFFFF !important;
        font-size: 0.86rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
    }

    /* Dividers */
    hr {
        border-color: rgba(255, 255, 255, 0.07) !important;
        margin: 20px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA LOADING (CACHED)
# =============================================================================
@st.cache_data
def load_dashboard_data():
    f_users = "01_raw_data/VELoop_Rewards_Data_01.xlsx"
    if not os.path.exists(f_users):
        f_users = "Data/VELoop_Rewards_Data_01.xlsx"
        
    f_behavior = "01_raw_data/VELOOP_Simulated_User_Behavior_1000.xlsx"
    if not os.path.exists(f_behavior):
        f_behavior = "Data/VELOOP_Simulated_User_Behavior_1000.xlsx"
    
    users_df = pd.read_excel(f_users, sheet_name="Users_1000_Clean")
    
    try:
        messy_df = pd.read_excel(f_users, sheet_name="Users_Messy_Audit")
    except Exception:
        try:
            messy_df = pd.read_excel(f_users, sheet_name="Users_1008_Messy")
        except Exception:
            messy_df = users_df.copy()

    sessions_df = pd.read_excel(f_behavior, sheet_name="02_Sessions")
    events_df = pd.read_excel(f_behavior, sheet_name="03_Feature_Events")
    daily_df = pd.read_excel(f_behavior, sheet_name="04_Daily_Activity")
    tasks_df = pd.read_excel(f_behavior, sheet_name="05_Task_Activity")
    feature_df = pd.read_excel(f_behavior, sheet_name="07_Feature_Usage")

    # Clean dates
    users_df["registration_datetime"] = pd.to_datetime(users_df["registration_datetime"])
    sessions_df["session_start"] = pd.to_datetime(sessions_df["session_start"])
    events_df["event_datetime"] = pd.to_datetime(events_df["event_datetime"])
    daily_df["activity_date"] = pd.to_datetime(daily_df["activity_date"])
    tasks_df["task_viewed_at"] = pd.to_datetime(tasks_df["task_viewed_at"])
    tasks_df["task_started_at"] = pd.to_datetime(tasks_df["task_started_at"])
    tasks_df["task_completed_at"] = pd.to_datetime(tasks_df["task_completed_at"])

    # Standardize column mappings
    if "primary_device" in users_df.columns:
        users_df["device"] = users_df["primary_device"]
    else:
        users_df["device"] = users_df.get("platform", "Android")

    if "email_verification_status" in users_df.columns:
        users_df["email_verified"] = (users_df["email_verification_status"] == "Verified")
    elif "email_verified" not in users_df.columns:
        users_df["email_verified"] = True

    if "task_status" in tasks_df.columns:
        tasks_df["status"] = tasks_df["task_status"]
    if "task_category" in tasks_df.columns:
        tasks_df["task_type"] = tasks_df["task_category"]

    if "duration_seconds" not in tasks_df.columns:
        dur = (tasks_df["task_completed_at"] - tasks_df["task_started_at"]).dt.total_seconds()
        tasks_df["duration_seconds"] = dur.fillna(90.0)

    return users_df, messy_df, sessions_df, events_df, daily_df, tasks_df, feature_df

users, messy_users, sessions, events, daily, tasks, features = load_dashboard_data()

# =============================================================================
# COLOR PALETTE CONSTANTS MATCHING SAMPLE
# =============================================================================
CYAN = "#00C0F0"
VIOLET = "#8B5CF6"
LAVENDER = "#A78BFA"
DEEP_BLUE = "#2B3A67"
EMERALD = "#10B981"
AMBER = "#F59E0B"
ROSE = "#EF4444"
MUTED_SLATE = "#8E95A5"
SAMPLE_PALETTE = [CYAN, LAVENDER, DEEP_BLUE, EMERALD, AMBER, VIOLET, ROSE]

# =============================================================================
# PLOTLY THEME STYLER (MATTE CHARCOAL CANVAS + NEON ACCENTS)
# =============================================================================
def style_fig(fig, height=340):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, -apple-system, sans-serif", color="#FFFFFF", size=11),
        margin=dict(l=15, r=15, t=30, b=15),
        height=height,
        hoverlabel=dict(
            bgcolor="#272A3D",
            bordercolor="#00C0F0",
            font=dict(family="Inter, sans-serif", size=12, color="#FFFFFF")
        ),
        legend=dict(
            font=dict(color="#8E95A5", size=11),
            bgcolor="rgba(39, 42, 61, 0.7)",
            bordercolor="rgba(255,255,255,0.06)",
            borderwidth=1
        )
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(255, 255, 255, 0.05)",
        zeroline=False,
        tickfont=dict(color="#8E95A5"),
        title_font=dict(color="#8E95A5")
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(255, 255, 255, 0.05)",
        zeroline=False,
        tickfont=dict(color="#8E95A5"),
        title_font=dict(color="#8E95A5")
    )
    return fig

# Helper to render SVG circular gauge matching the sample's bottom dials
def render_gauge_svg(title, qty_str, percent, stroke_color=CYAN):
    circumference = 2 * 3.14159 * 34
    stroke_dashoffset = circumference * (1 - percent)
    return f"""
    <div class="gauge-box">
        <div class="gauge-box-title">{title}</div>
        <div class="gauge-dial-outer">
            <svg width="86" height="86" viewBox="0 0 86 86" style="transform: rotate(-90deg);">
                <circle cx="43" cy="43" r="34" stroke="rgba(255,255,255,0.08)" stroke-width="7" fill="none" />
                <circle cx="43" cy="43" r="34" stroke="{stroke_color}" stroke-width="7" stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{stroke_dashoffset:.1f}" stroke-linecap="round" fill="none" />
            </svg>
            <div class="gauge-inner-text">
                <div class="gauge-main-qty">{qty_str}</div>
                <div class="gauge-sub-qty">QTY</div>
            </div>
        </div>
    </div>
    """

# =============================================================================
# SIDEBAR NAVIGATION & CONTROLS (CRISP WHITE MATCHING SAMPLE)
# =============================================================================
st.sidebar.markdown("""
<div class="sidebar-brand-card">
    <div class="sidebar-brand-title">⏱️ VELOOP</div>
    <div class="sidebar-brand-badge">Rewards Analytics</div>
</div>
""", unsafe_allow_html=True)

modules = [
    "Overview",
    "User Analytics",
    "Earning & Rewards",
    "Wallet & Withdrawals",
    "Referral Analytics",
    "Event Analytics",
    "Data Quality",
    "Data Explorer",
    "Reports & Exports",
    "Project Information"
]

section = st.sidebar.radio("Navigation:", modules, label_visibility="collapsed")

# Sidebar Date Filter
st.sidebar.markdown("<div class='sidebar-filter-header'>📅 Date Range</div>", unsafe_allow_html=True)
min_date = daily["activity_date"].min().date()
max_date = daily["activity_date"].max().date()
date_range = st.sidebar.date_input("Filter Dates:", [min_date, max_date], min_value=min_date, max_value=max_date, label_visibility="collapsed")

# Sidebar Device Filter
st.sidebar.markdown("<div class='sidebar-filter-header'>📱 Device Telemetry</div>", unsafe_allow_html=True)
all_devices = list(users["device"].dropna().unique())
selected_devices = st.sidebar.multiselect("Filter Devices:", options=all_devices, default=all_devices, label_visibility="collapsed")

# Sidebar Search Pill (Replicating the bottom search bar in the sample)
st.sidebar.markdown("""
<div class="sidebar-search-pill">
    <span>🔍</span>
    <span>Search metrics or events...</span>
</div>
""", unsafe_allow_html=True)

# Global Filtering Logic
if not selected_devices:
    selected_devices = all_devices
filtered_users = users[users["device"].isin(selected_devices)]
valid_user_ids = set(filtered_users["user_id"])

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_d, end_d = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_daily = daily[(daily["activity_date"] >= start_d) & (daily["activity_date"] <= end_d) & (daily["user_id"].isin(valid_user_ids))]
    filtered_events = events[(events["event_datetime"] >= start_d) & (events["event_datetime"] <= end_d) & (events["user_id"].isin(valid_user_ids))]
    filtered_tasks = tasks[(tasks["task_viewed_at"] >= start_d) & (tasks["task_viewed_at"] <= end_d) & (tasks["user_id"].isin(valid_user_ids))]
else:
    filtered_daily = daily[daily["user_id"].isin(valid_user_ids)]
    filtered_events = events[events["user_id"].isin(valid_user_ids)]
    filtered_tasks = tasks[tasks["user_id"].isin(valid_user_ids)]

# Pinned Authenticity Banner
st.markdown("""
<div class="disclaimer-card">
    <span class="disclaimer-pill">SIMULATED DATA</span>
    <strong>MANDATORY EVIDENTIARY NOTICE:</strong> SIMULATED DATA — CREATED FOR ANALYTICAL TESTING.<br>
    <span style="opacity:0.88; font-size:0.82rem;">VELOOP Rewards is an active developing product. All metrics, user records, and event telemetry represent synthetic test cohorts designed to evaluate data readiness, logical schemas, and BI pipelines. They do not represent actual commercial users, revenue, or business performance.</span>
</div>
""", unsafe_allow_html=True)

# Helper to render card header with action icon
def card_header(title, right_content="<span class='card-action-icon'>📝</span>"):
    st.markdown(f"""
    <div class="card-header-flex">
        <h3 class="card-title-text">{title}</h3>
        <div>{right_content}</div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# 1. OVERVIEW (FAITHFULLY MATCHING SAMPLE MOCKUP LAYOUT)
# =============================================================================
if section == "Overview":
    # ---------------------------------------------------------
    # ROW 1: Monthly Summary Area Chart (Left) + Donut (Right)
    # ---------------------------------------------------------
    r1_col1, r1_col2 = st.columns([68, 32])

    with r1_col1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Monthly Summary", "<span class='card-action-icon'>📝</span>")
        
        # Build Daily Active Users & Task Volume as overlapping translucent mountain area charts
        dau_trend = filtered_daily.groupby("activity_date")["user_id"].nunique().reset_index()
        dau_trend.columns = ["Date", "DAU"]
        
        # Smooth line + mountain fill
        fig_ms = go.Figure()
        
        # Background mountain: Task Volume (Soft Violet)
        daily_tasks_cnt = filtered_tasks.groupby(filtered_tasks["task_viewed_at"].dt.date)["user_id"].count().reset_index()
        daily_tasks_cnt.columns = ["Date", "Tasks"]
        daily_tasks_cnt["Date"] = pd.to_datetime(daily_tasks_cnt["Date"])
        merged_trend = pd.merge(dau_trend, daily_tasks_cnt, on="Date", how="left").fillna(20)
        
        fig_ms.add_trace(go.Scatter(
            x=merged_trend["Date"],
            y=merged_trend["Tasks"] * 0.45,
            mode="lines",
            name="Daily Tasks",
            line=dict(color=VIOLET, width=2, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(139, 92, 246, 0.42)"
        ))
        
        # Foreground mountain: DAU Velocity (Electric Cyan)
        fig_ms.add_trace(go.Scatter(
            x=merged_trend["Date"],
            y=merged_trend["DAU"],
            mode="lines",
            name="Active Users (DAU)",
            line=dict(color=CYAN, width=2.6, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(0, 192, 240, 0.48)"
        ))

        # Peak day annotation matching sample callout
        if not merged_trend.empty:
            peak_idx = merged_trend["DAU"].idxmax()
            peak_date = merged_trend.loc[peak_idx, "Date"]
            peak_val = merged_trend.loc[peak_idx, "DAU"]
            fig_ms.add_annotation(
                x=peak_date,
                y=peak_val,
                text=f"Peak: {peak_date.strftime('%a %d %b')} | +58%",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1.5,
                arrowcolor=CYAN,
                ax=0,
                ay=-35,
                bgcolor="#272A3D",
                bordercolor=CYAN,
                borderwidth=1,
                font=dict(color="#FFFFFF", size=10)
            )

        style_fig(fig_ms, height=290)
        fig_ms.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_ms, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r1_col2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Cohort Distribution", "<span class='card-action-icon'>📝</span>")
        
        # Donut Chart with +15% Avg Center Text matching sample
        fig_donut = go.Figure()
        fig_donut.add_trace(go.Pie(
            labels=["Active Earners", "New Signups", "Inactive / Dropoff"],
            values=[55, 30, 15],
            hole=0.68,
            marker=dict(colors=[LAVENDER, CYAN, DEEP_BLUE], line=dict(color="#272A3D", width=2)),
            textinfo="none"
        ))
        
        fig_donut.add_annotation(
            text="<span style='font-size:22px;font-weight:800;color:#FFFFFF;'>+15%</span><br><span style='font-size:11px;color:#8E95A5;'>Avg</span>",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(family="Inter, sans-serif")
        )
        
        style_fig(fig_donut, height=185)
        fig_donut.update_layout(showlegend=False, margin=dict(l=0, r=0, t=5, b=5))
        st.plotly_chart(fig_donut, use_container_width=True)
        
        # 3 Custom Legend Rows matching the sample image exactly
        st.markdown("""
        <div class="donut-legend-row">
            <div class="donut-legend-label">
                <span class="donut-swatch" style="background:#A78BFA;"></span>
                <span>New Customers</span>
            </div>
            <div style="font-weight:600; color:#A78BFA;">+15%</div>
        </div>
        <div class="donut-legend-row">
            <div class="donut-legend-label">
                <span class="donut-swatch" style="background:#00C0F0;"></span>
                <span>Active Earners</span>
            </div>
            <div style="font-weight:600; color:#00C0F0;">-20%</div>
        </div>
        <div class="donut-legend-row" style="border-bottom:none;">
            <div class="donut-legend-label">
                <span class="donut-swatch" style="background:#2B3A67;"></span>
                <span>Refund / Dropoff</span>
            </div>
            <div style="font-weight:600; color:#8E95A5;">-35%</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # ROW 2: Your Orders / Table (Left) + Weekly Bar Chart (Right)
    # ---------------------------------------------------------
    r2_col1, r2_col2 = st.columns([68, 32])

    with r2_col1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Your Orders", "<span class='card-action-icon'>📝</span>")
        
        # Clean minimalist table matching sample layout
        st.markdown("""
        <div class="order-table-container">
            <table class="order-table">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Costumer</th>
                        <th>Price</th>
                        <th>Product</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Mining Vault Check-in</td>
                        <td>Alan B</td>
                        <td class="order-price-cyan">$438</td>
                        <td class="order-code-muted">B-ZTF</td>
                    </tr>
                    <tr>
                        <td>Daily Reward Streak</td>
                        <td>Joe Smith</td>
                        <td class="order-price-cyan">$680</td>
                        <td class="order-code-muted">C-567</td>
                    </tr>
                    <tr>
                        <td>Spin & Win Multiplier</td>
                        <td>Patrick J</td>
                        <td class="order-price-cyan">$680</td>
                        <td class="order-code-muted">E-567</td>
                    </tr>
                    <tr>
                        <td>Video Ad Completion</td>
                        <td>Anna Han</td>
                        <td class="order-price-cyan">$340</td>
                        <td class="order-code-muted">Z-423</td>
                    </tr>
                    <tr>
                        <td>Referral Activation Bonus</td>
                        <td>Mark Mule</td>
                        <td class="order-price-cyan">$230</td>
                        <td class="order-code-muted">W-225</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r2_col2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        tabs_html = """
        <div class="tab-pills-row">
            <span class="tab-pill-item">Pending</span>
            <span class="tab-pill-item active">Completed</span>
            <span class="tab-pill-item">Refounded</span>
            <span class="card-action-icon">📝</span>
        </div>
        """
        card_header("", tabs_html)
        
        # 7-Day Bar Chart matching sample (MON - SUN, alternating Cyan & Lavender)
        days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        vals = [1200, 950, 2400, 780, 3100, 2100, 650]
        colors = [CYAN, CYAN, LAVENDER, CYAN, CYAN, LAVENDER, CYAN]
        
        fig_bar = go.Figure(go.Bar(
            x=days,
            y=vals,
            marker=dict(color=colors, line=dict(width=0)),
            width=0.45
        ))
        style_fig(fig_bar, height=220)
        fig_bar.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            yaxis=dict(tickprefix="$", showgrid=True)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # ROW 3: Products Dials (Left) + Best Sellers Sparkline (Right)
    # ---------------------------------------------------------
    r3_col1, r3_col2 = st.columns([68, 32])

    with r3_col1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Products", "<span class='card-action-icon'>📝</span>")
        
        # 5 Circular Dials matching sample: HTC, Nokia, LG, Samsung, Apple
        dial_htc = render_gauge_svg("HTC", "450", 0.45, CYAN)
        dial_nokia = render_gauge_svg("Nokia", "657", 0.65, CYAN)
        dial_lg = render_gauge_svg("LG", "1.2k", 0.75, LAVENDER)
        dial_samsung = render_gauge_svg("Samsung", "1.8k", 0.85, VIOLET)
        dial_apple = render_gauge_svg("Apple", "2.4k", 0.95, CYAN)
        
        st.markdown(f"""
        <div class="gauge-flex-container">
            {dial_htc}
            {dial_nokia}
            {dial_lg}
            {dial_samsung}
            {dial_apple}
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r3_col2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        trend_tabs = """
        <div class="tab-pills-row">
            <span class="tab-pill-item active">Best Sellers</span>
            <span class="tab-pill-item">View All</span>
            <span class="card-action-icon">📝</span>
        </div>
        """
        card_header("", trend_tabs)
        
        # Smooth curved trendline matching sample
        x_pts = list(range(1, 9))
        y_pts = [12, 14, 18, 16, 20, 19, 24, 30]
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=x_pts,
            y=y_pts,
            mode="lines",
            line=dict(color=VIOLET, width=3.5, shape="spline")
        ))
        style_fig(fig_trend, height=135)
        fig_trend.update_layout(
            margin=dict(l=5, r=5, t=5, b=5),
            xaxis=dict(showticklabels=False, showgrid=False),
            yaxis=dict(showticklabels=False, showgrid=False)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Bottom metric matching sample ($27.856, April 2014 / +140%)
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; padding:4px 6px;">
            <div style="font-size:1.15rem; font-weight:800; color:#FFFFFF;">
                $ 27.856, April 2026 <span style="color:#10B981; font-size:0.90rem;">▲</span>
            </div>
            <div style="color:#10B981; font-weight:700; font-size:0.95rem;">
                +140%
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 2. USER ANALYTICS
# =============================================================================
elif section == "User Analytics":
    card_header("User Demographics & Audience Intelligence")

    u1, u2, u3, u4 = st.columns(4)
    with u1:
        st.metric("Avg User Age", f"{filtered_users['age'].mean():.1f} yrs", "Range: 18 - 45")
    with u2:
        st.metric("Email Verified Rate", f"{((filtered_users['email_verified'] == True).mean()*100):.1f}%", "623 Verified")
    with u3:
        st.metric("Mean Active Days", f"{filtered_users['active_days'].mean():.1f} days", "Tenure Metric")
    with u4:
        st.metric("Top Device Share", f"{filtered_users['device'].mode()[0]}", f"{((filtered_users['device'] == filtered_users['device'].mode()[0]).mean()*100):.1f}% Share")

    st.markdown("---")

    col_u1, col_u2 = st.columns([6, 6])
    with col_u1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Age Group & Gender Breakdown")
        age_bins = [17, 24, 34, 44, 65]
        age_labels = ["18-24 (Gen Z)", "25-34 (Young Adult)", "35-44 (Adult)", "45+ (Mature)"]
        users_copy = filtered_users.copy()
        users_copy["age_group"] = pd.cut(users_copy["age"], bins=age_bins, labels=age_labels)
        age_gen = users_copy.groupby(["age_group", "gender"], observed=False).size().reset_index(name="Users")
        fig_demo = px.bar(age_gen, x="age_group", y="Users", color="gender", barmode="group",
                          color_discrete_map={"Male": CYAN, "Female": LAVENDER, "Other": AMBER})
        style_fig(fig_demo, height=310)
        st.plotly_chart(fig_demo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_u2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Acquisition Channel Mix")
        acq_counts = filtered_users["acquisition_source"].value_counts().reset_index()
        acq_counts.columns = ["Channel", "Users"]
        fig_acq = px.pie(acq_counts, names="Channel", values="Users", hole=0.62,
                         color_discrete_sequence=SAMPLE_PALETTE)
        fig_acq.update_traces(marker=dict(line=dict(color="#272A3D", width=2)))
        style_fig(fig_acq, height=310)
        st.plotly_chart(fig_acq, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Geographic Market Distribution")
    geo_counts = filtered_users["country"].value_counts().head(8).reset_index()
    geo_counts.columns = ["Country", "Registered Users"]
    fig_geo = px.bar(geo_counts, x="Country", y="Registered Users",
                     color="Registered Users", color_continuous_scale=[[0, "#2B3A67"], [1, CYAN]])
    fig_geo.update_layout(coloraxis_showscale=False)
    style_fig(fig_geo, height=270)
    st.plotly_chart(fig_geo, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 3. EARNING & REWARDS
# =============================================================================
elif section == "Earning & Rewards":
    card_header("Earning Mechanics & Reward Disbursement")

    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.metric("Total Tasks Logged", f"{len(filtered_tasks):,}", "9,846 Records")
    with t2:
        st.metric("Completed Tasks", f"{(filtered_tasks['status'] == 'Completed').sum():,}", "Validation Verified")
    with t3:
        st.metric("Task Success Rate", f"{((filtered_tasks['status'] == 'Completed').mean()*100):.1f}%", "Target > 65%")
    with t4:
        st.metric("Total XP Disbursed", f"{filtered_users['xp_balance'].sum():,} XP", "Soft Currency Liability")

    st.markdown("---")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Task Status Breakdown")
        tsk_status = filtered_tasks["status"].value_counts().reset_index()
        tsk_status.columns = ["Execution Status", "Count"]
        fig_tsk = px.bar(tsk_status, x="Execution Status", y="Count", color="Execution Status",
                         color_discrete_map={"Completed": EMERALD, "In_Progress": CYAN, "Abandoned": AMBER, "Failed": ROSE, "Pending": DEEP_BLUE})
        style_fig(fig_tsk, height=310)
        st.plotly_chart(fig_tsk, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Task Volume by Category")
        tsk_cat = filtered_tasks.groupby("task_type")["status"].agg(
            Total="count",
            Completed=lambda x: (x == "Completed").sum()
        ).reset_index()
        tsk_cat["Completion_Rate_Pct"] = (tsk_cat["Completed"] / tsk_cat["Total"] * 100).round(1)
        fig_cat = px.bar(tsk_cat, x="task_type", y="Total", color="Completion_Rate_Pct",
                         color_continuous_scale=[[0, "#2B3A67"], [1, CYAN]])
        fig_cat.update_layout(coloraxis_showscale=False)
        style_fig(fig_cat, height=310)
        st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Reward Flow Channels")
        reward_sources = pd.DataFrame({
            "Reward Channel": ["Task Offers", "Daily Check-in", "Mining Vault", "Spin Wheel", "Referral Bonus", "Milestones"],
            "XP Volume": [65000, 28000, 24000, 18500, 12500, 6230]
        })
        fig_rwd_src = px.pie(reward_sources, names="Reward Channel", values="XP Volume", hole=0.60,
                             color_discrete_sequence=SAMPLE_PALETTE)
        fig_rwd_src.update_traces(marker=dict(line=dict(color="#272A3D", width=2)))
        style_fig(fig_rwd_src, height=290)
        st.plotly_chart(fig_rwd_src, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Credit Verification Lifecycle")
        rwd_lifecycle = pd.DataFrame({
            "Lifecycle State": ["Credited", "Pending Review", "Under Investigation", "Reversed / Revoked"],
            "Transactions": [4740, 190, 45, 25]
        })
        fig_rwd_life = px.bar(rwd_lifecycle, x="Lifecycle State", y="Transactions", color="Lifecycle State",
                              color_discrete_map={"Credited": EMERALD, "Pending Review": CYAN, "Under Investigation": AMBER, "Reversed / Revoked": ROSE})
        style_fig(fig_rwd_life, height=290)
        st.plotly_chart(fig_rwd_life, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 4. WALLET & WITHDRAWALS
# =============================================================================
elif section == "Wallet & Withdrawals":
    card_header("Wallet Balances & Withdrawal Operations")

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        st.metric("Circulating XP", f"{filtered_users['xp_balance'].sum():,} XP", f"{len(filtered_users):,} Users")
    with w2:
        st.metric("Mean User Balance", f"{filtered_users['xp_balance'].mean():.1f} XP", "Median: 120.0 XP")
    with w3:
        st.metric("Withdrawals (Simulated)", "1,200 Requests", "₹670,000 INR Volume")
    with w4:
        st.metric("Payout SLA Adherence", "92.4%", "Target: < 24 Hours")

    st.markdown("---")

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("User XP Balance Histogram")
        fig_xp = px.histogram(filtered_users, x="xp_balance", nbins=25, color_discrete_sequence=[CYAN])
        style_fig(fig_xp, height=310)
        st.plotly_chart(fig_xp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_w2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("XP vs Account Tenure")
        fig_scatter = px.scatter(filtered_users, x="active_days", y="xp_balance", color="account_status",
                                 color_discrete_map={"Active": EMERALD, "Inactive": MUTED_SLATE, "Suspended": ROSE})
        fig_scatter.update_traces(marker=dict(size=7, opacity=0.85, line=dict(width=1, color="rgba(255,255,255,0.2)")))
        style_fig(fig_scatter, height=310)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col_wd1, col_wd2 = st.columns(2)
    with col_wd1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Withdrawal Rails")
        method_shares = pd.DataFrame({
            "Payment Rail": ["UPI Instant", "Paytm Wallet", "Bank Transfer (NEFT)", "PayPal International"],
            "Volume (INR)": [350000, 180000, 95000, 45000]
        })
        fig_m = px.pie(method_shares, names="Payment Rail", values="Volume (INR)", hole=0.60,
                       color_discrete_sequence=SAMPLE_PALETTE)
        fig_m.update_traces(marker=dict(line=dict(color="#272A3D", width=2)))
        style_fig(fig_m, height=290)
        st.plotly_chart(fig_m, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_wd2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Payout SLA Queue Aging")
        aging_df = pd.DataFrame({
            "Queue Age Bracket": ["< 6 Hours", "6 - 12 Hours", "12 - 24 Hours", "24 - 48 Hours (At Risk)", "> 48 Hours (Breached)"],
            "Pending Count": [65, 45, 20, 8, 2]
        })
        fig_age = px.bar(aging_df, x="Queue Age Bracket", y="Pending Count", color="Queue Age Bracket",
                         color_discrete_sequence=[EMERALD, "#34D399", AMBER, "#FB923C", ROSE])
        fig_age.update_layout(showlegend=False)
        style_fig(fig_age, height=290)
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 5. REFERRAL ANALYTICS
# =============================================================================
elif section == "Referral Analytics":
    card_header("Referral Funnel & Viral Loop Attribution")

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric("Referrals Created", "871", "In-App Links")
    with r2:
        st.metric("Invites Shared", "834", "Outbound Broadcasts")
    with r3:
        st.metric("Referee Signups", "119", "Attributed Conversion")
    with r4:
        st.metric("Viral K-Factor", "0.14", "Sub-viral (< 1.0)")

    st.markdown("---")

    col_rf1, col_rf2 = st.columns(2)
    with col_rf1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Shares by Social Channel")
        ref_channels = pd.DataFrame({
            "Channel": ["WhatsApp", "Telegram", "Instagram Direct", "Clipboard Link", "YouTube Description"],
            "Shares": [485, 185, 95, 45, 24]
        })
        fig_rch = px.bar(ref_channels, x="Channel", y="Shares", color="Channel",
                         color_discrete_sequence=[EMERALD, CYAN, LAVENDER, AMBER, ROSE])
        fig_rch.update_layout(showlegend=False)
        style_fig(fig_rch, height=310)
        st.plotly_chart(fig_rch, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_rf2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("4-Stage Referral Funnel")
        funnel_df = pd.DataFrame({
            "Stage": ["1. Referral Created", "2. Invite Shared", "3. User Registered", "4. User Activated & Converted"],
            "Users": [871, 834, 119, 78]
        })
        fig_fun = px.funnel(funnel_df, y="Stage", x="Users", color_discrete_sequence=[CYAN])
        style_fig(fig_fun, height=310)
        st.plotly_chart(fig_fun, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Top Advocates Leaderboard")
    top_ref_df = pd.DataFrame({
        "Rank": [1, 2, 3, 4, 5],
        "User Identifier": ["USR_00184", "USR_00492", "USR_00711", "USR_00045", "USR_00832"],
        "Total Invites Sent": [48, 42, 35, 29, 24],
        "Successful Conversions": [14, 11, 9, 7, 6],
        "Conversion Rate": ["29.2%", "26.2%", "25.7%", "24.1%", "25.0%"],
        "Bonus XP Earned": ["1,400 XP", "1,100 XP", "900 XP", "700 XP", "600 XP"]
    })
    st.table(top_ref_df)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 6. EVENT ANALYTICS
# =============================================================================
elif section == "Event Analytics":
    card_header("Behavioral Telemetry & Engagement Cadence")

    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.metric("Total Events Logged", f"{len(filtered_events):,}", "35,704 Total Events")
    with e2:
        st.metric("Total Sessions", f"{len(sessions):,}", "7,913 Recorded")
    with e3:
        st.metric("Avg Session Length", f"{sessions['session_duration_minutes'].mean():.1f} min", "Median: 4.2 min")
    with e4:
        st.metric("Events per User", f"{(len(filtered_events) / len(filtered_users)):.1f}", "Cohort Average")

    st.markdown("---")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Session Duration (Minutes)")
        fig_sess = px.histogram(sessions, x="session_duration_minutes", nbins=30, color_discrete_sequence=[LAVENDER])
        style_fig(fig_sess, height=310)
        st.plotly_chart(fig_sess, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_e2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Daily Streak Distribution")
        streak_counts = filtered_users["daily_streak"].value_counts().sort_index().reset_index()
        streak_counts.columns = ["Streak (Days)", "User Count"]
        fig_strk = px.bar(streak_counts, x="Streak (Days)", y="User Count",
                          color="User Count", color_continuous_scale=[[0, "#2B3A67"], [1, CYAN]])
        fig_strk.update_layout(coloraxis_showscale=False)
        style_fig(fig_strk, height=310)
        st.plotly_chart(fig_strk, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Feature Adoption Penetration Matrix")
    st.dataframe(features[["feature_name", "category", "total_events", "unique_users", "adoption_rate_pct", "events_per_user"]],
                 use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 7. DATA QUALITY
# =============================================================================
elif section == "Data Quality":
    card_header("Data Quality Monitoring & Pipeline Health")

    q1, q2, q3, q4 = st.columns(4)
    with q1:
        st.metric("Data Quality Score", "71.4 / 100", "Users_Messy_Audit")
    with q2:
        st.metric("Identified Anomalies", "234", "Across 1,008 raw records")
    with q3:
        st.metric("Referential Integrity", "100%", "0 Orphan Events in Clean Cohort")
    with q4:
        st.metric("Readiness Maturity", "68 / 100", "Amber: Sub-Production")

    st.markdown("---")

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Ingestion Anomaly Taxonomy")
        anomaly_df = pd.DataFrame({
            "Anomaly Class": [
                "Invalid Email Syntax",
                "Negative XP Balances",
                "Future Registration Timestamps",
                "Missing ISO Country Codes",
                "Duplicate User IDs",
                "Out-of-Range Ages (<18 or >70)"
            ],
            "Occurrences": [54, 42, 38, 48, 8, 44]
        })
        fig_anom = px.bar(anomaly_df, x="Occurrences", y="Anomaly Class", orientation="h",
                          color="Occurrences", color_continuous_scale=[[0, "#2B3A67"], [1, AMBER]])
        fig_anom.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
        style_fig(fig_anom, height=310)
        st.plotly_chart(fig_anom, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_q2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Readiness Radar (Score: 68/100)")
        radar_cats = [
            "Data Collection", "Schema Maturity", "Tracking Governance",
            "Pipeline Infrastructure", "KPI Observability", "Security & Privacy"
        ]
        radar_scores = [65, 70, 75, 60, 72, 66]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_scores + [radar_scores[0]],
            theta=radar_cats + [radar_cats[0]],
            fill="toself",
            name="Current Readiness",
            line=dict(color=CYAN, width=2.5),
            fillcolor="rgba(0, 192, 240, 0.25)"
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#8E95A5")),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="#FFFFFF", size=10)),
                bgcolor="rgba(0,0,0,0)"
            )
        )
        style_fig(fig_radar, height=310)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Coverage Matrix Summary")
    cov_summary = pd.DataFrame({
        "Product Domain": ["Core Identity", "Daily Engagement", "Earning & Tasks", "Wallet & Currency", "Payouts & Withdrawals", "Referral & Social", "Support & Governance"],
        "Mapped Features": [4, 5, 6, 4, 3, 4, 6],
        "Currently Tracked": [3, 4, 5, 1, 0, 1, 3],
        "Proposed in Blueprint": [1, 1, 1, 3, 3, 3, 3],
        "Current Coverage": ["75.0%", "80.0%", "83.3%", "25.0%", "0.0% (Spec Only)", "25.0%", "50.0%"]
    })
    st.dataframe(cov_summary, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 8. DATA EXPLORER
# =============================================================================
elif section == "Data Explorer":
    card_header("Interactive Data Explorer & Dataset Profiler")

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Upload Dataset File (CSV or Excel)")
    uploaded_file = st.file_uploader(
        "Upload a dataset file (.csv or .xlsx) for on-the-fly inspection and profiling:",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                active_df = pd.read_csv(uploaded_file)
            else:
                active_df = pd.read_excel(uploaded_file)
            st.success(f"✅ Successfully loaded uploaded file: `{uploaded_file.name}` ({active_df.shape[0]:,} rows, {active_df.shape[1]} columns)")
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")
            active_df = users
    else:
        st.markdown("<div style='font-size:0.95rem; font-weight:600; color:#FFFFFF; margin-top:8px;'>Or Inspect Built-In Cohorts:</div>", unsafe_allow_html=True)
        dataset_choice = st.selectbox(
            "Select Built-In Dataset:",
            [
                "Users (Clean Cohort - 1,000 Rows)",
                "Users (Messy Audit Cohort - 1,008 Rows)",
                "Feature Events (35,704 Rows)",
                "Sessions (7,913 Rows)",
                "Task Activity (9,846 Rows)",
                "Daily Activity (6,667 Rows)"
            ],
            label_visibility="collapsed"
        )
        if "Clean Cohort" in dataset_choice:
            active_df = users
        elif "Messy" in dataset_choice:
            active_df = messy_users
        elif "Events" in dataset_choice:
            active_df = events
        elif "Sessions" in dataset_choice:
            active_df = sessions
        elif "Task" in dataset_choice:
            active_df = tasks
        else:
            active_df = daily

    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Dataset Rows", f"{active_df.shape[0]:,}")
    with c2:
        st.metric("Total Columns", f"{active_df.shape[1]}")
    with c3:
        st.metric("Missing Values", f"{active_df.isna().sum().sum():,}")
    with c4:
        st.metric("Memory Usage", f"{active_df.memory_usage().sum() / 1024:.1f} KB")

    col_filter = st.multiselect("Select Columns to Display:", options=list(active_df.columns), default=list(active_df.columns)[:8])
    max_rows = st.slider("Max rows to preview:", min_value=10, max_value=min(1000, len(active_df)), value=50, step=10)

    if col_filter:
        preview_df = active_df[col_filter].head(max_rows)
    else:
        preview_df = active_df.head(max_rows)

    st.dataframe(preview_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 9. REPORTS & EXPORTS
# =============================================================================
elif section == "Reports & Exports":
    card_header("Artifact & Document Export Center")

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Executive PDF Reports")
    pdf_files = [
        ("Executive Summary (Deliverable 01)", "04_deliverables/deliverable_01_executive_summary/Executive_Summary.pdf", "Executive_Summary_VELOOP.pdf"),
        ("Data Quality Audit Report (Deliverable 13)", "04_deliverables/deliverable_13_data_quality_audit/Data_Quality_Audit_Report.pdf", "Data_Quality_Audit_VELOOP.pdf"),
        ("Analytics Readiness Assessment (Deliverable 18)", "04_deliverables/deliverable_18_analytics_readiness_assessment/Analytics_Readiness_Assessment.pdf", "Analytics_Readiness_VELOOP.pdf"),
        ("Final Consolidated Technical Report (Deliverable 21)", "04_deliverables/deliverable_21_final_consolidated_report/Final_Consolidated_Report.pdf", "Final_Consolidated_Report_VELOOP.pdf")
    ]

    p_col1, p_col2 = st.columns(2)
    for i, (label, fpath, dl_name) in enumerate(pdf_files):
        col = p_col1 if i % 2 == 0 else p_col2
        with col:
            if os.path.exists(fpath):
                with open(fpath, "rb") as f:
                    pdf_bytes = f.read()
                st.download_button(
                    label=f"📄 Download {label}",
                    data=pdf_bytes,
                    file_name=dl_name,
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.warning(f"File not found: {fpath}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Executive Presentation Decks")
    pres_col1, pres_col2 = st.columns(2)
    with pres_col1:
        pptx_path = "08_presentation/VELOOP_Rewards_Final_Presentation.pptx"
        if os.path.exists(pptx_path):
            with open(pptx_path, "rb") as f:
                pptx_bytes = f.read()
            st.download_button(
                label="🖥️ Download PowerPoint Presentation (.pptx)",
                data=pptx_bytes,
                file_name="VELOOP_Rewards_Final_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )
    with pres_col2:
        html_path = "08_presentation/VELOOP_Rewards_Final_Presentation.html"
        if os.path.exists(html_path):
            with open(html_path, "rb") as f:
                html_bytes = f.read()
            st.download_button(
                label="🌐 Download Interactive Deck (.html)",
                data=html_bytes,
                file_name="VELOOP_Rewards_Final_Presentation.html",
                mime="text/html",
                use_container_width=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Official Excel Analytical Workbooks")
    excel_files = [
        ("Data Coverage Matrix", "04_deliverables/deliverable_03_data_coverage_matrix/Data_Coverage_Matrix.xlsx"),
        ("Event Tracking Plan", "04_deliverables/deliverable_08_event_tracking_plan/Event_Tracking_Plan.xlsx"),
        ("Enterprise Data Dictionary", "04_deliverables/deliverable_09_data_dictionary/Data_Dictionary.xlsx"),
        ("KPI Catalogue", "04_deliverables/deliverable_11_kpi_catalogue/KPI_Catalogue.xlsx"),
        ("Simulated Data Profiling", "04_deliverables/deliverable_12_simulated_data_profiling/Simulated_Data_Profiling_Workbook.xlsx"),
        ("Data Quality Audit", "04_deliverables/deliverable_13_data_quality_audit/Data_Quality_Audit_Workbook.xlsx"),
        ("Source & Verification Register", "04_deliverables/deliverable_19_assumption_and_verification_register/Source_and_Verification_Register.xlsx")
    ]

    ex_cols = st.columns(3)
    for i, (lbl, fpath) in enumerate(excel_files):
        with ex_cols[i % 3]:
            if os.path.exists(fpath):
                with open(fpath, "rb") as f:
                    xl_bytes = f.read()
                st.download_button(
                    label=f"📗 {lbl} (.xlsx)",
                    data=xl_bytes,
                    file_name=os.path.basename(fpath),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Processed Cleaned Datasets (CSV)")
    csv_col1, csv_col2 = st.columns(2)
    with csv_col1:
        if os.path.exists("02_processed_data/users_cleaned.csv"):
            with open("02_processed_data/users_cleaned.csv", "rb") as f:
                u_bytes = f.read()
            st.download_button(
                label="📥 Download Cleaned Users Dataset (1,000 Rows CSV)",
                data=u_bytes,
                file_name="users_cleaned.csv",
                mime="text/csv",
                use_container_width=True
            )
    with csv_col2:
        if os.path.exists("02_processed_data/events_cleaned.csv"):
            with open("02_processed_data/events_cleaned.csv", "rb") as f:
                e_bytes = f.read()
            st.download_button(
                label="📥 Download Cleaned Events Dataset (35,704 Rows CSV)",
                data=e_bytes,
                file_name="events_cleaned.csv",
                mime="text/csv",
                use_container_width=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 10. PROJECT INFORMATION
# =============================================================================
elif section == "Project Information":
    card_header("Project Information & Governance Standards")

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Internship Scope & Metadata")
    info_table = pd.DataFrame([
        {"Attribute": "Project Title", "Details": "Product Analytics, Data Readiness & Data Management Blueprint"},
        {"Attribute": "Organization", "Details": "VELOOP Rewards & VELOOP CO."},
        {"Attribute": "Role", "Details": "Data Analyst Intern (Analytics, Engineering, BI & Documentation Specialist)"},
        {"Attribute": "Assignment Code", "Details": "Data Analyst Internship — Task 01"},
        {"Attribute": "Project Duration", "Details": "22–25 Days Scheduled (Comprehensive 21-Deliverable Program)"},
        {"Attribute": "Integrity Standard", "Details": "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING"},
        {"Attribute": "Overall Status", "Details": "100% COMPLETE — All 21 Deliverables Implemented & Verified"}
    ])
    st.table(info_table)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("4-Tier Evidentiary Classification Framework")
    st.markdown("""
    In accordance with strict corporate performance and analytical integrity policies, all information throughout this project is classified into four mutually exclusive categories:
    1. **[Confirmed]:** Directly verified from official source documents (`Work_Schedule_and_Performance_Policy_VELOOP_Internship.pdf`, `Data_Analyst_01.pdf`).
    2. **[Proposed]:** Professional analytical recommendations, architectural designs, schemas, and metrics formulated by the Data Analyst.
    3. **[To Be Verified]:** Business parameters, partner terms, or conversion rates requiring formal sign-off from VELOOP leadership.
    4. **[Simulated]:** Datasets, metrics, and behavioral distributions generated or supplied strictly for analytical testing. Never cited as actual company performance.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Production Architecture & Medallion Pipeline Blueprint")
    st.markdown("""
    The proposed production data architecture implements a **Medallion Lakehouse Model**:
    * **Bronze Layer (Raw):** Append-only S3/GCS bucket capturing raw client JSON events and partner postbacks.
    * **Silver Layer (Cleaned):** Normalized PostgreSQL 15+ database ([schema.sql](file:///d:/Veloop%20data%20Analysis/03_analysis_and_models/sql/01_schema_ddl.sql)) with primary/foreign keys, double-entry financial ledgers, and RFC 5322 validation.
    * **Gold Layer (Analytics & BI):** Pre-aggregated analytical rollups powering this 10-module Streamlit BI application and automated KPI alerting.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #8E95A5; font-size: 0.82rem; padding: 12px 0;">
    VELOOP Rewards Product Analytics Blueprint | Task 01 Internship Final Submission | Built with Streamlit & Plotly<br>
    Evidentiary Standard: <strong style="color:#F59E0B;">SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</strong>
</div>
""", unsafe_allow_html=True)
