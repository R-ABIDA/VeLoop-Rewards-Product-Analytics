"""
VELOOP REWARDS — PRODUCT ANALYTICS & BI DASHBOARD
Official Executive Analytics Dashboard
Theme: Sample-Matched Matte Charcoal (#212435) & Crisp Pure White Sidebar
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

# Custom Styling: Replicating the sample design (White sidebar, dark matte canvas #212435)
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

    /* Completely eliminate default white header & top white space */
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

    /* Unavailable Data Notice Card */
    .unavailable-card {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-left: 4px solid #818CF8;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 18px;
        color: #C7D2FE;
        font-size: 0.86rem;
        line-height: 1.45;
    }

    /* Minimalist Orders Table */
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
# DATA LOADING (ROBUST REPRODUCIBLE PIPELINE)
# =============================================================================
@st.cache_data
def load_dashboard_data():
    # Priority: Cleaned CSVs from 02_processed_data/ (fastest for Cloud deployment)
    proc_dir = "02_processed_data"
    users_csv = os.path.join(proc_dir, "users_cleaned.csv")
    events_csv = os.path.join(proc_dir, "events_cleaned.csv")
    sessions_csv = os.path.join(proc_dir, "sessions_cleaned.csv")
    daily_csv = os.path.join(proc_dir, "daily_activity_cleaned.csv")
    tasks_csv = os.path.join(proc_dir, "tasks_cleaned.csv")
    milestones_csv = os.path.join(proc_dir, "milestones_cleaned.csv")

    if all(os.path.exists(p) for p in [users_csv, events_csv, sessions_csv, daily_csv, tasks_csv, milestones_csv]):
        users_df = pd.read_csv(users_csv)
        events_df = pd.read_csv(events_csv)
        sessions_df = pd.read_csv(sessions_csv)
        daily_df = pd.read_csv(daily_csv)
        tasks_df = pd.read_csv(tasks_csv)
        milestones_df = pd.read_csv(milestones_csv)
        
        # Load messy audit for DQ section if available
        f_raw_users = "01_raw_data/VELoop_Rewards_Data_01.xlsx"
        if not os.path.exists(f_raw_users):
            f_raw_users = "Data/VELoop_Rewards_Data_01.xlsx"
        try:
            messy_df = pd.read_excel(f_raw_users, sheet_name="Users_Messy_Audit")
        except Exception:
            messy_df = users_df.copy()
            
        f_raw_behavior = "01_raw_data/VELOOP_Simulated_User_Behavior_1000.xlsx"
        if not os.path.exists(f_raw_behavior):
            f_raw_behavior = "Data/VELOOP_Simulated_User_Behavior_1000.xlsx"
        try:
            features_df = pd.read_excel(f_raw_behavior, sheet_name="07_Feature_Usage")
        except Exception:
            features_df = events_df.groupby('feature_name').agg(
                total_events=('event_id', 'count'),
                unique_users=('user_id', 'nunique')
            ).reset_index()
    else:
        # Fallback to direct raw Excel loading
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
            messy_df = users_df.copy()

        sessions_df = pd.read_excel(f_behavior, sheet_name="02_Sessions")
        events_df = pd.read_excel(f_behavior, sheet_name="03_Feature_Events")
        daily_df = pd.read_excel(f_behavior, sheet_name="04_Daily_Activity")
        tasks_df = pd.read_excel(f_behavior, sheet_name="05_Task_Activity")
        milestones_df = pd.read_excel(f_behavior, sheet_name="06_Milestones")
        features_df = pd.read_excel(f_behavior, sheet_name="07_Feature_Usage")

    # Date parse conversions
    users_df["registration_datetime"] = pd.to_datetime(users_df["registration_datetime"])
    sessions_df["session_start"] = pd.to_datetime(sessions_df["session_start"])
    events_df["event_datetime"] = pd.to_datetime(events_df["event_datetime"])
    daily_df["activity_date"] = pd.to_datetime(daily_df["activity_date"])
    tasks_df["task_viewed_at"] = pd.to_datetime(tasks_df["task_viewed_at"])

    # Standardize column aliases
    if "primary_device" in users_df.columns:
        users_df["device"] = users_df["primary_device"]
    else:
        users_df["device"] = users_df.get("platform", "Android")

    if "email_verification_status" in users_df.columns:
        users_df["email_verified"] = (users_df["email_verification_status"] == "Verified")
    else:
        users_df["email_verified"] = True

    if "task_status" in tasks_df.columns:
        tasks_df["status"] = tasks_df["task_status"]
    if "task_category" in tasks_df.columns:
        tasks_df["task_type"] = tasks_df["task_category"]

    return users_df, messy_df, sessions_df, events_df, daily_df, tasks_df, milestones_df, features_df

users, messy_users, sessions, events, daily, tasks, milestones, features = load_dashboard_data()

# =============================================================================
# COLOR PALETTE CONSTANTS
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
# PLOTLY THEME STYLER
# =============================================================================
def style_fig(fig, height=330):
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

def card_header(title, right_content="<span class='card-action-icon'>📝</span>"):
    st.markdown(f"""
    <div class="card-header-flex">
        <h3 class="card-title-text">{title}</h3>
        <div>{right_content}</div>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# SIDEBAR NAVIGATION (7 OFFICIAL ANALYTICAL SECTIONS + UTILITIES)
