"""
VELOOP REWARDS — PRODUCT ANALYTICS & BI DASHBOARD
Deliverable 14 | Functional 7-Section Interactive Executive Analytics Dashboard
Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="VELOOP Rewards | Product Analytics Blueprint",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Corporate Navy / Teal Palette
st.markdown("""
<style>
    .main-header {
        background-color: #1B365D;
        padding: 18px 24px;
        border-radius: 8px;
        color: white;
        margin-bottom: 20px;
    }
    .disclaimer-banner {
        background-color: #FFF3CD;
        border-left: 6px solid #856404;
        padding: 10px 16px;
        margin-bottom: 20px;
        border-radius: 4px;
        color: #856404;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .metric-card {
        background-color: #F8F9FA;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px 18px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING (CACHED)
# -----------------------------------------------------------------------------
@st.cache_data
def load_dashboard_data():
    f_users = "Data/VELoop_Rewards_Data_01.xlsx"
    f_behavior = "Data/VELOOP_Simulated_User_Behavior_1000.xlsx"
    
    users_df = pd.read_excel(f_users, sheet_name="Users_1000_Clean")
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

    return users_df, sessions_df, events_df, daily_df, tasks_df, feature_df

users, sessions, events, daily, tasks, features = load_dashboard_data()

# -----------------------------------------------------------------------------
# SIDEBAR FILTERS & CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.image("https://via.placeholder.com/260x80/1B365D/FFFFFF?text=VELOOP+REWARDS", use_container_width=True)
st.sidebar.markdown("### 🎛️ Analytics Navigation")

section = st.sidebar.radio(
    "Select Dashboard Section:",
    [
        "1. Executive Overview",
        "2. User & Account Analytics",
        "3. Engagement & Behavioral",
        "4. Earning & Reward Analytics",
        "5. Wallet Intelligence",
        "6. Withdrawal Operations",
        "7. Referral & Viral Growth"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Global Date Filters")
min_date = daily["activity_date"].min().date()
max_date = daily["activity_date"].max().date()
date_range = st.sidebar.date_input("Date Interval", [min_date, max_date], min_value=min_date, max_value=max_date)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📱 Platform Filter")
selected_platforms = st.sidebar.multiselect(
    "Select Platform:",
    options=users["platform"].unique(),
    default=users["platform"].unique()
)

# -----------------------------------------------------------------------------
# MAIN HEADER & DISCLAIMER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size: 1.8rem;">VELOOP REWARDS — PRODUCT ANALYTICS BLUEPRINT</h1>
    <p style="margin:4px 0 0 0; opacity: 0.85; font-size: 0.95rem;">
        Task 01 Data Analyst Internship | Product Management & Executive Reporting Suite
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-banner">
    ⚠️ <strong>SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</strong><br>
    VELOOP is a developing product. The metrics displayed below are derived from fictional/simulated test datasets to evaluate analytical architectures and do not represent actual company performance, users, or revenue.
</div>
""", unsafe_allow_html=True)

# Filtered data views
if len(date_range) == 2:
    start_d, end_d = date_range
    filtered_daily = daily[(daily["activity_date"].dt.date >= start_d) & (daily["activity_date"].dt.date <= end_d)]
else:
    filtered_daily = daily

filtered_users = users[users["platform"].isin(selected_platforms)]

# =============================================================================
# 1. EXECUTIVE OVERVIEW
# =============================================================================
if section == "1. Executive Overview":
    st.subheader("📊 Executive Overview & North Star Metrics")
    
    # KPI Summary Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total User Profiles", f"{len(filtered_users):,}", "Simulated Base")
    with col2:
        mean_dau = filtered_daily.groupby("activity_date")["user_id"].nunique().mean()
        st.metric("Average Daily Active Users (DAU)", f"{mean_dau:.0f}", "Qualifying actions")
    with col3:
        st.metric("Total Sessions", f"{len(sessions):,}", "Web & Mobile")
    with col4:
        task_comp_rate = (len(tasks[tasks["task_status"] == "Completed"]) / len(tasks)) * 100
        st.metric("Task Completion Rate", f"{task_comp_rate:.1f}%", f"{len(tasks):,} Total Tasks")
    with col5:
        total_xp = filtered_users["xp_balance"].sum()
        st.metric("Circulating XP Liability", f"{total_xp:,} XP", "Outstanding balance")

    st.markdown("---")

    # Main Executive Charts
    c1, c2 = st.columns([7, 5])
    with c1:
        st.markdown("#### 📈 Daily Active Users (DAU) & Event Velocity Trend")
        dau_trend = filtered_daily.groupby("activity_date").agg(
            dau=("user_id", "nunique"),
            total_events=("event_count", "sum")
        ).reset_index()
        
        fig_dau = px.line(
            dau_trend, x="activity_date", y="dau",
            title="Daily Active Users (DAU) Over Time [Simulated Sample]",
            labels={"activity_date": "Calendar Date", "dau": "Unique Active Users"},
            color_discrete_sequence=["#1B365D"]
        )
        fig_dau.update_layout(hovermode="x unified", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_dau, use_container_width=True)

    with c2:
        st.markdown("#### 🎯 Feature Engagement Share")
        fig_feat = px.pie(
            features, values="total_events", names="feature_name",
            title="Event Distribution Across 15 Core Features",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_feat.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_feat, use_container_width=True)

    # Secondary Executive Insights
    e1, e2 = st.columns(2)
    with e1:
        st.markdown("#### 📱 Platform & Verification Split")
        verif_summary = filtered_users.groupby(["platform", "email_verification_status"]).size().reset_index(name="count")
        fig_verif = px.bar(
            verif_summary, x="platform", y="count", color="email_verification_status",
            barmode="group",
            title="User Verification by Operating Platform",
            color_discrete_map={"Verified": "#2E7D32", "Pending": "#ED6C02", "Failed": "#D32F2F"}
        )
        st.plotly_chart(fig_verif, use_container_width=True)

    with e2:
        st.markdown("#### ⚙️ Task Execution Status Funnel")
        status_counts = tasks["task_status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig_status = px.bar(
            status_counts, x="Status", y="Count", color="Status",
            title="Earning Task Execution Outcomes (9,846 Attempts)",
            color_discrete_map={"Completed": "#2E7D32", "Abandoned": "#ED6C02", "Failed": "#D32F2F", "Pending": "#0288D1"}
        )
        st.plotly_chart(fig_status, use_container_width=True)

# =============================================================================
# 2. USER & ACCOUNT ANALYTICS
# =============================================================================
elif section == "2. User & Account Analytics":
    st.subheader("👥 User Demographics & Account Lifecycle Intelligence")

    u1, u2, u3, u4 = st.columns(4)
    with u1:
        st.metric("30-Day Active Users", f"{len(filtered_users[filtered_users['is_active_30d'] == 'Yes']):,}", "32.5% of Base")
    with u2:
        st.metric("7-Day Active Users", f"{len(filtered_users[filtered_users['is_active_7d'] == 'Yes']):,}", "7.8% of Base")
    with u3:
        st.metric("Onboarding Completed", f"{len(filtered_users[filtered_users['onboarding_status'] == 'Completed']):,}", "72.2% Conversion")
    with u4:
        st.metric("Suspended Accounts", f"{len(filtered_users[filtered_users['account_status'] == 'Suspended']):,}", "Anti-Fraud Triggers")

    st.markdown("---")
    
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        st.markdown("#### 🌐 Acquisition Channel Breakdown")
        acq_counts = filtered_users["acquisition_source"].value_counts().reset_index()
        acq_counts.columns = ["Channel", "Users"]
        fig_acq = px.bar(
            acq_counts, x="Channel", y="Users", color="Channel",
            title="User Acquisition Source Distribution",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_acq, use_container_width=True)

    with col_u2:
        st.markdown("#### 🎂 User Age Distribution by Gender")
        fig_age = px.histogram(
            filtered_users.dropna(subset=["age"]), x="age", color="gender",
            nbins=20, barmode="overlay", opacity=0.75,
            title="Demographic Age Pyramid (Self-Reported)",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_age, use_container_width=True)

    st.markdown("#### 🗺️ Geographic Distribution (Top States in India)")
    state_counts = filtered_users["state"].value_counts().head(10).reset_index()
    state_counts.columns = ["State", "User Count"]
    fig_state = px.bar(
        state_counts, x="State", y="User Count",
        title="Top 10 States by Simulated User Registrations",
        color="User Count", color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_state, use_container_width=True)

# =============================================================================
# 3. ENGAGEMENT & BEHAVIORAL
# =============================================================================
elif section == "3. Engagement & Behavioral":
    st.subheader("⚡ Engagement Depth & Feature Stickiness")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Mean Session Duration", f"{sessions['session_duration_seconds'].mean():.1f} sec", "Median: 45 sec")
    with m2:
        st.metric("Total Feature Events", f"{len(events):,}", "Across 15 Features")
    with m3:
        st.metric("Avg Daily Events per Active User", f"{(len(events)/len(daily)):.1f}", "Telemetry Density")

    st.markdown("---")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown("#### 🏆 Feature Adoption Ranking (Unique Users)")
        sorted_features = features.sort_values(by="unique_users", ascending=True)
        fig_f_adopt = px.bar(
            sorted_features, y="feature_name", x="unique_users", orientation="h",
            title="Feature Adoption Ranking (Out of 1,000 Users)",
            color="unique_users", color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_f_adopt, use_container_width=True)

    with col_e2:
        st.markdown("#### ⏱️ Session Duration Distribution")
        fig_dur = px.histogram(
            sessions, x="session_duration_seconds", nbins=30,
            title="Session Length Histogram (Seconds)",
            color_discrete_sequence=["#008080"]
        )
        st.plotly_chart(fig_dur, use_container_width=True)

    st.markdown("#### 🚪 App Entry Points vs Exit Features")
    c_entry, c_exit = st.columns(2)
    with c_entry:
        fig_ent = px.pie(sessions, names="entry_point", title="Session Entry Points", hole=0.4)
        st.plotly_chart(fig_ent, use_container_width=True)
    with c_exit:
        fig_ex = px.pie(sessions, names="exit_feature", title="Session Exit Points (Drop-offs)", hole=0.4)
        st.plotly_chart(fig_ex, use_container_width=True)

# =============================================================================
# 4. EARNING & REWARD ANALYTICS
# =============================================================================
elif section == "4. Earning & Reward Analytics":
    st.subheader("💎 Earning Tasks & Reward Fulfillment Engine")

    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.metric("Completed Tasks", f"{len(tasks[tasks['task_status'] == 'Completed']):,}", "57.1% Success Rate")
    with t2:
        st.metric("Abandoned Tasks", f"{len(tasks[tasks['task_status'] == 'Abandoned']):,}", "20.8% Drop-off")
    with t3:
        st.metric("Failed Tasks", f"{len(tasks[tasks['task_status'] == 'Failed']):,}", "15.4% Technical Fault")
    with t4:
        st.metric("Credited Rewards", f"{len(tasks[tasks['reward_status'] == 'Credited']):,}", "100% of Completed")

    st.markdown("---")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("#### 📂 Task Activity Volume by Category")
        cat_counts = tasks["task_category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Volume"]
        fig_cat = px.bar(
            cat_counts, x="Category", y="Volume", color="Category",
            title="Task Activity Distribution Across 8 Categories",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_t2:
        st.markdown("#### 🚨 Failure Root Cause Breakdown")
        fail_reasons = tasks["failure_reason"].dropna().value_counts().reset_index()
        fail_reasons.columns = ["Failure Reason", "Occurrences"]
        fig_fail = px.pie(
            fail_reasons, names="Failure Reason", values="Occurrences",
            title="Primary Causes of Uncompleted Tasks",
            hole=0.4, color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig_fail, use_container_width=True)

    st.markdown("#### 🎯 Completion Rate by Task Category")
    cat_summary = tasks.groupby("task_category")["task_status"].apply(lambda s: (s == "Completed").mean() * 100).reset_index()
    cat_summary.columns = ["Category", "Completion Rate (%)"]
    fig_comp = px.bar(
        cat_summary.sort_values(by="Completion Rate (%)", ascending=False),
        x="Category", y="Completion Rate (%)", color="Completion Rate (%)",
        color_continuous_scale="Tealgrn"
    )
    st.plotly_chart(fig_comp, use_container_width=True)

# =============================================================================
# 5. WALLET INTELLIGENCE
# =============================================================================
elif section == "5. Wallet Intelligence":
    st.subheader("💰 User Balances & Currency Flow Intelligence")

    w1, w2, w3 = st.columns(3)
    with w1:
        st.metric("Total Outstanding XP", f"{users['xp_balance'].sum():,} XP", "1,000 Users")
    with w2:
        st.metric("Mean Balance per User", f"{users['xp_balance'].mean():.1f} XP", "Median: 120 XP")
    with w3:
        st.metric("Max User Balance", f"{users['xp_balance'].max():,} XP", "Whale Earner")

    st.markdown("---")

    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown("#### 📊 User XP Balance Histogram")
        fig_xp = px.histogram(
            users, x="xp_balance", nbins=25,
            title="Distribution of User XP Balances",
            color_discrete_sequence=["#1B365D"]
        )
        st.plotly_chart(fig_xp, use_container_width=True)

    with col_w2:
        st.markdown("#### 📈 XP Balance vs Account Tenure (Active Days)")
        fig_scatter = px.scatter(
            users, x="active_days", y="xp_balance", color="account_status",
            title="XP Accumulation vs Active Days",
            color_discrete_map={"Active": "#2E7D32", "Inactive": "#9E9E9E", "Suspended": "#D32F2F"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.info("💡 **Proposed Architecture Note:** The platform data model specifies expanding the current single `xp_balance` into three segregated currency ledgers: `XP` (Experience), `GEMS` (Premium Hard Currency), and `TOKENS` (Cash-redeemable asset).")

# =============================================================================
# 6. WITHDRAWAL OPERATIONS
# =============================================================================
elif section == "6. Withdrawal Operations":
    st.subheader("💳 Withdrawal Operations & Payout Queue Model")
    
    st.markdown("""
    <div style="background-color: #E8F4FD; border-left: 6px solid #0288D1; padding: 10px; margin-bottom: 15px; border-radius: 4px; color: #01579B;">
        ℹ️ <strong>OPERATIONAL MODEL NOTICE:</strong> As identified in Work Package A & J, standalone withdrawal transaction records were not supplied in the raw files. The visual below demonstrates the <strong>Work Package D proposed withdrawal pipeline</strong> based on simulated operational parameters (~1,200 requests).
    </div>
    """, unsafe_allow_html=True)

    # Simulated Withdrawal Model for Demonstration
    wd_methods = ["UPI", "Paytm", "Bank Transfer", "PayPal"]
    wd_statuses = ["Completed", "Under_Review", "Processing", "Rejected", "Reversed"]
    
    col_wd1, col_wd2 = st.columns(2)
    with col_wd1:
        st.markdown("#### 📲 Withdrawal Volume by Payment Rail")
        method_shares = pd.DataFrame({"Payment Rail": wd_methods, "Volume (INR)": [350000, 180000, 95000, 45000]})
        fig_m = px.pie(method_shares, names="Payment Rail", values="Volume (INR)", hole=0.45, title="Payout Rail Share (Proposed Model)")
        st.plotly_chart(fig_m, use_container_width=True)

    with col_wd2:
        st.markdown("#### 🚦 Payout Status Queue Breakdown")
        status_shares = pd.DataFrame({"Status": wd_statuses, "Requests": [980, 85, 55, 60, 20]})
        fig_st = px.bar(status_shares, x="Status", y="Requests", color="Status", title="Simulated 1,200 Withdrawal Request Pipeline")
        st.plotly_chart(fig_st, use_container_width=True)

    st.markdown("#### ⏱️ Payout Fulfillment Latency SLA (Target < 24h)")
    st.success("Target Fulfillment SLA: 92% of verified withdrawals settled within 12 hours.")

# =============================================================================
# 7. REFERRAL & VIRAL GROWTH
# =============================================================================
elif section == "7. Referral & Viral Growth":
    st.subheader("🚀 Viral Growth & Referral Attribution Analytics")

    st.markdown("""
    <div style="background-color: #E8F4FD; border-left: 6px solid #0288D1; padding: 10px; margin-bottom: 15px; border-radius: 4px; color: #01579B;">
        ℹ️ <strong>ATTRIBUTION ARCHITECTURE NOTICE:</strong> As identified in Work Package A & J, the raw files capture outbound referral shares (`referral_shared: 834`), but lack referee-to-referrer database keys. The views below illustrate the <strong>Work Package E 4-stage referral funnel</strong>.
    </div>
    """, unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric("Referrals Created", "871", "In-App Codes")
    with r2:
        st.metric("Invites Shared", "834", "WhatsApp / Telegram")
    with r3:
        st.metric("Referee Registrations", "119", "Attributed Signups")
    with r4:
        st.metric("Viral Coefficient (K)", "0.14", "Sub-viral (< 1.0)")

    st.markdown("---")

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("#### 📣 Referral Outbound Sharing by Channel")
        ref_channels = pd.DataFrame({
            "Channel": ["WhatsApp", "Telegram", "Instagram", "Direct Link", "YouTube"],
            "Shares": [485, 185, 95, 45, 24]
        })
        fig_rch = px.bar(ref_channels, x="Channel", y="Shares", color="Channel", title="Invites Shared by Social Channel")
        st.plotly_chart(fig_rch, use_container_width=True)

    with col_r2:
        st.markdown("#### 🎯 4-Stage Referral Conversion Funnel")
        funnel_df = pd.DataFrame({
            "Stage": ["1. Referral Created", "2. Invite Shared", "3. User Registered", "4. User Activated & Converted"],
            "Users": [871, 834, 119, 78]
        })
        fig_fun = px.funnel(funnel_df, y="Stage", x="Users", title="Referral Conversion Drop-off")
        st.plotly_chart(fig_fun, use_container_width=True)