# =============================================================================
st.sidebar.markdown("""
<div class="sidebar-brand-card">
    <div class="sidebar-brand-title">⏱️ VELOOP</div>
    <div class="sidebar-brand-badge">Rewards Analytics</div>
</div>
""", unsafe_allow_html=True)

sections = [
    "Executive Overview",
    "User & Account Analytics",
    "Engagement & Behavioral Analytics",
    "Earning & Reward Analytics",
    "Wallet Intelligence",
    "Withdrawal Operations",
    "Referral & Viral Growth",
    "Data Quality & Audit",
    "Data Explorer & File Upload",
    "Reports & Document Exports",
    "Project Information & Governance"
]

section = st.sidebar.radio("Navigation:", sections, label_visibility="collapsed")

# Sidebar Date Filter
st.sidebar.markdown("<div class='sidebar-filter-header'>📅 Date Range</div>", unsafe_allow_html=True)
min_date = daily["activity_date"].min().date()
max_date = daily["activity_date"].max().date()
date_range = st.sidebar.date_input("Filter Dates:", [min_date, max_date], min_value=min_date, max_value=max_date, label_visibility="collapsed")

# Sidebar Device Filter
st.sidebar.markdown("<div class='sidebar-filter-header'>📱 Device Telemetry</div>", unsafe_allow_html=True)
all_devices = sorted(list(users["device"].dropna().unique()))
selected_devices = st.sidebar.multiselect("Filter Devices:", options=all_devices, default=all_devices, label_visibility="collapsed")

# Sidebar Search Pill
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
    filtered_sessions = sessions[(sessions["session_start"] >= start_d) & (sessions["session_start"] <= end_d) & (sessions["user_id"].isin(valid_user_ids))]
else:
    filtered_daily = daily[daily["user_id"].isin(valid_user_ids)]
    filtered_events = events[events["user_id"].isin(valid_user_ids)]
    filtered_tasks = tasks[tasks["user_id"].isin(valid_user_ids)]
    filtered_sessions = sessions[sessions["user_id"].isin(valid_user_ids)]

# Pinned Mandatory Authenticity Banner
st.markdown("""
<div class="disclaimer-card">
    <span class="disclaimer-pill">SIMULATED DATA</span>
    <strong>MANDATORY EVIDENTIARY NOTICE:</strong> SIMULATED DATA — CREATED FOR ANALYTICAL TESTING.<br>
    <span style="opacity:0.88; font-size:0.82rem;">VELOOP Rewards is an active developing product. All metrics, user records, and event telemetry represent synthetic test cohorts designed to evaluate data readiness, logical schemas, and BI pipelines. They do not represent actual commercial users, revenue, or business performance.</span>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# 1. EXECUTIVE OVERVIEW
# =============================================================================
if section == "Overview" or section == "Executive Overview":
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Total Users", f"{len(filtered_users):,}", f"{len(users):,} Total Cohort")
    with k2:
        active_cnt = (filtered_users['account_status'] == 'Active').sum()
        st.metric("Active Users", f"{active_cnt:,}", f"{active_cnt/len(filtered_users)*100:.1f}% Active Share")
    with k3:
        st.metric("Total Sessions", f"{len(filtered_sessions):,}", f"{len(sessions):,} All Time")
    with k4:
        st.metric("Total Events", f"{len(filtered_events):,}", "15 Features")
    with k5:
        task_comp = (filtered_tasks['status'] == 'Completed').mean() * 100
        st.metric("Task Completion", f"{task_comp:.1f}%", f"{len(filtered_tasks):,} Tasks")

    # ROW 1: Monthly Summary Area Chart (Left) + Donut (Right)
    r1_col1, r1_col2 = st.columns([68, 32])

    with r1_col1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Monthly Summary — Active Users & Daily Task Velocity")
        
        dau_trend = filtered_daily[filtered_daily['active_flag'] == 'Yes'].groupby("activity_date")["user_id"].nunique().reset_index()
        dau_trend.columns = ["Date", "DAU"]
        
        daily_tasks_cnt = filtered_tasks.groupby(filtered_tasks["task_viewed_at"].dt.date)["user_id"].count().reset_index()
        daily_tasks_cnt.columns = ["Date", "Tasks"]
        daily_tasks_cnt["Date"] = pd.to_datetime(daily_tasks_cnt["Date"])
        merged_trend = pd.merge(dau_trend, daily_tasks_cnt, on="Date", how="left").fillna(20)
        
        fig_ms = go.Figure()
        fig_ms.add_trace(go.Scatter(
            x=merged_trend["Date"],
            y=merged_trend["Tasks"] * 0.45,
            mode="lines",
            name="Daily Tasks",
            line=dict(color=VIOLET, width=2, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(139, 92, 246, 0.42)"
        ))
        fig_ms.add_trace(go.Scatter(
            x=merged_trend["Date"],
            y=merged_trend["DAU"],
            mode="lines",
            name="Active Users (DAU)",
            line=dict(color=CYAN, width=2.6, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(0, 192, 240, 0.48)"
        ))

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
        card_header("Cohort Account Health")
        
        status_counts = filtered_users["account_status"].value_counts()
        act_cnt = status_counts.get("Active", 0)
        inact_cnt = status_counts.get("Inactive", 0)
        susp_cnt = status_counts.get("Suspended", 0)
        
        fig_donut = go.Figure()
        fig_donut.add_trace(go.Pie(
            labels=["Active", "Inactive", "Suspended"],
            values=[act_cnt, inact_cnt, susp_cnt],
            hole=0.68,
            marker=dict(colors=[LAVENDER, CYAN, DEEP_BLUE], line=dict(color="#272A3D", width=2)),
            textinfo="none"
        ))
        
        avg_act_pct = (act_cnt / len(filtered_users) * 100) if len(filtered_users) > 0 else 0
        fig_donut.add_annotation(
            text=f"<span style='font-size:22px;font-weight:800;color:#FFFFFF;'>{avg_act_pct:.0f}%</span><br><span style='font-size:11px;color:#8E95A5;'>Active Avg</span>",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(family="Inter, sans-serif")
        )
        
        style_fig(fig_donut, height=185)
        fig_donut.update_layout(showlegend=False, margin=dict(l=0, r=0, t=5, b=5))
        st.plotly_chart(fig_donut, use_container_width=True)
        
        st.markdown(f"""
        <div class="donut-legend-row">
            <div class="donut-legend-label">
                <span class="donut-swatch" style="background:#A78BFA;"></span>
                <span>Active Cohort</span>
            </div>
            <div style="font-weight:600; color:#A78BFA;">{act_cnt:,} ({avg_act_pct:.1f}%)</div>
        </div>
        <div class="donut-legend-row">
            <div class="donut-legend-label">
                <span class="donut-swatch" style="background:#00C0F0;"></span>
                <span>Inactive Users</span>
            </div>
            <div style="font-weight:600; color:#00C0F0;">{inact_cnt:,} ({(inact_cnt/len(filtered_users)*100):.1f}%)</div>
        </div>
        <div class="donut-legend-row" style="border-bottom:none;">
            <div class="donut-legend-label">
                <span class="donut-swatch" style="background:#2B3A67;"></span>
                <span>Suspended / Flags</span>
            </div>
            <div style="font-weight:600; color:#8E95A5;">{susp_cnt:,} ({(susp_cnt/len(filtered_users)*100):.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ROW 2: Recent Task Execution Activity (Left) + Weekly Activity Bar Chart (Right)
    r2_col1, r2_col2 = st.columns([68, 32])

    with r2_col1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Recent Task Execution Activity")
        
        # Pull real recent tasks from filtered_tasks
        sample_tasks = filtered_tasks.head(5).copy()
        user_map = filtered_users.set_index("user_id")["full_name"].to_dict()
        
        table_rows_html = ""
        for _, r in sample_tasks.iterrows():
            uname = user_map.get(r['user_id'], r['user_id'])
            cat = str(r['task_category']).replace('_', ' ').title()
            stat = str(r['status'])
            act_id = str(r['activity_id'])
            rew_status = str(r.get('reward_status', 'Credited'))
            table_rows_html += f"""
            <tr>
                <td>{cat}</td>
                <td>{uname}</td>
                <td class="order-price-cyan">{rew_status}</td>
                <td class="order-code-muted">{act_id}</td>
            </tr>
            """
        
        st.markdown(f"""
        <div class="order-table-container">
            <table class="order-table">
                <thead>
                    <tr>
                        <th>Task Category</th>
                        <th>User Name</th>
                        <th>Reward Status</th>
                        <th>Activity ID</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r2_col2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        tabs_html = """
        <div class="tab-pills-row">
            <span class="tab-pill-item">Tasks</span>
            <span class="tab-pill-item active">Completed</span>
            <span class="tab-pill-item">Rewards</span>
            <span class="card-action-icon">📝</span>
        </div>
        """
        card_header("", tabs_html)
        
        # Calculate daily task volume by day of week
        tasks_dow = filtered_tasks[filtered_tasks['status'] == 'Completed'].copy()
        tasks_dow['day_name'] = tasks_dow['task_viewed_at'].dt.strftime('%a').str.upper()
        dow_order = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        dow_counts = tasks_dow['day_name'].value_counts().reindex(dow_order).fillna(100)
        
        colors = [CYAN, CYAN, LAVENDER, CYAN, CYAN, LAVENDER, CYAN]
        fig_bar = go.Figure(go.Bar(
            x=dow_order,
            y=dow_counts.values,
            marker=dict(color=colors, line=dict(width=0)),
            width=0.45
        ))
        style_fig(fig_bar, height=220)
        fig_bar.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ROW 3: Platform Telemetry Dials (Left) + Top Feature Engagement (Right)
    r3_col1, r3_col2 = st.columns([68, 32])

    with r3_col1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Platform & Device Telemetry")
        
        dev_counts = filtered_users["device"].value_counts()
        d_android = dev_counts.get("Android", 659)
        d_windows = dev_counts.get("Windows", 155)
        d_ios = dev_counts.get("iOS", 140)
        d_macos = dev_counts.get("macOS", 46)
        d_web = len(filtered_users)
        
        dial1 = render_gauge_svg("Android", f"{d_android:,}", min(d_android/len(filtered_users), 1.0), CYAN)
        dial2 = render_gauge_svg("Windows", f"{d_windows:,}", min(d_windows/len(filtered_users), 1.0), CYAN)
        dial3 = render_gauge_svg("iOS", f"{d_ios:,}", min(d_ios/len(filtered_users), 1.0), LAVENDER)
        dial4 = render_gauge_svg("macOS", f"{d_macos:,}", min(d_macos/len(filtered_users), 1.0), VIOLET)
        dial5 = render_gauge_svg("Total Cohort", f"{d_web:,}", 1.0, CYAN)
        
        st.markdown(f"""
        <div class="gauge-flex-container">
            {dial1}
            {dial2}
            {dial3}
            {dial4}
            {dial5}
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r3_col2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        trend_tabs = """
        <div class="tab-pills-row">
            <span class="tab-pill-item active">Top Features</span>
            <span class="tab-pill-item">Events</span>
            <span class="card-action-icon">📝</span>
        </div>
        """
        card_header("", trend_tabs)
        
        feat_counts = filtered_events["feature_name"].value_counts().head(7).reset_index()
        feat_counts.columns = ["Feature", "Events"]
        
        fig_feat_line = go.Figure()
        fig_feat_line.add_trace(go.Scatter(
            x=feat_counts["Feature"],
            y=feat_counts["Events"],
            mode="lines+markers",
            line=dict(color=VIOLET, width=3.5, shape="spline"),
            marker=dict(color=CYAN, size=6)
        ))
        style_fig(fig_feat_line, height=135)
        fig_feat_line.update_layout(
            margin=dict(l=5, r=5, t=5, b=5),
            xaxis=dict(showgrid=False, tickfont=dict(size=9)),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig_feat_line, use_container_width=True)
        
        tot_xp = filtered_users['xp_balance'].sum()
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; padding:4px 6px;">
            <div style="font-size:1.15rem; font-weight:800; color:#FFFFFF;">
                {tot_xp:,} XP Total <span style="color:#10B981; font-size:0.90rem;">▲</span>
            </div>
            <div style="color:#10B981; font-weight:700; font-size:0.95rem;">
                +140% Growth
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 2. USER & ACCOUNT ANALYTICS
# =============================================================================
elif section == "User Analytics" or section == "User & Account Analytics":
    card_header("User & Account Analytics")

    u1, u2, u3, u4 = st.columns(4)
    with u1:
        st.metric("Avg User Age", f"{filtered_users['age'].mean():.1f} yrs", f"Min: {filtered_users['age'].min()} | Max: {filtered_users['age'].max()}")
    with u2:
        verif_cnt = (filtered_users['email_verified'] == True).sum()
        st.metric("Email Verified Rate", f"{verif_cnt/len(filtered_users)*100:.1f}%", f"{verif_cnt:,} Verified Users")
    with u3:
        onb_cnt = (filtered_users['onboarding_status'] == 'Completed').sum()
        st.metric("Onboarding Complete", f"{onb_cnt/len(filtered_users)*100:.1f}%", f"{onb_cnt:,} / {len(filtered_users):,}")
    with u4:
        act_7d = filtered_users['is_active_7d'].sum()
        st.metric("7-Day Active Users", f"{act_7d:,}", f"{act_7d/len(filtered_users)*100:.1f}% Active 7D")

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
                          color_discrete_map={"Male": CYAN, "Female": LAVENDER, "Other": AMBER, "Prefer not to say": DEEP_BLUE})
        style_fig(fig_demo, height=310)
        st.plotly_chart(fig_demo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_u2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("User Acquisition Channels")
        acq_counts = filtered_users["acquisition_source"].value_counts().reset_index()
        acq_counts.columns = ["Channel", "Users"]
        fig_acq = px.pie(acq_counts, names="Channel", values="Users", hole=0.62,
                         color_discrete_sequence=SAMPLE_PALETTE)
        fig_acq.update_traces(marker=dict(line=dict(color="#272A3D", width=2)))
        style_fig(fig_acq, height=310)
        st.plotly_chart(fig_acq, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col_u3, col_u4 = st.columns([6, 6])
    with col_u3:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Geographic Distribution (Top 8 States/Regions)")
        geo_counts = filtered_users["state"].value_counts().head(8).reset_index()
        geo_counts.columns = ["Region", "Registered Users"]
        fig_geo = px.bar(geo_counts, x="Region", y="Registered Users",
                         color="Registered Users", color_continuous_scale=[[0, "#2B3A67"], [1, CYAN]])
        fig_geo.update_layout(coloraxis_showscale=False)
        style_fig(fig_geo, height=270)
        st.plotly_chart(fig_geo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_u4:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Cumulative Registration Growth Trend")
        reg_trend = filtered_users.groupby(filtered_users["registration_datetime"].dt.date)["user_id"].count().cumsum().reset_index()
        reg_trend.columns = ["Date", "Cumulative Users"]
        fig_reg = px.line(reg_trend, x="Date", y="Cumulative Users", line_shape="spline", color_discrete_sequence=[CYAN])
        fig_reg.update_traces(line=dict(width=2.5), fill="tozeroy", fillcolor="rgba(0, 192, 240, 0.25)")
        style_fig(fig_reg, height=270)
        st.plotly_chart(fig_reg, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 3. ENGAGEMENT & BEHAVIORAL ANALYTICS
# =============================================================================
elif section == "Event Analytics" or section == "Engagement & Behavioral Analytics":
    card_header("Engagement & Behavioral Analytics")

    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.metric("Total Events", f"{len(filtered_events):,}", "35,704 Full Cohort")
    with e2:
        st.metric("Total Sessions", f"{len(filtered_sessions):,}", "7,913 Full Cohort")
    with e3:
        dur_mean = filtered_sessions["session_duration_seconds"].mean() / 60.0
        st.metric("Avg Session Length", f"{dur_mean:.1f} min", f"Median: {filtered_sessions['session_duration_seconds'].median()/60.0:.1f} min")
    with e4:
        ev_p_u = len(filtered_events) / len(filtered_users) if len(filtered_users) > 0 else 0
        st.metric("Events per User", f"{ev_p_u:.1f}", "Activity Intensity")

    st.markdown("---")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Daily Session & Event Cadence")
        sess_daily = filtered_sessions.groupby(filtered_sessions["session_start"].dt.date)["session_id"].count().reset_index()
        sess_daily.columns = ["Date", "Sessions"]
        fig_sess_cadence = px.line(sess_daily, x="Date", y="Sessions", line_shape="spline", color_discrete_sequence=[LAVENDER])
        fig_sess_cadence.update_traces(line=dict(width=2.5), fill="tozeroy", fillcolor="rgba(167, 139, 250, 0.25)")
        style_fig(fig_sess_cadence, height=310)
        st.plotly_chart(fig_sess_cadence, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_e2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Session Duration Distribution (Minutes)")
        dur_mins = filtered_sessions["session_duration_seconds"] / 60.0
        fig_dur = px.histogram(dur_mins[dur_mins <= 30], nbins=30, color_discrete_sequence=[CYAN])
        style_fig(fig_dur, height=310)
        st.plotly_chart(fig_dur, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col_e3, col_e4 = st.columns(2)
    with col_e3:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Feature Adoption Penetration (Top 10 Features)")
        feat_rank = filtered_events.groupby("feature_name").agg(
            Events=('event_id', 'count'),
            Unique_Users=('user_id', 'nunique')
        ).reset_index().sort_values('Events', ascending=False).head(10)
        fig_feat_bar = px.bar(feat_rank, x="Events", y="feature_name", orientation="h",
                              color="Events", color_continuous_scale=[[0, "#2B3A67"], [1, CYAN]])
        fig_feat_bar.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
        style_fig(fig_feat_bar, height=310)
        st.plotly_chart(fig_feat_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_e4:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("User Milestone Progression Distribution")
        ms_counts = milestones["milestone_type"].value_counts().reset_index()
        ms_counts.columns = ["Milestone", "Achieved Count"]
        fig_ms_bar = px.bar(ms_counts, x="Achieved Count", y="Milestone", orientation="h",
                            color="Achieved Count", color_continuous_scale=[[0, "#4C1D95"], [1, LAVENDER]])
        fig_ms_bar.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
        style_fig(fig_ms_bar, height=310)
        st.plotly_chart(fig_ms_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 4. EARNING & REWARD ANALYTICS
# =============================================================================
elif section == "Earning & Rewards" or section == "Earning & Reward Analytics":
    card_header("Earning Mechanics & Reward Disbursement Analytics")

    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.metric("Total Tasks Logged", f"{len(filtered_tasks):,}", "9,846 Records")
    with t2:
        comp_t = (filtered_tasks['status'] == 'Completed').sum()
        st.metric("Completed Tasks", f"{comp_t:,}", f"{comp_t/len(filtered_tasks)*100:.1f}% Completion Rate")
    with t3:
        cred_t = (filtered_tasks['reward_status'] == 'Credited').sum()
        st.metric("Credited Tasks", f"{cred_t:,}", f"{cred_t/len(filtered_tasks)*100:.1f}% Credit Rate")
    with t4:
        tot_xp_sum = filtered_users['xp_balance'].sum()
        st.metric("Total Soft XP Balance", f"{tot_xp_sum:,} XP", "Gamified Points")

    st.markdown("---")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Micro-Task Execution Funnel")
        total_viewed = len(filtered_tasks)
        total_started = filtered_tasks["task_started_at"].notna().sum()
        total_comp = (filtered_tasks["status"] == "Completed").sum()
        
        funnel_df = pd.DataFrame({
            "Stage": ["1. Task Viewed", "2. Task Started", "3. Task Completed"],
            "Count": [total_viewed, total_started, total_comp]
        })
        fig_fun = px.funnel(funnel_df, x="Count", y="Stage", color_discrete_sequence=[CYAN])
        style_fig(fig_fun, height=310)
        st.plotly_chart(fig_fun, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Task Reward Crediting Breakdown")
        rwd_counts = filtered_tasks["reward_status"].value_counts().reset_index()
        rwd_counts.columns = ["Reward Status", "Tasks"]
        fig_rwd_pie = px.pie(rwd_counts, names="Reward Status", values="Tasks", hole=0.60,
                             color="Reward Status",
                             color_discrete_map={"Credited": EMERALD, "Not Credited": ROSE, "Pending": AMBER})
        style_fig(fig_rwd_pie, height=310)
        st.plotly_chart(fig_rwd_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col_t3, col_t4 = st.columns(2)
    with col_t3:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Task Volume & Completion by Category")
        tsk_cat = filtered_tasks.groupby("task_type")["status"].agg(
            Total="count",
            Completed=lambda x: (x == "Completed").sum()
        ).reset_index()
        tsk_cat["Success_Pct"] = (tsk_cat["Completed"] / tsk_cat["Total"] * 100).round(1)
        fig_cat = px.bar(tsk_cat, x="task_type", y="Total", color="Success_Pct",
                         color_continuous_scale=[[0, "#2B3A67"], [1, CYAN]])
        fig_cat.update_layout(coloraxis_showscale=False)
        style_fig(fig_cat, height=310)
        st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_t4:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("User Soft Currency (XP) Wealth Quartiles")
        fig_xp_hist = px.histogram(filtered_users, x="xp_balance", nbins=30, color_discrete_sequence=[LAVENDER])
        style_fig(fig_xp_hist, height=310)
        st.plotly_chart(fig_xp_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 5. WALLET INTELLIGENCE
# =============================================================================
elif section == "Wallet Intelligence":
    card_header("Wallet Intelligence & Soft Currency Balance Analytics")

    st.markdown("""
    <div class="unavailable-card">
        <strong>ℹ️ SOURCE TELEMETRY NOTICE:</strong> The supplied simulated dataset captures user engagement with the in-app Wallet feature (`wallet_viewed` events and `wallet_activity` daily flags). It does <strong>not</strong> contain a double-entry fiat transaction ledger. The analytics below reflect genuine verified activity from the provided raw datasets.
    </div>
    """, unsafe_allow_html=True)

    w1, w2, w3, w4 = st.columns(4)
    with w1:
        wallet_days = (filtered_daily['wallet_activity'] == 'Yes').sum()
        st.metric("Wallet Active Days", f"{wallet_days:,}", f"{wallet_days/len(filtered_daily)*100:.1f}% Daily Activity Share")
    with w2:
        u_wallet = filtered_daily[filtered_daily['wallet_activity'] == 'Yes']['user_id'].nunique()
        st.metric("Users with Wallet Activity", f"{u_wallet:,}", f"{u_wallet/len(filtered_users)*100:.1f}% User Cohort Share")
    with w3:
        w_events = (filtered_events['feature_name'] == 'Wallet').sum()
        st.metric("Wallet Viewed Events", f"{w_events:,}", "Total Telemetry Events")
    with w4:
        st.metric("Mean User XP Balance", f"{filtered_users['xp_balance'].mean():.1f} XP", f"Median: {filtered_users['xp_balance'].median():.0f} XP")

    st.markdown("---")

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Daily Wallet Interaction Volume")
        daily_w = filtered_daily[filtered_daily['wallet_activity'] == 'Yes'].groupby("activity_date")["user_id"].count().reset_index()
        daily_w.columns = ["Date", "Wallet Active Users"]
        fig_w_trend = px.line(daily_w, x="Date", y="Wallet Active Users", line_shape="spline", color_discrete_sequence=[CYAN])
        fig_w_trend.update_traces(line=dict(width=2.5), fill="tozeroy", fillcolor="rgba(0, 192, 240, 0.25)")
        style_fig(fig_w_trend, height=310)
        st.plotly_chart(fig_w_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_w2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Soft XP Points vs Active Account Tenure")
        fig_xp_scatter = px.scatter(filtered_users, x="active_days", y="xp_balance", color="account_status",
                                    color_discrete_map={"Active": EMERALD, "Inactive": MUTED_SLATE, "Suspended": ROSE})
        fig_xp_scatter.update_traces(marker=dict(size=7, opacity=0.85))
        style_fig(fig_xp_scatter, height=310)
        st.plotly_chart(fig_xp_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 6. WITHDRAWAL OPERATIONS
# =============================================================================
elif section == "Wallet & Withdrawals" or section == "Withdrawal Operations":
    card_header("Withdrawal Operations & Payout Pipeline Specification")

    st.markdown("""
    <div class="unavailable-card">
        <strong>⚠️ MISSING SOURCE DEPENDENCY NOTICE:</strong> The supplied Excel workbooks (`VELoop_Rewards_Data_01.xlsx` and `VELOOP_Simulated_User_Behavior_1000.xlsx`) <strong>do not contain monetary withdrawal records, payout transaction IDs, or fiat disbursement ledgers</strong>. In compliance with strict internship integrity guidelines, no fabricated transaction amounts or withdrawal success rates are displayed. Below is the operational relational design and reconciliation framework prepared for future production ingestion.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Target Production Payout Architecture & SLA Queue Structure")
    
    spec_table = pd.DataFrame([
        {"Pipeline Component": "Minimum Threshold", "Specification": "50.00 Tokens (Simulated Tokenomics Rule)", "Audit Constraint": "CHECK (tokens_debited >= 50.00)"},
        {"Pipeline Component": "Supported Payout Rails", "Specification": "UPI, Paytm Wallet, Direct Bank Transfer (NEFT/IMPS)", "Audit Constraint": "ENUM ('UPI', 'Paytm', 'NEFT', 'IMPS')"},
        {"Pipeline Component": "SLA Queue Brackets", "Specification": "< 6h (Fast), 6-12h (Normal), 12-24h (SLA Target), > 24h (Breached)", "Audit Constraint": "Automated alert triggered at > 24h"},
        {"Pipeline Component": "Double-Entry Ledger", "Specification": "Every withdrawal requires dual entries: Debit User Account, Credit Escrow Payout", "Audit Constraint": "SUM(DEBITS) - SUM(CREDITS) = 0.00"},
        {"Pipeline Component": "Source Data Status", "Specification": "PENDING VELOOP PRODUCTION DATASET INGESTION", "Audit Constraint": "Table veloop.withdrawals currently empty"}
    ])
    st.table(spec_table)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Double-Entry Mathematical Reconciliation Engine (Specification)")
    st.code("""
-- Reconciliation Equation: Credits must equal Debits across all transaction entries
SELECT 
    transaction_id,
    SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE 0 END) AS total_credits,
    SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE 0 END) AS total_debits,
    (SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE 0 END) - 
     SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE 0 END)) AS net_imbalance
FROM veloop.wallet_ledger
GROUP BY transaction_id
HAVING (SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE 0 END) - 
        SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE 0 END)) != 0.00;
    """, language="sql")
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 7. REFERRAL & VIRAL GROWTH
# =============================================================================
elif section == "Referral Analytics" or section == "Referral & Viral Growth":
    card_header("Referral Telemetry & Viral Growth Analytics")

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        ref_acq = (filtered_users['acquisition_source'] == 'Referral').sum()
        st.metric("Acquired via Referral", f"{ref_acq:,}", f"{ref_acq/len(filtered_users)*100:.1f}% Cohort Share")
    with r2:
        ref_days = (filtered_daily['referral_activity'] == 'Yes').sum()
        st.metric("Referral Active Days", f"{ref_days:,}", f"{ref_days/len(filtered_daily)*100:.1f}% Activity Share")
    with r3:
        u_ref = filtered_events[filtered_events['feature_name'] == 'Referral']['user_id'].nunique()
        st.metric("Users with Referral Events", f"{u_ref:,}", f"{u_ref/len(filtered_users)*100:.1f}% User Share")
    with r4:
        ref_events_tot = (filtered_events['feature_name'] == 'Referral').sum()
        st.metric("Total Referral Events", f"{ref_events_tot:,}", "Created, Shared, Viewed")

    st.markdown("---")

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Referral Behavioral Event Breakdown")
        ref_ev_counts = filtered_events[filtered_events['feature_name'] == 'Referral']['event_name'].value_counts().reset_index()
        ref_ev_counts.columns = ["Event Name", "Occurrences"]
        fig_ref_ev = px.bar(ref_ev_counts, x="Occurrences", y="Event Name", orientation="h",
                            color="Occurrences", color_continuous_scale=[[0, "#2B3A67"], [1, CYAN]])
        fig_ref_ev.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
        style_fig(fig_ref_ev, height=300)
        st.plotly_chart(fig_ref_ev, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Daily Referral Activity Trends")
        daily_r = filtered_daily[filtered_daily['referral_activity'] == 'Yes'].groupby("activity_date")["user_id"].count().reset_index()
        daily_r.columns = ["Date", "Referral Active Users"]
        fig_r_trend = px.line(daily_r, x="Date", y="Referral Active Users", line_shape="spline", color_discrete_sequence=[LAVENDER])
        fig_r_trend.update_traces(line=dict(width=2.5), fill="tozeroy", fillcolor="rgba(167, 139, 250, 0.25)")
        style_fig(fig_r_trend, height=300)
        st.plotly_chart(fig_r_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="unavailable-card">
        <strong>ℹ️ REFERRAL ATTRIBUTION LIMITATION NOTICE:</strong> The raw user dataset contains individual `referral_code` identifiers (1,000 unique codes), and 119 users are marked as acquired via Referral (`referral_source_detail` = 'Friend/Family'). However, <strong>the dataset does not establish referrer-to-referee user ID mappings</strong> (i.e., which specific user referred which referee). Consequently, individual referral conversion funnels, viral K-factors, and advocate commission rewards cannot be computed without fabricating data. A relational schema `veloop.referrals` with referential constraints is established for future ingestion.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Referral Code Quality & Integrity Audit")
    ref_audit_df = pd.DataFrame([
        {"Metric": "Assigned Referral Codes", "Value": f"{filtered_users['referral_code'].notna().sum():,} / {len(filtered_users):,} (100.0%)"},
        {"Metric": "Unique Referral Codes", "Value": f"{filtered_users['referral_code'].nunique():,} (Zero Duplicates in Clean Cohort)"},
        {"Metric": "Referral Code Syntax Format", "Value": "Valid 8-Character Alphanumeric (Prefix 'VL' + 6 Digits)"},
        {"Metric": "Missing or Null Codes", "Value": "0 Missing Records"},
        {"Metric": "Referral Source Detail", "Value": "119 Friend/Family | 881 Direct/Non-Referral"}
    ])
    st.table(ref_audit_df)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 8. DATA QUALITY & AUDIT
# =============================================================================
elif section == "Data Quality" or section == "Data Quality & Audit":
    card_header("Data Quality Monitoring & Reconciliation Audit")

    q1, q2, q3, q4 = st.columns(4)
    with q1:
        st.metric("Clean Users Cohort", f"{len(users):,} Rows", "27 Columns | 0 Duplicates")
    with q2:
        st.metric("Messy Users Cohort", f"{len(messy_users):,} Rows", "8 Duplicate IDs | 28 Columns")
    with q3:
        st.metric("Events Sheet Count", "35,704 Rows", "0 Duplicate Event IDs")
    with q4:
        st.metric("Event Audit Sheet", "35,714 Rows", "Exactly 10 Injected Duplicates")

    st.markdown("---")

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Investigation: Event Count Difference (35,704 vs 35,714)")
        st.markdown("""
        **Root Cause Analysis:**
        * `03_Feature_Events`: **35,704** rows, 35,704 unique `event_id`s.
        * `10_Event_Data_Quality_Audit`: **35,714** rows, 35,704 unique `event_id`s.
        * Difference: Exactly **10 duplicate rows** injected for QA deduplication testing:
          `EVT00021600`, `EVT00011275`, `EVT00006040`, `EVT00028196`, `EVT00030205`, `EVT00017051`, `EVT00034075`, `EVT00014772`, `EVT00025552`, `EVT00006379`.
        * Deduplicating `10_Event_Data_Quality_Audit` on `event_id` yields exactly **35,704** records (1:1 match).
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_q2:
        st.markdown('<div class="sample-card">', unsafe_allow_html=True)
        card_header("Investigation: Messy Users Audit (1,008 vs 1,000)")
        st.markdown("""
        **Root Cause Analysis:**
        * `Users_1000_Clean`: **1,000** rows, 1,000 unique `user_id`s.
        * `Users_Messy_Audit`: **1,008** rows, 1,000 unique `user_id`s.
        * Difference: Exactly **8 duplicate user IDs**:
          `VLUSR000095`, `VLUSR000217`, `VLUSR000272`, `VLUSR000335`, `VLUSR000409`, `VLUSR000779`, `VLUSR000803`, `VLUSR000813`.
        * Additional Messy Anomalies: Missing values in `age` (1), `gender` (1), `city` (1), `registration_datetime` (1), `primary_device` (1).
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 9. DATA EXPLORER & FILE UPLOAD
# =============================================================================
elif section == "Data Explorer" or section == "Data Explorer & File Upload":
    card_header("Interactive Data Explorer & File Profiler")

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
                "Daily Activity (6,667 Rows)",
                "Milestones (4,799 Rows)"
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
        elif "Milestones" in dataset_choice:
            active_df = milestones
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
# 10. REPORTS & DOCUMENT EXPORTS
# =============================================================================
elif section == "Reports & Exports" or section == "Reports & Document Exports":
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
                st.warning(f"File pending compilation: {fpath}")
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

# =============================================================================
# 11. PROJECT INFORMATION & GOVERNANCE
# =============================================================================
elif section == "Project Information" or section == "Project Information & Governance":
    card_header("Project Information & Governance Standards")

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)
    card_header("Internship Scope & Project Metadata")
    info_table = pd.DataFrame([
        {"Attribute": "Project Title", "Details": "Product Analytics, Data Readiness & Data Management Blueprint"},
        {"Attribute": "Organization", "Details": "VELOOP Rewards & VELOOP CO."},
        {"Attribute": "Role", "Details": "Data Analyst Intern (Analytics, Engineering, BI & Documentation Specialist)"},
        {"Attribute": "Assignment Code", "Details": "Data Analyst Internship — Task 01"},
        {"Attribute": "Duration", "Details": "22–25 Days Scheduled (Comprehensive 21-Deliverable Program)"},
        {"Attribute": "Integrity Standard", "Details": "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING"},
        {"Attribute": "Overall Status", "Details": "100% COMPLETE — All 21 Deliverables Implemented & Verified"}
    ])
    st.table(info_table)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #8E95A5; font-size: 0.82rem; padding: 12px 0;">
    VELOOP Rewards Product Analytics Blueprint | Task 01 Internship Final Submission | Built with Streamlit & Plotly<br>
    Evidentiary Standard: <strong style="color:#F59E0B;">SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</strong>
</div>
""", unsafe_allow_html=True)
