"""
VELOOP REWARDS — PRODUCT ANALYTICS & BI DASHBOARD

Theme:
Enterprise Blue — Corporate Business Intelligence

Data policy:
SIMULATED DATA — CREATED FOR ANALYTICAL TESTING

Database:
PostgreSQL first, CSV / Excel fallback
"""

# ============================================================
# 1. IMPORTS
# ============================================================

import os
import sys
import io
import warnings

from pathlib import Path
from datetime import datetime, date

import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings("ignore", category=FutureWarning)


# ============================================================
# 2. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DASHBOARD_DIR = Path(__file__).resolve().parent

PROCESSED_DIR = PROJECT_ROOT / "02_processed_data"

REPORTS_DIR = PROJECT_ROOT / "06_documentation_and_reports"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# 3. DATABASE IMPORT
# ============================================================

DB_AVAILABLE = False
DB_IMPORT_ERROR = None

try:
    import db
    DB_AVAILABLE = True

except Exception as exc:
    DB_IMPORT_ERROR = str(exc)
    db = None


# ============================================================
# 4. STREAMLIT CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VELOOP Rewards Analytics",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 5. COLOR PALETTE
# ============================================================

COLORS = {
    "background": "#F3F6FB",
    "sidebar": "#142B4A",
    "card": "#FFFFFF",
    "card_secondary": "#EAF1FA",
    "border": "#DCE5F0",
    "primary": "#2463A6",
    "cyan": "#1596C5",
    "green": "#23845B",
    "yellow": "#C58A22",
    "red": "#C94F55",
    "purple": "#7866B2",
    "pink": "#B45E91",
    "text": "#172B45",
    "muted": "#66788F",
    "white": "#FFFFFF"
}

# ============================================================
# 6. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp { background: #F3F6FB; color: #172B45; }
    [data-testid="stHeader"] { background: rgba(243,246,251,.96); }
    [data-testid="stSidebar"] { background: #142B4A; border-right: 1px solid #233F61; }
    [data-testid="stSidebar"] > div, [data-testid="stSidebarContent"] { background: #142B4A; }
    [data-testid="stSidebar"] * { color: #EAF2FC; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label { padding: 7px 10px; border-radius: 8px; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background: #24466D; }
    [data-testid="stMetric"] {
        background: #FFFFFF; border: 1px solid #DCE5F0; border-radius: 14px;
        padding: 18px 20px; box-shadow: 0 3px 12px rgba(24,53,85,.055);
    }
    [data-testid="stMetricLabel"] { color: #66788F; font-size: 12px; font-weight: 700; }
    [data-testid="stMetricValue"] { color: #172B45; font-size: 28px; font-weight: 800; }
    [data-testid="stMetricDelta"] { font-size: 12px; }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF; border: 1px solid #DCE5F0; border-radius: 14px;
        box-shadow: 0 3px 12px rgba(24,53,85,.04);
    }
    .main-title { font-size: 30px; font-weight: 800; color: #172B45; margin-bottom: 4px; letter-spacing: -.6px; }
    .main-subtitle { font-size: 13px; color: #66788F; margin-bottom: 20px; }
    .section-title { font-size: 20px; font-weight: 750; color: #172B45; margin: 16px 0 12px; }
    .card-header { font-size: 15px; font-weight: 700; color: #203B5C; padding-bottom: 10px; border-bottom: 1px solid #E5EBF3; margin-bottom: 14px; }
    .notice, .warning-notice, .success-notice, .data-notice { border-radius: 10px; padding: 13px 16px; font-size: 13px; margin: 12px 0; }
    .notice { background: #EAF2FC; border: 1px solid #C9DCF3; color: #24466D; }
    .warning-notice { background: #FFF6E5; border: 1px solid #F0D69C; color: #805B16; }
    .success-notice { background: #EAF7F0; border: 1px solid #BFE3CE; color: #216344; }
    .data-notice { background: #FFF4E9; border: 1px solid #F0D0B1; color: #87502A; font-weight: 700; }
    .sidebar-brand { font-size: 23px; font-weight: 800; color: #FFFFFF; padding: 12px 0 3px; letter-spacing: -.5px; }
    .sidebar-caption { color: #B8CBE0; font-size: 10px; letter-spacing: 1.1px; margin-bottom: 20px; }
    .small-muted { color: #66788F; font-size: 12px; }
    .stButton > button { background: #2463A6; color: #FFFFFF; border: 1px solid #2463A6; border-radius: 9px; font-weight: 650; }
    .stButton > button:hover { background: #174E88; border-color: #174E88; color: #FFFFFF; }
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stDateInput input,
    .stMultiSelect div[data-baseweb="select"] { background: #FFFFFF; color: #172B45; border-color: #CBD7E5; }
    [data-testid="stDataFrame"] { border: 1px solid #DCE5F0; border-radius: 10px; }
    h1, h2, h3, h4, h5 { color: #172B45; }
    p, label { color: #43566E; }
    hr { border-color: #DCE5F0; }
    [data-testid="stExpander"] { background: #FFFFFF; border: 1px solid #DCE5F0; border-radius: 10px; }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 7. GENERAL HELPER FUNCTIONS
# ============================================================

def safe_number(value, default=0):
    """Convert a value to a safe numeric value."""

    try:
        result = pd.to_numeric(value, errors="coerce")

        if pd.isna(result):
            return default

        return float(result)

    except Exception:
        return default


def safe_percent(numerator, denominator):
    """Calculate percentage safely."""

    numerator = safe_number(numerator)
    denominator = safe_number(denominator)

    if denominator == 0:
        return 0.0

    return (numerator / denominator) * 100


def safe_mean(series):
    """Calculate mean safely."""

    if series is None or len(series) == 0:
        return 0.0

    values = pd.to_numeric(series, errors="coerce").dropna()

    if values.empty:
        return 0.0

    return float(values.mean())


def safe_median(series):
    """Calculate median safely."""

    if series is None or len(series) == 0:
        return 0.0

    values = pd.to_numeric(series, errors="coerce").dropna()

    if values.empty:
        return 0.0

    return float(values.median())


def ensure_columns(df, defaults):
    """
    Add missing columns without overwriting existing data.
    """

    if df is None:
        df = pd.DataFrame()

    df = df.copy()

    for column, default_value in defaults.items():

        if column not in df.columns:
            df[column] = default_value

    return df


def normalize_datetime(df, columns):
    """Convert available columns to datetime safely."""

    if df is None:
        return pd.DataFrame()

    df = df.copy()

    for column in columns:

        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    return df


def empty_frame(columns=None):
    """Create an empty DataFrame with optional columns."""

    if columns is None:
        return pd.DataFrame()

    return pd.DataFrame(columns=columns)


def style_fig(fig, height=350):
    """Apply common dashboard chart styling."""

    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter",
            color=COLORS["text"],
            size=11
        ),
        margin=dict(
            l=15,
            r=15,
            t=35,
            b=15
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS["muted"])
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            color=COLORS["muted"]
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E5EBF3",
            zeroline=False,
            color=COLORS["muted"]
        )
    )

    return fig


def card_header(title):
    """Display a consistent card heading."""

    st.markdown(
        f'<div class="card-header">{title}</div>',
        unsafe_allow_html=True
    )


def show_chart_or_empty(fig, df, message="No data available for the selected filters."):
    """Display a chart or a friendly empty-state message."""

    if df is None or df.empty:
        st.info(message)
    else:
        st.plotly_chart(
            style_fig(fig),
            use_container_width=True
        )


def show_notice(message, notice_type="info"):
    """Display styled notices."""

    class_name = {
        "info": "notice",
        "warning": "warning-notice",
        "success": "success-notice",
        "data": "data-notice"
    }.get(notice_type, "notice")

    st.markdown(
        f'<div class="{class_name}">{message}</div>',
        unsafe_allow_html=True
    )


def safe_sum(df, column):
    """Safely calculate a numeric column sum."""

    if df is None or df.empty or column not in df.columns:
        return 0.0

    return safe_number(
        pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0).sum()
    )


def safe_unique(df, column):
    """Count unique non-null values."""

    if df is None or df.empty or column not in df.columns:
        return 0

    return int(df[column].nunique())



def make_hashable(value):
    """Convert nested containers into hashable values for duplicate checks."""
    if isinstance(value, (list, tuple)):
        return tuple(make_hashable(item) for item in value)
    if isinstance(value, dict):
        return tuple(sorted(
            (str(key), make_hashable(item))
            for key, item in value.items()
        ))
    if isinstance(value, set):
        return frozenset(make_hashable(item) for item in value)
    return value

# ============================================================
# 8. DATA LOADING — POSTGRESQL FIRST
# ============================================================

def load_dashboard_data():

    data = {}

    database_connected = False
    database_error = None

    # --------------------------------------------------------
    # 8.1 PostgreSQL loading
    # --------------------------------------------------------
    if DB_AVAILABLE:
        try:
            table_names = [
                "users",
                "sessions",
                "feature_events",
                "daily_activity",
                "wallet_accounts",
                "wallet_ledger",
                "withdrawals",
                "referrals",
                "event_catalog",
                "event_validation_test_log",
                "task_activity",
                "milestones"
            ]

            table_errors = {}
            for table_name in table_names: 
                try:
                    table_data = db.get_table(table_name)
                    if table_data is None:
                        data[table_name] = pd.DataFrame()
                    else:
                        data[table_name] = table_data

                except Exception as table_exc:

                    data[table_name] = pd.DataFrame()
                    table_errors[table_name] = str(table_exc)

            required_tables = [

                "users",
                "sessions",
                "feature_events",
                "daily_activity"
            ]

            missing_required = [
                table
                for table in required_tables
                if data.get(table, pd.DataFrame()).empty
            ]

            if missing_required:

                error_details = []

                for table in missing_required:

                    if table in table_errors:
                        error_details.append(
                        f"{table}: {table_errors[table]}"
                    )
                    else:
                        error_details.append(
                        f"{table}: No records returned"
                    )

            raise RuntimeError(
                "Required PostgreSQL tables could not be loaded. "
                + " | ".join(error_details)
            )

            database_connected = True

            data["tasks"] = data.get(
                "task_activity",
                pd.DataFrame()
            ) .copy()

            data["milestones"] = data.get(
                "milestones",
                pd.DataFrame()
            ).copy()

            data_source = "PostgreSQL"


        except Exception as exc:
            database_error = str(exc)
            database_connected = False

    else:
    

        database_error = (

            DB_IMPORT_ERROR
            or "Database module unavailable."
        )
    
    # --------------------------------------------------------
    # 8.2 CSV / Excel fallback
    # --------------------------------------------------------

    if not database_connected:

        data = {}

        csv_files = {
            "users": ["02_processed_data/users_cleaned.csv", "02_processed_data/users.csv"],
            "sessions": ["02_processed_data/sessions_cleaned.csv", "02_processed_data/sessions.csv"],
            "feature_events": ["02_processed_data/events_cleaned.csv", "02_processed_data/feature_events.csv", "02_processed_data/events.csv"],
            "daily_activity": ["02_processed_data/daily_activity_cleaned.csv", "02_processed_data/daily_activity.csv"],
            "wallet_accounts": ["Wallet & Withdrawal Simulation/wallet_accounts_simulated.csv", "02_processed_data/wallet_accounts.csv"],
            "wallet_ledger": ["Wallet & Withdrawal Simulation/wallet_ledger_simulated.csv", "02_processed_data/wallet_ledger.csv"],
            "withdrawals": ["Wallet & Withdrawal Simulation/withdrawals_simulated.csv", "02_processed_data/withdrawals.csv"],
            "referrals": ["02_processed_data/referrals.csv"],
            "event_catalog": ["02_processed_data/event_catalog.csv"],
            "event_validation_test_log": ["02_processed_data/event_validation_test_log.csv"],
            "tasks": ["02_processed_data/tasks_cleaned.csv", "02_processed_data/task_activity.csv"],
            "milestones": ["02_processed_data/milestones_cleaned.csv", "02_processed_data/milestones.csv"]
        }

        for logical_name, filenames in csv_files.items():

            loaded_df = pd.DataFrame()

            for relative_path in filenames:

                file_path = PROJECT_ROOT / relative_path

                if file_path.exists():

                    try:
                        loaded_df = pd.read_csv(file_path)
                        break

                    except Exception:
                        continue

            data[logical_name] = loaded_df

        # Try source Excel workbooks if processed CSVs are unavailable.

        if data["users"].empty:

            excel_files = list(PROJECT_ROOT.glob("*.xlsx"))

            for excel_path in excel_files:

                try:

                    workbook = pd.ExcelFile(excel_path)

                    for sheet in workbook.sheet_names:

                        sheet_df = pd.read_excel(
                            excel_path,
                            sheet_name=sheet
                        )

                        normalized_name = sheet.lower().replace(" ", "_")

                        if normalized_name in data and data[normalized_name].empty:
                            data[normalized_name] = sheet_df

                except Exception:
                    continue

        data_source = "CSV / Excel fallback"

    # --------------------------------------------------------
    # 8.3 Ensure all expected datasets exist
    # --------------------------------------------------------

    expected_datasets = [
        "users",
        "sessions",
        "feature_events",
        "daily_activity",
        "wallet_accounts",
        "wallet_ledger",
        "withdrawals",
        "referrals",
        "event_catalog",
        "event_validation_test_log",
        "tasks",
        "milestones"
    ]

    for dataset_name in expected_datasets:

        if dataset_name not in data or data[dataset_name] is None:
            data[dataset_name] = pd.DataFrame()

    # --------------------------------------------------------
    # 8.3A Map actual PostgreSQL column names to dashboard aliases
    # --------------------------------------------------------

    # Keep original database columns; add aliases used by charts.
    alias_map = {
        "users": {"primary_device": "device_type"},
        "sessions": {"device": "device_type"},
        "feature_events": {"device": "device_type", "action_type": "event_name"},
        "daily_activity": {"daily_xp_earned": "xp_earned"},
        "tasks": {
            "category": "task_category",
            "task_status": "status",
            "started_datetime": "created_at",
            "completed_datetime": "completed_at"
        }
    }

    for dataset_name, aliases in alias_map.items():
        frame = data.get(dataset_name, pd.DataFrame()).copy()
        for source_column, alias_column in aliases.items():
            if source_column in frame.columns and alias_column not in frame.columns:
                frame[alias_column] = frame[source_column]
        data[dataset_name] = frame

    # --------------------------------------------------------
    # 8.4 Standardize users
    # --------------------------------------------------------

    data["users"] = ensure_columns(
        data["users"],
        {
            "user_id": "",
            "full_name": "",
            "age": np.nan,
            "gender": "Unknown",
            "state": "Unknown",
            "city": "Unknown",
            "primary_device": "Unknown",
            "device_type": "Unknown",
            "xp_balance": 0,
            "acquisition_source": "Unknown",
            "registration_datetime": pd.NaT,
            "account_status": "Unknown"
        }
    )

    # --------------------------------------------------------
    # 8.5 Standardize sessions
    # --------------------------------------------------------

    data["sessions"] = ensure_columns(
        data["sessions"],
        {
            "session_id": "",
            "user_id": "",
            "session_start": pd.NaT,
            "session_end": pd.NaT,
            "session_duration_seconds": 0,
            "device": "Unknown",
            "device_type": "Unknown"
        }
    )

    # --------------------------------------------------------
    # 8.6 Standardize feature events
    # --------------------------------------------------------

    data["feature_events"] = ensure_columns(
        data["feature_events"],
        {
            "event_id": "",
            "user_id": "",
            "event_name": "Unknown",
            "feature_name": "Unknown",
            "event_datetime": pd.NaT,
            "device": "Unknown",
            "device_type": "Unknown",
            "xp_earned": 0
        }
    )

    # --------------------------------------------------------
    # 8.7 Standardize daily activity
    # --------------------------------------------------------

    data["daily_activity"] = ensure_columns(
        data["daily_activity"],
        {
            "user_id": "",
            "activity_date": pd.NaT,
            "tasks_started": 0,
            "tasks_completed": 0,
            "active_flag": "No",
            "wallet_activity": "No",
            "referral_activity": "No",
            "daily_xp_earned": 0,
            "xp_earned": 0
        }
    )

    # --------------------------------------------------------
    # 8.8 Standardize wallet accounts
    # --------------------------------------------------------

    data["wallet_accounts"] = ensure_columns(
        data["wallet_accounts"],
        {
            "user_id": "",
            "opening_balance": 0,
            "current_balance": 0,
            "wallet_status": "Unknown"
        }
    )

    # --------------------------------------------------------
    # 8.9 Standardize wallet ledger
    # --------------------------------------------------------

    data["wallet_ledger"] = ensure_columns(
        data["wallet_ledger"],
        {
            "transaction_id": "",
            "user_id": "",
            "transaction_type": "Unknown",
            "amount": 0,
            "transaction_datetime": pd.NaT,
            "debit": 0,
            "credit": 0
        }
    )

    # --------------------------------------------------------
    # 8.10 Standardize withdrawals
    # --------------------------------------------------------

    data["withdrawals"] = ensure_columns(
        data["withdrawals"],
        {
            "withdrawal_id": "",
            "user_id": "",
            "amount": 0,
            "status": "Unknown",
            "requested_at": pd.NaT,
            "processed_at": pd.NaT
        }
    )

    # --------------------------------------------------------
    # 8.11 Standardize referrals
    # --------------------------------------------------------

    data["referrals"] = ensure_columns(
        data["referrals"],
        {
            "referral_id": "",
            "referrer_user_id": "",
            "referred_user_id": "",
            "referral_status": "Unknown",
            "created_at": pd.NaT
        }
    )

    # --------------------------------------------------------
    # 8.12 Standardize task activity
    # --------------------------------------------------------

    data["tasks"] = ensure_columns(
        data["tasks"],
        {
            "user_id": "",
            "task_category": "Unknown",
            "task_name": "Unknown",
            "category": "Unknown",
            "task_status": "Unknown",
            "status": "Unknown",
            "reward_status": "Unknown",
            "reward_points_allocated": 0,
            "activity_id": "",
            "started_datetime": pd.NaT,
            "completed_datetime": pd.NaT,
            "created_at": pd.NaT,
            "completed_at": pd.NaT,
            "device": "Unknown",
            "xp_earned": 0
        }
    )

    # --------------------------------------------------------
    # 8.13 Standardize milestones
    # --------------------------------------------------------

    data["milestones"] = ensure_columns(
        data["milestones"],
        {
            "user_id": "",
            "milestone_name": "Unknown",
            "milestone_status": "Unknown",
            "achieved_at": pd.NaT
        }
    )

    # --------------------------------------------------------
    # 8.14 Standardize event catalog
    # --------------------------------------------------------

    data["event_catalog"] = ensure_columns(
        data["event_catalog"],
        {
            "event_name": "Unknown",
            "feature_name": "Unknown",
            "description": ""
        }
    )

    # --------------------------------------------------------
    # 8.15 Normalize datetime columns
    # --------------------------------------------------------

    datetime_columns = {
        "users": ["registration_datetime"],
        "sessions": ["session_start", "session_end"],
        "feature_events": ["event_datetime"],
        "daily_activity": ["activity_date"],
        "wallet_ledger": ["transaction_datetime"],
        "withdrawals": ["requested_at", "processed_at"],
        "referrals": ["created_at"],
        "tasks": ["created_at", "completed_at", "started_datetime", "completed_datetime"],
        "milestones": ["achieved_at"]
    }

    for dataset_name, columns in datetime_columns.items():

        data[dataset_name] = normalize_datetime(
            data[dataset_name],
            columns
        )

    # --------------------------------------------------------
    # 8.16 Numeric conversions
    # --------------------------------------------------------

    numeric_columns = {
        "users": ["age", "xp_balance"],
        "sessions": ["session_duration_seconds"],
        "daily_activity": [
            "tasks_started",
            "tasks_completed",
            "daily_xp_earned",
            "xp_earned"
        ],
        "wallet_accounts": [
            "opening_balance",
            "current_balance"
        ],
        "wallet_ledger": [
            "amount",
            "debit",
            "credit"
        ],
        "withdrawals": ["amount"],
        "tasks": ["xp_earned", "reward_points_allocated"],
        "feature_events": ["xp_earned"]
    }

    for dataset_name, columns in numeric_columns.items():

        for column in columns:

            if column in data[dataset_name].columns:

                data[dataset_name][column] = pd.to_numeric(
                    data[dataset_name][column],
                    errors="coerce"
                )

    # --------------------------------------------------------
    # 8.17 Feature aggregation
    # --------------------------------------------------------

    events_df = data["feature_events"]

    if not events_df.empty:

        features_df = (
            events_df
            .groupby(
                ["feature_name"],
                dropna=False
            )
            .agg(
                total_events=("event_name", "count"),
                unique_users=("user_id", "nunique")
            )
            .reset_index()
            .sort_values(
                "total_events",
                ascending=False
            )
        )

    else:

        features_df = pd.DataFrame(
            columns=[
                "feature_name",
                "total_events",
                "unique_users"
            ]
        )

    data["features"] = features_df

    # --------------------------------------------------------
    # 8.18 Return datasets and connection information
    # --------------------------------------------------------

    return {
        **data,
        "data_source": data_source,
        "database_connected": database_connected,
        "database_error": database_error
    }

# ============================================================
# 9. LOAD DASHBOARD DATA
# ============================================================

try:

    dashboard_data = load_dashboard_data()

except Exception as exc:

    st.error(f"Unable to load dashboard data: {exc}")
    st.stop()


# Extract datasets

users_df = dashboard_data["users"]
sessions_df = dashboard_data["sessions"]
events_df = dashboard_data["feature_events"]
daily_df = dashboard_data["daily_activity"]

wallet_accounts_df = dashboard_data["wallet_accounts"]
wallet_ledger_df = dashboard_data["wallet_ledger"]
withdrawals_df = dashboard_data["withdrawals"]

referrals_df = dashboard_data["referrals"]
event_catalog_df = dashboard_data["event_catalog"]
validation_log_df = dashboard_data["event_validation_test_log"]

tasks_df = dashboard_data["tasks"]
milestones_df = dashboard_data["milestones"]

features_df = dashboard_data["features"]

DATA_SOURCE = dashboard_data["data_source"]
DATABASE_CONNECTED = dashboard_data["database_connected"]
DATABASE_ERROR = dashboard_data["database_error"]


# ============================================================
# 10. APPLICATION HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        VELOOP Rewards Analytics
    </div>

    <div class="main-subtitle">
        Product Intelligence Dashboard &nbsp;•&nbsp; User Behaviour &nbsp;•&nbsp; Rewards Analytics
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 11. SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            ⏱️ VELOOP
        </div>

        <div class="sidebar-caption">
            REWARDS ANALYTICS PLATFORM
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    section = st.radio(
        "DASHBOARD NAVIGATION",
        [
            "Overview",
            "User Analytics",
            "Earning & Rewards",
            "Wallet & Withdrawal",
            "Referral & Virality",
            "Feature & Engagement",
            "Data Quality & Audit"
        ],
        index=0,
        key="dashboard_section"
    )

    st.markdown("---")

    st.markdown("### Data Connection")

    if DATABASE_CONNECTED:

        st.success("PostgreSQL Connected")

    else:

        st.warning("CSV / Excel Fallback")

    st.caption(f"Data source: {DATA_SOURCE}")

    if not DATABASE_CONNECTED and DATABASE_ERROR:

        with st.expander("Database connection details"):

            st.code(
                str(DATABASE_ERROR),
                language="text"
            )

    st.markdown("---")

    if st.button(
        "🔄 Refresh Dashboard",
        use_container_width=True
    ):

        st.cache_data.clear()
        st.rerun()

    st.markdown("---")

    st.caption("VELOOP Rewards Analytics")
    st.caption("Product Intelligence Dashboard")


# ============================================================
# 12. DATABASE DIAGNOSTICS
# ============================================================

with st.expander("PostgreSQL connection diagnostics"):

    diagnostic_col1, diagnostic_col2 = st.columns(2)

    with diagnostic_col1:

        st.metric(
            "Connection Status",
            "Connected" if DATABASE_CONNECTED else "Fallback Mode"
        )

    with diagnostic_col2:

        st.metric(
            "Data Source",
            DATA_SOURCE
        )

    if DATABASE_CONNECTED:

        st.success(
            "Dashboard data was successfully loaded from PostgreSQL."
        )

    else:

        st.warning(
            "PostgreSQL data could not be loaded. "
            "The dashboard is using the available CSV / Excel datasets."
        )

        if DATABASE_ERROR:

            st.code(
                str(DATABASE_ERROR),
                language="text"
            )

    st.markdown("#### Dataset availability")

    dataset_status = []

    for dataset_name in [
        "users",
        "sessions",
        "feature_events",
        "daily_activity",
        "wallet_accounts",
        "wallet_ledger",
        "withdrawals",
        "referrals",
        "event_catalog",
        "event_validation_test_log",
        "tasks",
        "milestones"
    ]:

        dataset = dashboard_data.get(
            dataset_name,
            pd.DataFrame()
        )

        dataset_status.append({
            "Dataset": dataset_name,
            "Rows": len(dataset),
            "Columns": len(dataset.columns),
            "Status": "Available" if not dataset.empty else "Empty / Unavailable"
        })

    st.dataframe(
        pd.DataFrame(dataset_status),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 13. GLOBAL FILTERS
# ============================================================

st.markdown("### Dashboard Filters")
st.caption("Refine the reporting cohort by activity period, device telemetry and keyword.")

filter_col1, filter_col2, filter_col3 = st.columns(
    [1.5, 1.2, 1.5]
)


# ------------------------------------------------------------
# 13.1 Date filter
# ------------------------------------------------------------

available_dates = []

for dataset, date_column in [
    (daily_df, "activity_date"),
    (events_df, "event_datetime"),
    (sessions_df, "session_start"),
    (tasks_df, "created_at")
]:

    if (
        dataset is not None
        and not dataset.empty
        and date_column in dataset.columns
    ):

        valid_dates = pd.to_datetime(
            dataset[date_column],
            errors="coerce"
        ).dropna()

        if not valid_dates.empty:

            available_dates.extend(
                valid_dates.dt.date.tolist()
            )


if available_dates:

    minimum_date = min(available_dates)
    maximum_date = max(available_dates)

else:

    minimum_date = date.today()
    maximum_date = date.today()


with filter_col1:

    date_range = st.date_input(
        "📅 Activity Date Range",
        value=(
            minimum_date,
            maximum_date
        ),
        min_value=minimum_date,
        max_value=maximum_date,
        key="dashboard_date_range"
    )


# ------------------------------------------------------------
# 13.2 Device filter
# ------------------------------------------------------------

device_values = set()

# Users table uses primary_device
if (
    users_df is not None
    and not users_df.empty
    and "primary_device" in users_df.columns
):
    device_values.update(
        users_df["primary_device"]
        .dropna()
        .astype(str)
        .unique()
    )

# Sessions table uses device
if (
    sessions_df is not None
    and not sessions_df.empty
    and "device" in sessions_df.columns
):
    device_values.update(
        sessions_df["device"]
        .dropna()
        .astype(str)
        .unique()
    )

# Feature Events table uses device
if (
    events_df is not None
    and not events_df.empty
    and "device" in events_df.columns
):
    device_values.update(
        events_df["device"]
        .dropna()
        .astype(str)
        .unique()
    )

device_options = sorted(
    value for value in device_values
    if value.strip() and value.lower() != "nan"
)

device_options = sorted(
    [
        value
        for value in device_values
        if value.strip() and value.lower() != "nan"
    ]
)


with filter_col2:

    selected_devices = st.multiselect(
        "📱 Device Telemetry",
        options=device_options,
        default=device_options,
        key="dashboard_device_filter"
    )


# ------------------------------------------------------------
# 13.3 Search filter
# ------------------------------------------------------------

with filter_col3:

    search_query = st.text_input(
        "🔍 Search Features / Events",
        placeholder="Search metrics or events...",
        key="dashboard_search"
    )


st.caption(
    "The date range filters activity records. "
    "Registration-based user metrics use the available user cohort."
)


# ============================================================
# 14. APPLY GLOBAL FILTERS
# ============================================================

def filter_by_date(df, date_column, start_date, end_date):

    if df is None:
        return pd.DataFrame()

    if df.empty:
        return df.copy()

    if date_column not in df.columns:
        return df.copy()

    result = df.copy()

    dates = pd.to_datetime(
        result[date_column],
        errors="coerce",
        utc=True
    ).dt.tz_convert(None)

    start_timestamp = pd.Timestamp(start_date).normalize()

    end_timestamp = (
        pd.Timestamp(end_date).normalize()
        + pd.Timedelta(days=1)
    )

    mask = (
        dates.notna()
        & (dates >= start_timestamp)
        & (dates < end_timestamp)
    )

    return result.loc[mask].copy()


def filter_by_device(df, selected_device_values, device_column="device"):

    if df is None or df.empty:
        return pd.DataFrame() if df is None else df.copy()

    if not selected_device_values:
        return df.copy()

    if device_column not in df.columns:
        return df.copy()

    return df[
        df[device_column]
        .astype(str)
        .isin(selected_device_values)
    ].copy()

# Resolve date selection safely.

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:

    start_date = date_range[0]
    end_date = date_range[1]

else:

    start_date = date_range
    end_date = date_range


# Filter activity datasets.

filtered_daily = filter_by_date(
    daily_df,
    "activity_date",
    start_date,
    end_date
)

filtered_events = filter_by_date(
    events_df,
    "event_datetime",
    start_date,
    end_date
)

filtered_sessions = filter_by_date(
    sessions_df,
    "session_start",
    start_date,
    end_date
)

filtered_tasks = filter_by_date(
    tasks_df,
    "created_at",
    start_date,
    end_date
)

filtered_wallet_ledger = filter_by_date(
    wallet_ledger_df,
    "transaction_datetime",
    start_date,
    end_date
)

filtered_withdrawals = filter_by_date(
    withdrawals_df,
    "requested_at",
    start_date,
    end_date
)

filtered_referrals = filter_by_date(
    referrals_df,
    "created_at",
    start_date,
    end_date
)

# Shared aliases used by the Data Quality and Audit section.
filtered_daily_activity = filtered_daily.copy()
event_validation_df = validation_log_df.copy()


# Apply device filtering

filtered_users = filter_by_device(
    users_df,
    selected_devices,
    "primary_device"
)

filtered_sessions = filter_by_device(
    filtered_sessions,
    selected_devices,
    "device"
)

filtered_events = filter_by_device(
    filtered_events,
    selected_devices,
    "device"
)

filtered_tasks = filter_by_device(
    filtered_tasks,
    selected_devices,
    "device"
)


# ------------------------------------------------------------
# Search feature and event names
# ------------------------------------------------------------

if search_query.strip():

    search_text = search_query.strip().lower()

    event_mask = (
        filtered_events["event_name"]
        .astype(str)
        .str.lower()
        .str.contains(search_text, na=False)
        |
        filtered_events["feature_name"]
        .astype(str)
        .str.lower()
        .str.contains(search_text, na=False)
    )

    filtered_events = filtered_events[
        event_mask
    ].copy()

    feature_mask = (
        features_df["feature_name"]
        .astype(str)
        .str.lower()
        .str.contains(search_text, na=False)
    )

    filtered_features = features_df[
        feature_mask
    ].copy()

else:

    filtered_features = features_df.copy()


# ============================================================
# 15. TASK ACTIVITY VALIDATION
# ============================================================

filtered_daily["tasks_started"] = pd.to_numeric(
    filtered_daily["tasks_started"],
    errors="coerce"
).fillna(0)

filtered_daily["tasks_completed"] = pd.to_numeric(
    filtered_daily["tasks_completed"],
    errors="coerce"
).fillna(0)


# Invalid daily activity records:
# Completed tasks greater than started tasks,
# or negative task counts.

invalid_task_mask = (
    (filtered_daily["tasks_completed"] < 0)
    |
    (filtered_daily["tasks_started"] < 0)
    |
    (
        filtered_daily["tasks_completed"]
        > filtered_daily["tasks_started"]
    )
)

invalid_task_records = filtered_daily[
    invalid_task_mask
].copy()

valid_daily = filtered_daily[
    ~invalid_task_mask
].copy()


total_tasks_started = safe_sum(
    valid_daily,
    "tasks_started"
)

total_tasks_completed = safe_sum(
    valid_daily,
    "tasks_completed"
)

overall_task_completion_rate = safe_percent(
    total_tasks_completed,
    total_tasks_started
)


# ============================================================
# 16. USER COHORT AND ACTIVITY METRICS
# ============================================================

total_users = len(filtered_users)

total_sessions = len(filtered_sessions)

total_events = len(filtered_events)

unique_active_users = safe_unique(
    filtered_daily,
    "user_id"
)

unique_event_users = safe_unique(
    filtered_events,
    "user_id"
)

unique_session_users = safe_unique(
    filtered_sessions,
    "user_id"
)


# ============================================================
# 17. SIMULATED DATA NOTICE
# ============================================================

show_notice(
    "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING. "
    "Dashboard metrics and visualizations must not be interpreted "
    "as verified live business performance unless independently "
    "validated against production records.",
    "data"
)


# ============================================================
# 18. OVERVIEW
# ============================================================

if section == "Overview":

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "High-level product activity, user engagement, "
        "task completion, and feature performance."
    )

    # --------------------------------------------------------
    # 18.1 KPI CARDS
    # --------------------------------------------------------

    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

    with kpi_col1:

        st.metric(
            "Total Users",
            f"{total_users:,}"
        )

    with kpi_col2:

        st.metric(
            "Active Users",
            f"{unique_active_users:,}"
        )

    with kpi_col3:

        st.metric(
            "Total Sessions",
            f"{total_sessions:,}"
        )

    with kpi_col4:

        st.metric(
            "Task Completion",
            f"{overall_task_completion_rate:.1f}%"
        )

    with kpi_col5:

        st.metric(
            "Feature Events",
            f"{total_events:,}"
        )


    st.markdown("---")


    # --------------------------------------------------------
    # 18.2 DAILY ACTIVITY AND TASK PERFORMANCE
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(
        [1.6, 1]
    )

    with chart_col1:

        card_header(
            "Daily Active Users & Task Activity"
        )

        if not filtered_daily.empty:

            daily_overview = (
                filtered_daily
                .groupby("activity_date", dropna=False)
                .agg(
                    active_users=("user_id", "nunique"),
                    tasks_started=("tasks_started", "sum"),
                    tasks_completed=("tasks_completed", "sum")
                )
                .reset_index()
            )

            daily_overview["activity_date"] = pd.to_datetime(
                daily_overview["activity_date"],
                errors="coerce"
            )

            daily_overview = daily_overview.dropna(
                subset=["activity_date"]
            )

            if not daily_overview.empty:

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=daily_overview["activity_date"],
                        y=daily_overview["active_users"],
                        name="Active Users",
                        mode="lines+markers",
                        line=dict(
                            color=COLORS["cyan"],
                            width=3
                        ),
                        fill="tozeroy",
                        fillcolor="rgba(34,211,238,0.08)"
                    )
                )

                fig.add_trace(
                    go.Bar(
                        x=daily_overview["activity_date"],
                        y=daily_overview["tasks_completed"],
                        name="Tasks Completed",
                        marker_color=COLORS["primary"],
                        opacity=0.65
                    )
                )

                fig.update_layout(
                    barmode="overlay",
                    xaxis_title="Activity Date",
                    yaxis_title="Count",
                    legend=dict(
                        orientation="h",
                        y=1.12
                    )
                )

                st.plotly_chart(
                    style_fig(fig, 380),
                    use_container_width=True
                )

            else:

                st.info(
                    "No valid activity dates available."
                )

        else:

            st.info(
                "No daily activity data for the selected filters."
            )


    with chart_col2:

        card_header(
            "Account Health Distribution"
        )

        if (
            not filtered_users.empty
            and "account_status" in filtered_users.columns
        ):

            account_status = (
                filtered_users["account_status"]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .reset_index()
            )

            account_status.columns = [
                "Account Status",
                "Users"
            ]

            fig = px.pie(
                account_status,
                names="Account Status",
                values="Users",
                hole=0.65,
                color_discrete_sequence=[
                    COLORS["green"],
                    COLORS["yellow"],
                    COLORS["red"],
                    COLORS["purple"],
                    COLORS["cyan"]
                ]
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )

            st.plotly_chart(
                style_fig(fig, 380),
                use_container_width=True
            )

        else:

            st.info(
                "Account status information is unavailable."
            )


    # --------------------------------------------------------
    # 18.3 RECENT TASK EXECUTION ACTIVITY
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "Recent Task Execution Activity"
    )

    if not filtered_tasks.empty:

        recent_tasks = filtered_tasks.copy()

        recent_tasks = ensure_columns(
            recent_tasks,
            {
                "task_category": "Unknown",
                "user_id": "",
                "status": "Unknown",
                "activity_id": "",
                "created_at": pd.NaT
            }
        )

        recent_tasks["created_at"] = pd.to_datetime(
            recent_tasks["created_at"],
            errors="coerce"
        )

        recent_tasks = recent_tasks.sort_values(
            "created_at",
            ascending=False,
            na_position="last"
        ).head(10)

        recent_tasks = recent_tasks.rename(
            columns={
                "task_category": "Task Category",
                "user_id": "User ID",
                "status": "Reward Status",
                "activity_id": "Activity ID",
                "created_at": "Activity Date"
            }
        )

        display_columns = [
            "Task Category",
            "User ID",
            "Reward Status",
            "Activity ID",
            "Activity Date"
        ]

        st.dataframe(
            recent_tasks[display_columns],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Task-level execution records are not available "
            "in the current data source. Daily task aggregates "
            "are displayed separately."
        )


    # --------------------------------------------------------
    # 18.4 WEEKDAY COMPLETION PERFORMANCE
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        card_header(
            "Task Completion by Weekday"
        )

        if not valid_daily.empty:

            weekday_data = valid_daily.copy()

            weekday_data["activity_date"] = pd.to_datetime(
                weekday_data["activity_date"],
                errors="coerce"
            )

            weekday_data = weekday_data.dropna(
                subset=["activity_date"]
            )

            if not weekday_data.empty:

                weekday_data["Weekday"] = (
                    weekday_data["activity_date"]
                    .dt.day_name()
                )

                weekday_order = [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday"
                ]

                weekday_summary = (
                    weekday_data
                    .groupby("Weekday")
                    .agg(
                        Tasks_Started=("tasks_started", "sum"),
                        Tasks_Completed=("tasks_completed", "sum")
                    )
                    .reindex(weekday_order)
                    .fillna(0)
                    .reset_index()
                )

                fig = go.Figure()

                fig.add_trace(
                    go.Bar(
                        x=weekday_summary["Weekday"],
                        y=weekday_summary["Tasks_Started"],
                        name="Started",
                        marker_color=COLORS["primary"]
                    )
                )

                fig.add_trace(
                    go.Bar(
                        x=weekday_summary["Weekday"],
                        y=weekday_summary["Tasks_Completed"],
                        name="Completed",
                        marker_color=COLORS["green"]
                    )
                )

                fig.update_layout(
                    barmode="group",
                    xaxis_title="Weekday",
                    yaxis_title="Tasks"
                )

                st.plotly_chart(
                    style_fig(fig, 350),
                    use_container_width=True
                )

            else:

                st.info("No valid weekday information.")

        else:

            st.info("No task aggregates available.")


    # --------------------------------------------------------
    # 18.5 DEVICE TELEMETRY
    # --------------------------------------------------------

    with chart_col2:

        card_header(
            "Device Telemetry Distribution"
        )

        if not filtered_users.empty:

            device_summary = (
                filtered_users["device_type"]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .reset_index()
            )

            device_summary.columns = [
                "Device",
                "Users"
            ]

            fig = px.bar(
                device_summary,
                x="Device",
                y="Users",
                color="Device",
                color_discrete_sequence=[
                    COLORS["primary"],
                    COLORS["cyan"],
                    COLORS["purple"],
                    COLORS["green"]
                ]
            )

            fig.update_layout(
                showlegend=False,
                xaxis_title="Device Type",
                yaxis_title="Users"
            )

            st.plotly_chart(
                style_fig(fig, 350),
                use_container_width=True
            )

        else:

            st.info(
                "Device information is unavailable."
            )


    # --------------------------------------------------------
    # 18.6 TOP FEATURE ENGAGEMENT
    # --------------------------------------------------------

    st.markdown("---")

    chart_col1, chart_col2 = st.columns(
        [1.4, 1]
    )

    with chart_col1:

        card_header(
            "Top Feature Engagement"
        )

        if not filtered_events.empty:

            top_features = (
                filtered_events
                .groupby("feature_name", dropna=False)
                .agg(
                    Total_Events=("event_name", "count"),
                    Unique_Users=("user_id", "nunique")
                )
                .reset_index()
                .sort_values(
                    "Total_Events",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                top_features,
                x="Total_Events",
                y="feature_name",
                orientation="h",
                color="Total_Events",
                color_continuous_scale="Blues",
                hover_data=["Unique_Users"]
            )

            fig.update_layout(
                yaxis_title="Feature",
                xaxis_title="Events",
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            st.plotly_chart(
                style_fig(fig, 380),
                use_container_width=True
            )

        else:

            st.info(
                "No feature events are available for this selection."
            )


    with chart_col2:

        card_header(
            "XP & Reward Activity"
        )

        daily_xp_series = pd.to_numeric(
            valid_daily.get("daily_xp_earned", pd.Series(dtype=float)),
            errors="coerce"
        ).dropna()
        user_xp_series = pd.to_numeric(
            filtered_users.get("xp_balance", pd.Series(dtype=float)),
            errors="coerce"
        ).dropna()

        xp_total = float(daily_xp_series.sum()) if not daily_xp_series.empty else 0.0
        xp_average = float(daily_xp_series.mean()) if not daily_xp_series.empty else 0.0
        xp_median = float(daily_xp_series.median()) if not daily_xp_series.empty else 0.0
        current_xp_balance = float(user_xp_series.sum()) if not user_xp_series.empty else 0.0

        xp_col1, xp_col2 = st.columns(2)

        with xp_col1:

            st.metric(
                "Current User XP Balance",
                f"{current_xp_balance:,.0f}"
            )

            st.metric(
                "Average XP / Record",
                f"{xp_average:,.1f}"
            )

        with xp_col2:

            st.metric(
                "Median XP",
                f"{xp_median:,.0f}"
            )

            st.metric(
                "Completed Tasks",
                f"{total_tasks_completed:,.0f}"
            )

        st.caption(
            "Current XP balance comes from users.xp_balance. Daily XP earned "
            "is shown separately from daily_activity.daily_xp_earned."
        )


    # --------------------------------------------------------
    # 18.7 OVERVIEW DATA QUALITY SUMMARY
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "Overview Data Quality Summary"
    )

    quality_col1, quality_col2, quality_col3 = st.columns(3)

    with quality_col1:

        st.metric(
            "Invalid Daily Task Records",
            f"{len(invalid_task_records):,}"
        )

    with quality_col2:

        st.metric(
            "Valid Daily Activity Records",
            f"{len(valid_daily):,}"
        )

    with quality_col3:

        st.metric(
            "Available Event Catalog Entries",
            f"{len(event_catalog_df):,}"
        )

    st.caption(
        "Invalid task records are excluded from task performance "
        "calculations when completed tasks exceed started tasks "
        "or task counts are negative."
    )

# ============================================================
# 19. USER ANALYTICS
# ============================================================

elif section == "User Analytics":

    st.markdown(
        '<div class="section-title">User & Account Analytics</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Understand user demographics, acquisition channels, "
        "geographic distribution, and registration trends."
    )

    # --------------------------------------------------------
    # 19.1 USER KPI METRICS
    # --------------------------------------------------------

    total_user_records = len(filtered_users)

    active_accounts = 0
    inactive_accounts = 0
    suspended_accounts = 0

    if not filtered_users.empty:

        account_status_values = (
            filtered_users["account_status"]
            .fillna("Unknown")
            .astype(str)
            .str.lower()
            .str.strip()
        )

        active_accounts = int(
            account_status_values.isin(
                ["active", "verified"]
            ).sum()
        )

        inactive_accounts = int(
            account_status_values.isin(
                ["inactive", "pending", "pending verification"]
            ).sum()
        )

        suspended_accounts = int(
            account_status_values.isin(
                ["suspended", "blocked", "disabled"]
            ).sum()
        )

    user_col1, user_col2, user_col3, user_col4 = st.columns(4)

    with user_col1:

        st.metric(
            "Total User Records",
            f"{total_user_records:,}"
        )

    with user_col2:

        st.metric(
            "Active Accounts",
            f"{active_accounts:,}"
        )

    with user_col3:

        st.metric(
            "Inactive / Pending",
            f"{inactive_accounts:,}"
        )

    with user_col4:

        st.metric(
            "Suspended Accounts",
            f"{suspended_accounts:,}"
        )


    st.markdown("---")


    # --------------------------------------------------------
    # 19.2 AGE DISTRIBUTION
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        card_header(
            "User Age Distribution"
        )

        age_data = filtered_users.copy()

        age_data["age"] = pd.to_numeric(
            age_data["age"],
            errors="coerce"
        )

        age_data = age_data[
            age_data["age"].between(0, 120)
        ]

        if not age_data.empty:

            age_data["Age Group"] = pd.cut(
                age_data["age"],
                bins=[0, 24, 34, 44, np.inf],
                labels=[
                    "0–24",
                    "25–34",
                    "35–44",
                    "45+"
                ],
                include_lowest=True
            )

            age_summary = (
                age_data["Age Group"]
                .value_counts()
                .sort_index()
                .reset_index()
            )

            age_summary.columns = [
                "Age Group",
                "Users"
            ]

            fig = px.bar(
                age_summary,
                x="Age Group",
                y="Users",
                color="Users",
                color_continuous_scale="Blues",
                text="Users"
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                xaxis_title="Age Group",
                yaxis_title="Number of Users"
            )

            st.plotly_chart(
                style_fig(fig, 350),
                use_container_width=True
            )

            st.caption(
                f"Average age: {safe_mean(age_data['age']):.1f} years"
            )

        else:

            st.info(
                "Age information is unavailable."
            )


    # --------------------------------------------------------
    # 19.3 GENDER DISTRIBUTION
    # --------------------------------------------------------

    with chart_col2:

        card_header(
            "Gender Distribution"
        )

        if not filtered_users.empty:

            gender_summary = (
                filtered_users["gender"]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .reset_index()
            )

            gender_summary.columns = [
                "Gender",
                "Users"
            ]

            fig = px.pie(
                gender_summary,
                names="Gender",
                values="Users",
                hole=0.58,
                color_discrete_sequence=[
                    COLORS["primary"],
                    COLORS["pink"],
                    COLORS["purple"],
                    COLORS["cyan"]
                ]
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )

            st.plotly_chart(
                style_fig(fig, 350),
                use_container_width=True
            )

        else:

            st.info(
                "Gender information is unavailable."
            )


    st.markdown("---")


    # --------------------------------------------------------
    # 19.4 ACQUISITION CHANNEL ANALYSIS
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(
        [1.2, 1]
    )

    with chart_col1:

        card_header(
            "User Acquisition Channels"
        )

        if not filtered_users.empty:

            acquisition_summary = (
                filtered_users["acquisition_source"]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .reset_index()
            )

            acquisition_summary.columns = [
                "Acquisition Channel",
                "Users"
            ]

            fig = px.bar(
                acquisition_summary,
                x="Users",
                y="Acquisition Channel",
                orientation="h",
                color="Users",
                color_continuous_scale="Blues",
                text="Users"
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                yaxis=dict(
                    categoryorder="total ascending"
                ),
                xaxis_title="Users",
                yaxis_title="Acquisition Channel"
            )

            st.plotly_chart(
                style_fig(fig, 380),
                use_container_width=True
            )

        else:

            st.info(
                "Acquisition information is unavailable."
            )


    # --------------------------------------------------------
    # 19.5 GEOGRAPHIC DISTRIBUTION
    # --------------------------------------------------------

    with chart_col2:

        card_header(
            "Geographic User Distribution"
        )

        if not filtered_users.empty:

            geographic_summary = (
                filtered_users["state"]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .head(12)
                .reset_index()
            )

            geographic_summary.columns = [
                "State",
                "Users"
            ]

            fig = px.bar(
                geographic_summary,
                x="Users",
                y="State",
                orientation="h",
                color="Users",
                color_continuous_scale="Viridis"
            )

            fig.update_layout(
                yaxis=dict(
                    categoryorder="total ascending"
                ),
                xaxis_title="Users",
                yaxis_title="State"
            )

            st.plotly_chart(
                style_fig(fig, 380),
                use_container_width=True
            )

        else:

            st.info(
                "Geographic information is unavailable."
            )


    st.markdown("---")


    # --------------------------------------------------------
    # 19.6 REGISTRATION GROWTH
    # --------------------------------------------------------

    card_header(
        "Cumulative User Registration Growth"
    )

    registration_data = filtered_users.copy()

    registration_data["registration_datetime"] = pd.to_datetime(
        registration_data["registration_datetime"],
        errors="coerce"
    )

    registration_data = registration_data.dropna(
        subset=["registration_datetime"]
    )

    if not registration_data.empty:

        registration_data["Registration Date"] = (
            registration_data["registration_datetime"].dt.date
        )

        registration_summary = (
            registration_data
            .groupby("Registration Date")
            .size()
            .reset_index(name="New Users")
            .sort_values("Registration Date")
        )

        registration_summary["Cumulative Users"] = (
            registration_summary["New Users"].cumsum()
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=registration_summary["Registration Date"],
                y=registration_summary["Cumulative Users"],
                mode="lines+markers",
                name="Cumulative Users",
                line=dict(
                    color=COLORS["cyan"],
                    width=3
                ),
                fill="tozeroy",
                fillcolor="rgba(34,211,238,0.10)"
            )
        )

        fig.update_layout(
            xaxis_title="Registration Date",
            yaxis_title="Cumulative Users"
        )

        st.plotly_chart(
            style_fig(fig, 380),
            use_container_width=True
        )

    else:

        st.info(
            "Registration dates are unavailable."
        )


    # --------------------------------------------------------
    # 19.7 USER ACCOUNT TABLE
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "User Account Records"
    )

    if not filtered_users.empty:

        display_user_columns = [
            "user_id",
            "full_name",
            "age",
            "gender",
            "state",
            "city",
            "device_type",
            "acquisition_source",
            "account_status",
            "registration_datetime"
        ]

        available_columns = [
            column
            for column in display_user_columns
            if column in filtered_users.columns
        ]

        st.dataframe(
            filtered_users[available_columns],
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Showing {len(filtered_users):,} user records."
        )

    else:

        st.info(
            "No user records are available for the selected filters."
        )


# ============================================================
# 20. FEATURE & ENGAGEMENT ANALYTICS
# ============================================================

elif section == "Feature & Engagement":

    st.markdown(
        '<div class="section-title">Engagement & Behavioral Analytics</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Analyze user interaction patterns, session behavior, "
        "feature adoption, and engagement trends."
    )


    # --------------------------------------------------------
    # 20.1 ENGAGEMENT KPIs
    # --------------------------------------------------------

    total_engagement_events = len(filtered_events)

    total_engagement_sessions = len(filtered_sessions)

    unique_event_users = safe_unique(
        filtered_events,
        "user_id"
    )

    unique_session_users = safe_unique(
        filtered_sessions,
        "user_id"
    )

    average_events_per_user = (
        total_engagement_events / unique_event_users
        if unique_event_users > 0
        else 0
    )

    average_sessions_per_user = (
        total_engagement_sessions / unique_session_users
        if unique_session_users > 0
        else 0
    )

    session_duration = pd.to_numeric(
        filtered_sessions["session_duration_seconds"],
        errors="coerce"
    ).dropna()

    average_duration = (
        session_duration.mean() / 60
        if not session_duration.empty
        else 0
    )

    median_duration = (
        session_duration.median() / 60
        if not session_duration.empty
        else 0
    )


    engagement_col1, engagement_col2, engagement_col3, engagement_col4, engagement_col5 = st.columns(5)

    with engagement_col1:

        st.metric(
            "Total Events",
            f"{total_engagement_events:,}"
        )

    with engagement_col2:

        st.metric(
            "Total Sessions",
            f"{total_engagement_sessions:,}"
        )

    with engagement_col3:

        st.metric(
            "Unique Event Users",
            f"{unique_event_users:,}"
        )

    with engagement_col4:

        st.metric(
            "Avg. Session Duration",
            f"{average_duration:.1f} min"
        )

    with engagement_col5:

        st.metric(
            "Events / User",
            f"{average_events_per_user:.1f}"
        )


    st.markdown("---")


    # --------------------------------------------------------
    # 20.2 DAILY ENGAGEMENT CADENCE
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(
        [1.5, 1]
    )

    with chart_col1:

        card_header(
            "Daily Engagement Activity"
        )

        if not filtered_events.empty:

            engagement_daily = filtered_events.copy()

            engagement_daily["event_datetime"] = pd.to_datetime(
                engagement_daily["event_datetime"],
                errors="coerce"
            )

            engagement_daily = engagement_daily.dropna(
                subset=["event_datetime"]
            )

            if not engagement_daily.empty:

                engagement_daily["Date"] = (
                    engagement_daily["event_datetime"].dt.date
                )

                engagement_summary = (
                    engagement_daily
                    .groupby("Date")
                    .agg(
                        Total_Events=("event_name", "count"),
                        Unique_Users=("user_id", "nunique")
                    )
                    .reset_index()
                )

                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=engagement_summary["Date"],
                        y=engagement_summary["Total_Events"],
                        mode="lines+markers",
                        name="Events",
                        line=dict(
                            color=COLORS["cyan"],
                            width=3
                        )
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=engagement_summary["Date"],
                        y=engagement_summary["Unique_Users"],
                        mode="lines+markers",
                        name="Unique Users",
                        line=dict(
                            color=COLORS["purple"],
                            width=2
                        )
                    )
                )

                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Count",
                    legend=dict(
                        orientation="h",
                        y=1.12
                    )
                )

                st.plotly_chart(
                    style_fig(fig, 380),
                    use_container_width=True
                )

            else:

                st.info(
                    "Event timestamps are unavailable."
                )

        else:

            st.info(
                "No event records are available for the selected filters."
            )


    # --------------------------------------------------------
    # 20.3 SESSION DURATION DISTRIBUTION
    # --------------------------------------------------------

    with chart_col2:

        card_header(
            "Session Duration Distribution"
        )

        if not session_duration.empty:

            duration_minutes = (
                session_duration / 60
            )

            duration_df = pd.DataFrame({
                "Duration (Minutes)": duration_minutes
            })

            fig = px.histogram(
                duration_df,
                x="Duration (Minutes)",
                nbins=25,
                color_discrete_sequence=[
                    COLORS["primary"]
                ]
            )

            fig.update_layout(
                xaxis_title="Session Duration (Minutes)",
                yaxis_title="Number of Sessions"
            )

            st.plotly_chart(
                style_fig(fig, 380),
                use_container_width=True
            )

        else:

            st.info(
                "Session duration information is unavailable."
            )


    st.markdown("---")


    # --------------------------------------------------------
    # 20.4 FEATURE ADOPTION
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        card_header(
            "Feature Adoption by Unique Users"
        )

        if not filtered_events.empty:

            feature_adoption = (
                filtered_events
                .groupby("feature_name", dropna=False)
                .agg(
                    Unique_Users=("user_id", "nunique"),
                    Total_Events=("event_name", "count")
                )
                .reset_index()
                .sort_values(
                    "Unique_Users",
                    ascending=False
                )
                .head(12)
            )

            fig = px.bar(
                feature_adoption,
                x="Unique_Users",
                y="feature_name",
                orientation="h",
                color="Unique_Users",
                color_continuous_scale="Teal",
                hover_data=["Total_Events"]
            )

            fig.update_layout(
                yaxis=dict(
                    categoryorder="total ascending"
                ),
                xaxis_title="Unique Users",
                yaxis_title="Feature"
            )

            st.plotly_chart(
                style_fig(fig, 380),
                use_container_width=True
            )

        else:

            st.info(
                "Feature adoption data is unavailable."
            )


    # --------------------------------------------------------
    # 20.5 EVENT BREAKDOWN
    # --------------------------------------------------------

    with chart_col2:

        card_header(
            "Most Frequently Triggered Events"
        )

        if not filtered_events.empty:

            event_summary = (
                filtered_events["event_name"]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .head(12)
                .reset_index()
            )

            event_summary.columns = [
                "Event",
                "Count"
            ]

            fig = px.bar(
                event_summary,
                x="Count",
                y="Event",
                orientation="h",
                color="Count",
                color_continuous_scale="Purples"
            )

            fig.update_layout(
                yaxis=dict(
                    categoryorder="total ascending"
                ),
                xaxis_title="Event Count",
                yaxis_title="Event"
            )

            st.plotly_chart(
                style_fig(fig, 380),
                use_container_width=True
            )

        else:

            st.info(
                "Event breakdown is unavailable."
            )


    st.markdown("---")


    # --------------------------------------------------------
    # 20.6 SESSION ENGAGEMENT METRICS
    # --------------------------------------------------------

    card_header(
        "Session Engagement Metrics"
    )

    session_col1, session_col2, session_col3, session_col4 = st.columns(4)

    with session_col1:

        st.metric(
            "Average Session Duration",
            f"{average_duration:.2f} minutes"
        )

    with session_col2:

        st.metric(
            "Median Session Duration",
            f"{median_duration:.2f} minutes"
        )

    with session_col3:

        st.metric(
            "Sessions per User",
            f"{average_sessions_per_user:.2f}"
        )

    with session_col4:

        st.metric(
            "Unique Session Users",
            f"{unique_session_users:,}"
        )


    # --------------------------------------------------------
    # 20.7 FEATURE ENGAGEMENT TABLE
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "Feature Engagement Details"
    )

    if not filtered_events.empty:

        feature_table = (
            filtered_events
            .groupby("feature_name", dropna=False)
            .agg(
                Total_Events=("event_name", "count"),
                Unique_Users=("user_id", "nunique"),
                Event_Types=("event_name", "nunique")
            )
            .reset_index()
            .sort_values(
                "Total_Events",
                ascending=False
            )
        )

        feature_table = feature_table.rename(
            columns={
                "feature_name": "Feature",
                "Total_Events": "Total Events",
                "Unique_Users": "Unique Users",
                "Event_Types": "Event Types"
            }
        )

        st.dataframe(
            feature_table,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No feature engagement records are available."
        )


    # --------------------------------------------------------
    # 20.8 MILESTONE ANALYTICS
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "Milestone Achievement Analytics"
    )

    if not milestones_df.empty:

        milestone_data = milestones_df.copy()

        milestone_data = ensure_columns(
            milestone_data,
            {
                "milestone_name": "Unknown",
                "milestone_status": "Unknown",
                "user_id": ""
            }
        )

        milestone_summary = (
            milestone_data
            .groupby(
                ["milestone_name", "milestone_status"],
                dropna=False
            )
            .size()
            .reset_index(name="Records")
        )

        st.dataframe(
            milestone_summary,
            use_container_width=True,
            hide_index=True
        )

        milestone_col1, milestone_col2 = st.columns(2)

        with milestone_col1:

            st.metric(
                "Total Milestone Records",
                f"{len(milestone_data):,}"
            )

        with milestone_col2:

            st.metric(
                "Unique Users",
                f"{safe_unique(milestone_data, 'user_id'):,}"
            )

    else:

        show_notice(
            "Milestone-level records are not available in the "
            "current PostgreSQL dataset. No milestone achievements "
            "are being fabricated or inferred.",
            "warning"
        )


    # --------------------------------------------------------
    # 20.9 EVENT CATALOG
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "Registered Event Catalog"

    )

    if not event_catalog_df.empty:

        st.dataframe(
            event_catalog_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"{len(event_catalog_df):,} event catalog records available."
        )

    else:

        st.info(
            "No event catalog records are available."
        )
# ============================================================
# 21. EARNING & REWARDS ANALYTICS
# ============================================================

elif section == "Earning & Rewards":

    st.markdown(
        '<div class="section-title">Earning & Rewards Analytics</div>',
        unsafe_allow_html=True
    )
    st.caption(
        "Analyze daily task aggregates, current XP balances, and reward engagement."
    )

    if filtered_daily.empty:
        show_notice(
            "Daily task activity is unavailable for the selected date range.",
            "warning"
        )

    if tasks_df.empty:
        show_notice(
            "The PostgreSQL task_activity table contains no task-level records. "
            "Task execution details cannot be displayed until source records exist.",
            "warning"
        )

    total_started = safe_sum(valid_daily, "tasks_started")
    total_completed = safe_sum(valid_daily, "tasks_completed")
    completion_rate = safe_percent(total_completed, total_started)

    daily_xp_values = pd.to_numeric(
        valid_daily.get("daily_xp_earned", pd.Series(dtype=float)),
        errors="coerce"
    ).dropna()
    total_xp_earned = float(daily_xp_values.sum()) if not daily_xp_values.empty else 0.0
    average_xp_earned = float(daily_xp_values.mean()) if not daily_xp_values.empty else 0.0
    median_xp_earned = float(daily_xp_values.median()) if not daily_xp_values.empty else 0.0

    user_xp_values = pd.to_numeric(
        filtered_users.get("xp_balance", pd.Series(dtype=float)),
        errors="coerce"
    ).dropna()
    total_xp_balance = float(user_xp_values.sum()) if not user_xp_values.empty else 0.0
    average_xp_balance = float(user_xp_values.mean()) if not user_xp_values.empty else 0.0
    maximum_xp_balance = float(user_xp_values.max()) if not user_xp_values.empty else 0.0

    reward_col1, reward_col2, reward_col3, reward_col4, reward_col5 = st.columns(5)
    with reward_col1:
        st.metric("Tasks Started", f"{total_started:,.0f}")
    with reward_col2:
        st.metric("Tasks Completed", f"{total_completed:,.0f}")
    with reward_col3:
        st.metric("Completion Rate", f"{completion_rate:.2f}%")
    with reward_col4:
        st.metric("Daily XP Earned", f"{total_xp_earned:,.0f}")
    with reward_col5:
        st.metric("Average Daily XP / Record", f"{average_xp_earned:,.1f}")

    st.markdown("### Current User XP Balance")
    xp_col1, xp_col2, xp_col3 = st.columns(3)
    with xp_col1:
        st.metric("Total User XP Balance", f"{total_xp_balance:,.0f}")
    with xp_col2:
        st.metric("Average User XP Balance", f"{average_xp_balance:,.2f}")
    with xp_col3:
        st.metric("Maximum User XP Balance", f"{maximum_xp_balance:,.0f}")
    st.caption(
        "XP earned is sourced from daily_activity.daily_xp_earned. "
        "Current balances are sourced independently from users.xp_balance."
    )

    st.markdown("---")
    chart_col1, chart_col2 = st.columns([1.5, 1])

    with chart_col1:
        card_header("Daily Task Starts vs Completions")
        if not valid_daily.empty and "activity_date" in valid_daily.columns:
            daily_task_summary = (
                valid_daily.groupby("activity_date", dropna=False)
                .agg(
                    Tasks_Started=("tasks_started", "sum"),
                    Tasks_Completed=("tasks_completed", "sum")
                ).reset_index()
            )
            daily_task_summary["activity_date"] = pd.to_datetime(
                daily_task_summary["activity_date"], errors="coerce"
            )
            daily_task_summary = daily_task_summary.dropna(subset=["activity_date"])
            if not daily_task_summary.empty:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=daily_task_summary["activity_date"],
                    y=daily_task_summary["Tasks_Started"],
                    name="Tasks Started", marker_color=COLORS["primary"]
                ))
                fig.add_trace(go.Bar(
                    x=daily_task_summary["activity_date"],
                    y=daily_task_summary["Tasks_Completed"],
                    name="Tasks Completed", marker_color=COLORS["green"]
                ))
                fig.update_layout(
                    barmode="group", xaxis_title="Activity Date",
                    yaxis_title="Task Count"
                )
                st.plotly_chart(style_fig(fig, 380), use_container_width=True)
            else:
                st.info("No valid task activity dates are available.")
        else:
            st.info("No daily task aggregate data is available.")

    with chart_col2:
        card_header("Overall Task Completion Rate")
        if total_started > 0:
            completed_value = min(max(total_completed, 0), max(total_started, 0))
            incomplete_value = max(total_started - completed_value, 0)
            fig = go.Figure(data=[go.Pie(
                labels=["Completed", "Not Completed"],
                values=[completed_value, incomplete_value],
                hole=0.70,
                marker=dict(colors=[COLORS["green"], COLORS["card_secondary"]]),
                textinfo="label+percent"
            )])
            fig.update_layout(annotations=[dict(
                text=f"{completion_rate:.1f}%", x=0.5, y=0.5,
                font_size=24, showarrow=False, font_color=COLORS["text"]
            )])
            st.plotly_chart(style_fig(fig, 380), use_container_width=True)
        else:
            st.info("Task completion rate cannot be calculated because there are no valid task starts.")

    st.markdown("---")
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        card_header("Daily XP Earned Distribution")
        if not daily_xp_values.empty:
            xp_distribution = pd.DataFrame({"Daily XP Earned": daily_xp_values})
            fig = px.histogram(
                xp_distribution, x="Daily XP Earned", nbins=30,
                color_discrete_sequence=[COLORS["purple"]]
            )
            fig.update_layout(
                xaxis_title="Daily XP Earned", yaxis_title="Activity Records"
            )
            st.plotly_chart(style_fig(fig, 350), use_container_width=True)
        else:
            st.info("Daily XP earned values are zero or unavailable in the selected records.")

    with chart_col2:
        card_header("Current User XP Balance Distribution")
        if not user_xp_values.empty:
            xp_balance_frame = pd.DataFrame({"User XP Balance": user_xp_values})
            fig = px.histogram(
                xp_balance_frame, x="User XP Balance", nbins=25,
                color_discrete_sequence=[COLORS["primary"]]
            )
            fig.update_layout(
                xaxis_title="Current XP Balance", yaxis_title="Users"
            )
            st.plotly_chart(style_fig(fig, 350), use_container_width=True)
        else:
            st.info("User XP balance data is unavailable.")

    st.markdown("---")
    card_header("Task Category Analysis")
    if not filtered_tasks.empty:
        task_category_col = "task_category" if "task_category" in filtered_tasks.columns else "category"
        task_summary = (
            filtered_tasks.groupby(task_category_col, dropna=False)
            .agg(
                Task_Records=("user_id", "size"),
                Unique_Users=("user_id", "nunique"),
                Reward_Points=("reward_points_allocated", "sum")
            ).reset_index()
            .sort_values("Task_Records", ascending=False)
        )
        task_summary = task_summary.rename(columns={
            task_category_col: "Task Category",
            "Task_Records": "Task Records",
            "Unique_Users": "Unique Users",
            "Reward_Points": "Reward Points Allocated"
        })
        st.dataframe(task_summary, use_container_width=True, hide_index=True)
    else:
        st.info("Task category records are unavailable because task_activity is empty.")

    st.markdown("---")
    card_header("Task Data Validation")
    validation_col1, validation_col2, validation_col3 = st.columns(3)
    with validation_col1:
        st.metric("Valid Daily Records", f"{len(valid_daily):,}")
    with validation_col2:
        st.metric("Invalid Daily Records", f"{len(invalid_task_records):,}")
    with validation_col3:
        st.metric("Median Daily XP", f"{median_xp_earned:,.0f}")

    if not invalid_task_records.empty:
        st.warning(
            "Some daily activity records contain negative task counts or "
            "completed tasks greater than started tasks. They are excluded "
            "from task performance calculations."
        )
        with st.expander("View invalid task records"):
            st.dataframe(invalid_task_records, use_container_width=True, hide_index=True)
    else:
        st.success("No invalid daily task records were detected under the current validation rules.")


# ============================================================
# 22. WALLET & WITHDRAWAL ANALYTICS
# ============================================================
elif section == "Wallet & Withdrawal":
    st.markdown(
        '<div class="section-title">Wallet & Withdrawal Analytics</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Monitor wallet balances, transaction activity, "
        "withdrawal processing, and reconciliation indicators."
    )

    show_notice(
        "Wallet and withdrawal figures are based on the available "
        "wallet datasets. Confirm these values against production "
        "financial records before making settlement or accounting decisions.",
        "warning"
    )


    # --------------------------------------------------------
    # 22.1 WALLET METRICS
    # --------------------------------------------------------

    total_wallet_accounts = len(wallet_accounts_df)

    total_opening_balance = safe_sum(
        wallet_accounts_df,
        "opening_balance"
    )

    total_current_balance = safe_sum(
        wallet_accounts_df,
        "current_balance"
    )

    total_ledger_records = len(filtered_wallet_ledger)

    total_ledger_amount = safe_sum(
        filtered_wallet_ledger,
        "amount"
    )

    total_withdrawal_records = len(filtered_withdrawals)

    total_withdrawal_amount = safe_sum(
        filtered_withdrawals,
        "amount"
    )


    wallet_col1, wallet_col2, wallet_col3, wallet_col4, wallet_col5 = st.columns(5)

    with wallet_col1:

        st.metric(
            "Wallet Accounts",
            f"{total_wallet_accounts:,}"
        )

    with wallet_col2:

        st.metric(
            "Opening Balance",
            f"₹{total_opening_balance:,.2f}"
        )

    with wallet_col3:

        st.metric(
            "Current Balance",
            f"₹{total_current_balance:,.2f}"
        )

    with wallet_col4:

        st.metric(
            "Ledger Records",
            f"{total_ledger_records:,}"
        )

    with wallet_col5:

        st.metric(
            "Withdrawal Records",
            f"{total_withdrawal_records:,}"
        )


    st.markdown("---")


    # --------------------------------------------------------
    # 22.2 WITHDRAWAL STATUS DISTRIBUTION
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        card_header(
            "Withdrawal Status Distribution"
        )

        if not filtered_withdrawals.empty:

            withdrawal_status = (
                filtered_withdrawals["status"]
                .fillna("Unknown")
                .astype(str)
                .str.lower()
                .str.strip()
                .value_counts()
                .reset_index()
            )

            withdrawal_status.columns = [
                "Status",
                "Records"
            ]

            fig = px.pie(
                withdrawal_status,
                names="Status",
                values="Records",
                hole=0.62,
                color_discrete_sequence=[
                    COLORS["green"],
                    COLORS["yellow"],
                    COLORS["primary"],
                    COLORS["red"],
                    COLORS["purple"]
                ]
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )

            st.plotly_chart(
                style_fig(fig, 360),
                use_container_width=True
            )

        else:

            st.info(
                "Withdrawal records are unavailable."
            )


    # --------------------------------------------------------
    # 22.3 WITHDRAWAL AMOUNT BY STATUS
    # --------------------------------------------------------

    with chart_col2:

        card_header(
            "Withdrawal Amount by Status"
        )

        if not filtered_withdrawals.empty:

            withdrawal_amount_data = filtered_withdrawals.copy()

            withdrawal_amount_data["amount"] = pd.to_numeric(
                withdrawal_amount_data["amount"],
                errors="coerce"
            ).fillna(0)

            withdrawal_amount_summary = (
                withdrawal_amount_data
                .groupby("status", dropna=False)["amount"]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                withdrawal_amount_summary,
                x="status",
                y="amount",
                color="status",
                text_auto=".2f",
                color_discrete_sequence=[
                    COLORS["primary"],
                    COLORS["green"],
                    COLORS["yellow"],
                    COLORS["red"],
                    COLORS["purple"]
                ]
            )

            fig.update_layout(
                showlegend=False,
                xaxis_title="Withdrawal Status",
                yaxis_title="Amount"
            )

            st.plotly_chart(
                style_fig(fig, 360),
                use_container_width=True
            )

        else:

            st.info(
                "Withdrawal amount data is unavailable."
            )


    # --------------------------------------------------------
    # 22.4 WITHDRAWAL PERFORMANCE
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "Withdrawal Performance Indicators"
    )

    withdrawal_status_normalized = (
        filtered_withdrawals["status"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.strip()
        if not filtered_withdrawals.empty
        else pd.Series(dtype=str)
    )

    settled_count = int(
        withdrawal_status_normalized.isin(
            ["settled", "completed", "success", "successful"]
        ).sum()
    )

    rejected_count = int(
        withdrawal_status_normalized.isin(
            ["rejected", "failed", "declined"]
        ).sum()
    )

    processing_count = int(
        withdrawal_status_normalized.isin(
            ["processing", "pending", "requested"]
        ).sum()
    )

    settled_amount = safe_sum(
        filtered_withdrawals[
            withdrawal_status_normalized.isin(
                ["settled", "completed", "success", "successful"]
            )
        ],
        "amount"
    ) if not filtered_withdrawals.empty else 0

    withdrawal_success_rate = safe_percent(
        settled_count,
        total_withdrawal_records
    )

    withdrawal_col1, withdrawal_col2, withdrawal_col3, withdrawal_col4 = st.columns(4)

    with withdrawal_col1:

        st.metric(
            "Settled Withdrawals",
            f"{settled_count:,}"
        )

    with withdrawal_col2:

        st.metric(
            "Rejected Withdrawals",
            f"{rejected_count:,}"
        )

    with withdrawal_col3:

        st.metric(
            "Processing / Pending",
            f"{processing_count:,}"
        )

    with withdrawal_col4:

        st.metric(
            "Settled Amount",
            f"₹{settled_amount:,.2f}"
        )

    st.caption(
        f"Settled withdrawal rate: {withdrawal_success_rate:.2f}% "
        "of withdrawal records in the selected date range."
    )


    # --------------------------------------------------------
    # 22.5 WALLET DAILY INTERACTIONS
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "Daily Wallet Transaction Activity"
    )

    if not filtered_wallet_ledger.empty:

        ledger_daily = filtered_wallet_ledger.copy()

        ledger_daily["transaction_datetime"] = pd.to_datetime(
            ledger_daily["transaction_datetime"],
            errors="coerce"
        )

        ledger_daily = ledger_daily.dropna(
            subset=["transaction_datetime"]
        )

        if not ledger_daily.empty:

            ledger_daily["Date"] = (
                ledger_daily["transaction_datetime"].dt.date
            )

            ledger_summary = (
                ledger_daily
                .groupby("Date")
                .agg(
                    Transactions=("transaction_id", "count"),
                    Total_Amount=("amount", "sum")
                )
                .reset_index()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=ledger_summary["Date"],
                    y=ledger_summary["Transactions"],
                    name="Transactions",
                    marker_color=COLORS["primary"]
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=ledger_summary["Date"],
                    y=ledger_summary["Total_Amount"],
                    name="Transaction Amount",
                    yaxis="y2",
                    mode="lines+markers",
                    line=dict(
                        color=COLORS["cyan"],
                        width=3
                    )
                )
            )

            fig.update_layout(
                yaxis=dict(
                    title="Transaction Count"
                ),
                yaxis2=dict(
                    title="Amount",
                    overlaying="y",
                    side="right",
                    showgrid=False
                ),
                xaxis_title="Date",
                legend=dict(
                    orientation="h",
                    y=1.12
                )
            )

            st.plotly_chart(
                style_fig(fig, 380),
                use_container_width=True
            )

        else:

            st.info(
                "Valid wallet transaction timestamps are unavailable."
            )

    else:

        st.info(
            "No wallet ledger activity is available for the selected period."
        )


    # --------------------------------------------------------
    # 22.6 XP VS USER ACTIVITY
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "XP Earned vs Active Days"
    )

    if not valid_daily.empty:

        xp_activity = (
            valid_daily
            .groupby("user_id", dropna=False)
            .agg(
                Total_XP=("xp_earned", "sum"),
                Active_Days=("activity_date", "nunique"),
                Tasks_Completed=("tasks_completed", "sum")
            )
            .reset_index()
        )

        xp_activity = xp_activity[
            xp_activity["user_id"].astype(str).str.strip() != ""
        ]

        if not xp_activity.empty:

            fig = px.scatter(
                xp_activity,
                x="Active_Days",
                y="Total_XP",
                size="Tasks_Completed",
                color="Tasks_Completed",
                hover_data=["user_id"],
                color_continuous_scale="Viridis"
            )

            fig.update_layout(
                xaxis_title="Active Days",
                yaxis_title="Total XP"
            )

            st.plotly_chart(
                style_fig(fig, 380),
                use_container_width=True
            )

        else:

            st.info(
                "User activity information is unavailable."
            )

    else:

        st.info(
            "Daily XP activity is unavailable."
        )


    # --------------------------------------------------------
    # 22.7 WITHDRAWAL PIPELINE
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "Withdrawal Processing Pipeline"
    )

    pipeline_stages = [
        ("Requested", ["requested"]),
        ("Processing", ["processing", "pending"]),
        ("Settled", ["settled", "completed", "success", "successful"]),
        ("Rejected", ["rejected", "failed", "declined"]),
        ("Reversed", ["reversed"])
    ]

    pipeline_data = []

    for stage_name, stage_values in pipeline_stages:

        stage_count = int(
            withdrawal_status_normalized.isin(
                stage_values
            ).sum()
        )

        pipeline_data.append({
            "Pipeline Stage": stage_name,
            "Withdrawals": stage_count
        })

    pipeline_df = pd.DataFrame(pipeline_data)

    st.dataframe(
        pipeline_df,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # 22.8 WALLET RECONCILIATION INDICATORS
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "Wallet Reconciliation Indicators"
    )

    if (
        not wallet_accounts_df.empty
        and {"opening_balance", "current_balance"}.issubset(
            wallet_accounts_df.columns
        )
    ):

        opening_total = safe_sum(
            wallet_accounts_df,
            "opening_balance"
        )

        current_total = safe_sum(
            wallet_accounts_df,
            "current_balance"
        )

        balance_change = current_total - opening_total

        reconciliation_col1, reconciliation_col2, reconciliation_col3 = st.columns(3)

        with reconciliation_col1:

            st.metric(
                "Opening Balance Total",
                f"₹{opening_total:,.2f}"
            )

        with reconciliation_col2:

            st.metric(
                "Current Balance Total",
                f"₹{current_total:,.2f}"
            )

        with reconciliation_col3:

            st.metric(
                "Net Balance Change",
                f"₹{balance_change:,.2f}"
            )

    else:

        st.info(
            "Wallet balance information is unavailable."
        )

    st.caption(
        "These totals are dashboard-level indicators. They do not "
        "replace a full double-entry accounting reconciliation."
    )


    # --------------------------------------------------------
    # 22.9 WITHDRAWAL RECORDS
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "Withdrawal Transaction Records"
    )

    if not filtered_withdrawals.empty:

        display_columns = [
            "withdrawal_id",
            "user_id",
            "amount",
            "status",
            "requested_at",
            "processed_at"
        ]

        display_columns = [
            column
            for column in display_columns
            if column in filtered_withdrawals.columns
        ]

        st.dataframe(
            filtered_withdrawals[display_columns],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No withdrawal records are available for the selected filters."
        )


# ============================================================
# 23. REFERRAL & VIRALITY ANALYTICS
# ============================================================

elif section == "Referral & Virality":

    st.markdown(
        '<div class="section-title">Referral & Virality Analytics</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Analyze referral-related user acquisition, referral event "
        "engagement, and available referral relationship records."
    )


    # --------------------------------------------------------
    # 23.1 REFERRAL DATA AVAILABILITY
    # --------------------------------------------------------

    if referrals_df.empty:

        show_notice(
            "Referral relationship records are not available in the "
            "current dataset. Referral acquisition and referral-related "
            "event engagement are shown separately and must not be "
            "interpreted as verified referral conversions.",
            "warning"
        )


    # --------------------------------------------------------
    # 23.2 ACQUISITION SOURCE ANALYSIS
    # --------------------------------------------------------

    if not filtered_users.empty:

        acquisition_data = filtered_users.copy()

        acquisition_data["acquisition_source"] = (
            acquisition_data["acquisition_source"]
            .fillna("Unknown")
            .astype(str)
        )

        referral_acquisition_users = int(
            acquisition_data["acquisition_source"]
            .str.lower()
            .str.contains("referral", na=False)
            .sum()
        )

        total_acquired_users = len(acquisition_data)

    else:

        referral_acquisition_users = 0
        total_acquired_users = 0


    referral_acquisition_rate = safe_percent(
        referral_acquisition_users,
        total_acquired_users
    )


    # --------------------------------------------------------
    # 23.3 REFERRAL KPIs
    # --------------------------------------------------------

    referral_event_names = [
        "referral_created",
        "referral_page_viewed",
        "referral_shared"
    ]

    if not filtered_events.empty:

        normalized_event_names = (
            filtered_events["event_name"]
            .fillna("")
            .astype(str)
            .str.lower()
        )

        referral_event_data = filtered_events[
            normalized_event_names.isin(
                referral_event_names
            )
        ].copy()

    else:

        referral_event_data = pd.DataFrame()


    referral_total_events = len(referral_event_data)

    referral_unique_users = safe_unique(
        referral_event_data,
        "user_id"
    )

    referral_relationship_count = len(
        filtered_referrals
    )

    referral_col1, referral_col2, referral_col3, referral_col4, referral_col5 = st.columns(5)

    with referral_col1:

        st.metric(
            "Referral Acquisition Users",
            f"{referral_acquisition_users:,}"
        )

    with referral_col2:

        st.metric(
            "Acquisition Share",
            f"{referral_acquisition_rate:.1f}%"
        )

    with referral_col3:

        st.metric(
            "Referral Events",
            f"{referral_total_events:,}"
        )

    with referral_col4:

        st.metric(
            "Unique Engaged Users",
            f"{referral_unique_users:,}"
        )

    with referral_col5:

        st.metric(
            "Relationship Records",
            f"{referral_relationship_count:,}"
        )


    st.markdown("---")


    # --------------------------------------------------------
    # 23.4 ACQUISITION CHANNEL DISTRIBUTION
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        card_header(
            "Acquisition Channel Distribution"
        )

        if not filtered_users.empty:

            channel_summary = (
                filtered_users["acquisition_source"]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
                .reset_index()
            )

            channel_summary.columns = [
                "Channel",
                "Users"
            ]

            fig = px.pie(
                channel_summary,
                names="Channel",
                values="Users",
                hole=0.60,
                color_discrete_sequence=[
                    COLORS["primary"],
                    COLORS["cyan"],
                    COLORS["purple"],
                    COLORS["green"],
                    COLORS["yellow"],
                    COLORS["pink"]
                ]
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )

            st.plotly_chart(
                style_fig(fig, 360),
                use_container_width=True
            )

        else:

            st.info(
                "Acquisition channel information is unavailable."
            )


    # --------------------------------------------------------
    # 23.5 REFERRAL EVENT BREAKDOWN
    # --------------------------------------------------------

    with chart_col2:

        card_header(
            "Referral Event Breakdown"
        )

        if not referral_event_data.empty:

            referral_event_summary = (
                referral_event_data["event_name"]
                .value_counts()
                .reset_index()
            )

            referral_event_summary.columns = [
                "Referral Event",
                "Event Count"
            ]

            fig = px.bar(
                referral_event_summary,
                x="Referral Event",
                y="Event Count",
                color="Referral Event",
                color_discrete_sequence=[
                    COLORS["primary"],
                    COLORS["cyan"],
                    COLORS["purple"]
                ],
                text="Event Count"
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                showlegend=False
            )

            st.plotly_chart(
                style_fig(fig, 360),
                use_container_width=True
            )

        else:

            st.info(
                "No referral-related event records are available."
            )


    st.markdown("---")


    # --------------------------------------------------------
    # 23.6 DAILY REFERRAL ENGAGEMENT TREND
    # --------------------------------------------------------

    card_header(
        "Daily Referral Engagement Trend"
    )

    if not referral_event_data.empty:

        referral_trend = referral_event_data.copy()

        referral_trend["event_datetime"] = pd.to_datetime(
            referral_trend["event_datetime"],
            errors="coerce"
        )

        referral_trend = referral_trend.dropna(
            subset=["event_datetime"]
        )

        if not referral_trend.empty:

            referral_trend["Date"] = (
                referral_trend["event_datetime"].dt.date
            )

            referral_daily_summary = (
                referral_trend
                .groupby("Date")
                .agg(
                    Referral_Events=("event_name", "count"),
                    Unique_Users=("user_id", "nunique")
                )
                .reset_index()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=referral_daily_summary["Date"],
                    y=referral_daily_summary["Referral_Events"],
                    mode="lines+markers",
                    name="Referral Events",
                    line=dict(
                        color=COLORS["cyan"],
                        width=3
                    )
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=referral_daily_summary["Date"],
                    y=referral_daily_summary["Unique_Users"],
                    mode="lines+markers",
                    name="Unique Users",
                    line=dict(
                        color=COLORS["purple"],
                        width=2
                    )
                )
            )

            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Count",
                legend=dict(
                    orientation="h",
                    y=1.12
                )
            )

            st.plotly_chart(
                style_fig(fig, 380),
                use_container_width=True
            )

        else:

            st.info(
                "Referral event timestamps are unavailable."
            )

    else:

        st.info(
            "Referral trend information is unavailable."
        )


    # --------------------------------------------------------
    # 23.7 REFERRAL RELATIONSHIP AUDIT
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "Referral Relationship Audit"
    )

    if not filtered_referrals.empty:

        referral_status_summary = (
            filtered_referrals["referral_status"]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
            .reset_index()
        )

        referral_status_summary.columns = [
            "Referral Status",
            "Records"
        ]

        st.dataframe(
            referral_status_summary,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("#### Referral relationship records")

        st.dataframe(
            filtered_referrals,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Referral relationship table contains no records "
            "for the selected period. Conversion rate and successful "
            "referral counts cannot be calculated."
        )


    # --------------------------------------------------------
    # 23.8 REFERRAL EVENT INTERPRETATION
    # --------------------------------------------------------

    st.markdown("---")

    card_header(
        "Referral Analytics Interpretation"
    )

    interpretation_col1, interpretation_col2 = st.columns(2)

    with interpretation_col1:

        st.markdown("#### Available measurements")

        st.write(
            "- Users acquired through a referral-labelled source."
        )

        st.write(
            "- Referral-related feature events."
        )

        st.write(
            "- Unique users triggering referral events."
        )

        st.write(
            "- Referral relationship records, where available."
        )

    with interpretation_col2:

        st.markdown("#### Current limitations")

        st.write(
            "- Referral acquisition does not prove a completed referral."
        )

        st.write(
            "- Event activity does not prove a successful conversion."
        )

        st.write(
            "- Empty relationship data prevents conversion-rate calculation."
        )

        st.write(
            "- Attribution requires a validated referral relationship."
        )

# =============================================================================
# PART 5 — DATA QUALITY, AUDIT, DATA EXPLORER, REPORTS & FOOTER
# =============================================================================

elif section == "Data Quality & Audit":

    card_header("Data Quality & Audit")

    # -------------------------------------------------------------------------
    # TABS
    # -------------------------------------------------------------------------

    quality_tab, explorer_tab, reports_tab, system_tab = st.tabs([
        "Quality Audit",
        "Data Explorer",
        "Reports & Exports",
        "System Information"
    ])

    # =========================================================================
    # TAB 1 — QUALITY AUDIT
    # =========================================================================

    with quality_tab:

        st.subheader("Data Integrity Overview")

        datasets_for_audit = {
            "Users": filtered_users,
            "Sessions": filtered_sessions,
            "Feature Events": filtered_events,
            "Daily Activity": filtered_daily_activity,
            "Wallet Accounts": wallet_accounts_df,
            "Wallet Ledger": filtered_wallet_ledger,
            "Withdrawals": filtered_withdrawals,
            "Referrals": filtered_referrals,
            "Event Catalog": event_catalog_df,
            "Event Validation Log": event_validation_df
        }

        audit_records = []

        for dataset_name, dataset in datasets_for_audit.items():

            if dataset is None:
                dataset = pd.DataFrame()

            row_count = len(dataset)

            missing_cells = (
                int(dataset.isna().sum().sum())
                if not dataset.empty else 0
            )

            if not dataset.empty:
                duplicate_check_df = dataset.copy()

                for column in duplicate_check_df.columns: 
                    duplicate_check_df[column] = duplicate_check_df[column].map(
                        make_hashable
                    )

                duplicate_rows = int(duplicate_check_df.duplicated().sum())
            else:
                duplicate_rows = 0
            duplicate_ids = 0

            possible_id_columns = [
                "id",
                "user_id",
                "session_id",
                "event_id",
                "activity_id",
                "wallet_id",
                "withdrawal_id",
                "referral_id"
            ]

            for column in possible_id_columns:

                if column in dataset.columns:

                    valid_ids = dataset[column].dropna()

                    if not valid_ids.empty:
                        duplicate_ids = max(
                            duplicate_ids,
                            int(valid_ids.duplicated().sum())
                        )

            audit_records.append({
                "Dataset": dataset_name,
                "Rows": row_count,
                "Columns": len(dataset.columns),
                "Missing Cells": missing_cells,
                "Duplicate Rows": duplicate_rows,
                "Duplicate IDs": duplicate_ids,
                "Status": (
                    "EMPTY"
                    if row_count == 0
                    else (
                        "REVIEW"
                        if missing_cells > 0
                        or duplicate_rows > 0
                        or duplicate_ids > 0
                        else "CHECKED"
                    )
                )
            })

        audit_df = pd.DataFrame(audit_records)

        total_audit_rows = int(audit_df["Rows"].sum())
        total_missing_cells = int(audit_df["Missing Cells"].sum())
        total_duplicate_rows = int(audit_df["Duplicate Rows"].sum())
        total_duplicate_ids = int(audit_df["Duplicate IDs"].sum())

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        metric_col1.metric(
            "Total Records",
            f"{total_audit_rows:,}"
        )

        metric_col2.metric(
            "Missing Cells",
            f"{total_missing_cells:,}"
        )

        metric_col3.metric(
            "Duplicate Rows",
            f"{total_duplicate_rows:,}"
        )

        metric_col4.metric(
            "Duplicate IDs",
            f"{total_duplicate_ids:,}"
        )

        st.markdown("### Dataset Audit Results")

        st.dataframe(
            audit_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Data Quality Distribution")

        status_counts = (
            audit_df["Status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = ["Status", "Datasets"]

        if not status_counts.empty:

            fig_quality = px.pie(
                status_counts,
                names="Status",
                values="Datasets",
                hole=0.55,
                title="Dataset Quality Status"
            )

            fig_quality = style_fig(fig_quality)

            st.plotly_chart(
                fig_quality,
                use_container_width=True
            )

        st.markdown("### Task Validation Checks")

        task_validation_records = []

        if not filtered_daily_activity.empty:

            task_data = filtered_daily_activity.copy()

            task_columns = [
                "tasks_started",
                "tasks_completed",
                "tasks_failed",
                "xp_earned"
            ]

            for column in task_columns:

                if column in task_data.columns:

                    numeric_values = pd.to_numeric(
                        task_data[column],
                        errors="coerce"
                    )

                    negative_count = int(
                        (numeric_values < 0).sum()
                    )

                    missing_count = int(
                        numeric_values.isna().sum()
                    )

                    task_validation_records.append({
                        "Validation": f"{column} non-negative",
                        "Records Checked": len(task_data),
                        "Invalid Records": negative_count,
                        "Missing Values": missing_count,
                        "Result": (
                            "PASS"
                            if negative_count == 0
                            else "REVIEW"
                        )
                    })

            if (
                "tasks_started" in task_data.columns
                and "tasks_completed" in task_data.columns
            ):

                started = pd.to_numeric(
                    task_data["tasks_started"],
                    errors="coerce"
                )

                completed = pd.to_numeric(
                    task_data["tasks_completed"],
                    errors="coerce"
                )

                invalid_completion = int(
                    (completed > started).fillna(False).sum()
                )

                task_validation_records.append({
                    "Validation": "Completed tasks <= Started tasks",
                    "Records Checked": len(task_data),
                    "Invalid Records": invalid_completion,
                    "Missing Values": int(
                        started.isna().sum() + completed.isna().sum()
                    ),
                    "Result": (
                        "PASS"
                        if invalid_completion == 0
                        else "REVIEW"
                    )
                })

        if task_validation_records:

            task_validation_df = pd.DataFrame(
                task_validation_records
            )

            st.dataframe(
                task_validation_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Task validation cannot be performed because "
                "daily activity data is unavailable."
            )

        st.markdown("### Session Duration Validation")

        if (
            not filtered_sessions.empty
            and "session_duration_seconds" in filtered_sessions.columns
        ):

            session_duration = pd.to_numeric(
                filtered_sessions["session_duration_seconds"],
                errors="coerce"
            )

            invalid_duration = int(
                (session_duration < 0).sum()
            )

            missing_duration = int(
                session_duration.isna().sum()
            )

            duration_col1, duration_col2, duration_col3 = st.columns(3)

            duration_col1.metric(
                "Sessions Checked",
                f"{len(filtered_sessions):,}"
            )

            duration_col2.metric(
                "Negative Durations",
                f"{invalid_duration:,}"
            )

            duration_col3.metric(
                "Missing Durations",
                f"{missing_duration:,}"
            )

            if invalid_duration == 0:
                st.success(
                    "No negative session durations detected."
                )
            else:
                st.warning(
                    f"{invalid_duration:,} sessions have negative durations."
                )

        else:

            st.info(
                "Session duration data is not available."
            )

        st.markdown("### Event Validation Log")

        if not event_validation_df.empty:

            st.dataframe(
                event_validation_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No event validation log records are available."
            )

        st.caption(
            "Audit results are calculated from the currently filtered "
            "datasets. Missing values are not automatically treated as errors."
        )

    # =========================================================================
    # TAB 2 — DATA EXPLORER
    # =========================================================================

    with explorer_tab:

        st.subheader("Dataset Explorer")

        available_datasets = {
            "Users": filtered_users,
            "Sessions": filtered_sessions,
            "Feature Events": filtered_events,
            "Daily Activity": filtered_daily_activity,
            "Wallet Accounts": wallet_accounts_df,
            "Wallet Ledger": filtered_wallet_ledger,
            "Withdrawals": filtered_withdrawals,
            "Referrals": filtered_referrals,
            "Event Catalog": event_catalog_df,
            "Event Validation Log": event_validation_df
        }

        explorer_source = st.radio(
            "Select data source",
            [
                "Dashboard Dataset",
                "Upload CSV / Excel"
            ],
            horizontal=True,
            key="explorer_source"
        )

        selected_explorer_df = pd.DataFrame()
        selected_dataset_name = "No dataset selected"

        if explorer_source == "Dashboard Dataset":

            selected_dataset_name = st.selectbox(
                "Choose dataset",
                list(available_datasets.keys()),
                key="explorer_dataset"
            )

            selected_explorer_df = available_datasets[
                selected_dataset_name
            ].copy()

        else:

            uploaded_file = st.file_uploader(
                "Upload CSV or Excel file",
                type=["csv", "xlsx", "xls"],
                key="analytics_file_upload"
            )

            if uploaded_file is not None:

                try:

                    file_extension = uploaded_file.name.lower()

                    if file_extension.endswith(".csv"):

                        selected_explorer_df = pd.read_csv(
                            uploaded_file
                        )

                    else:

                        selected_explorer_df = pd.read_excel(
                            uploaded_file
                        )

                    selected_dataset_name = uploaded_file.name

                    st.success(
                        f"Successfully loaded: {uploaded_file.name}"
                    )

                except Exception as error:

                    st.error(
                        f"Unable to read uploaded file: {error}"
                    )

                    selected_explorer_df = pd.DataFrame()

        if selected_explorer_df is not None:

            if not selected_explorer_df.empty:

                st.markdown("### Dataset Summary")

                row_count = len(selected_explorer_df)
                column_count = len(selected_explorer_df.columns)

                explorer_col1, explorer_col2, explorer_col3 = st.columns(3)

                explorer_col1.metric(
                    "Total Rows",
                    f"{row_count:,}"
                )

                explorer_col2.metric(
                    "Total Columns",
                    f"{column_count:,}"
                )

                explorer_col3.metric(
                    "Memory Usage",
                    f"{selected_explorer_df.memory_usage(deep=True).sum() / 1024:.2f} KB"
                )

                st.markdown("### Dataset Preview")

                if row_count > 10:

                    preview_rows = st.slider(
                        "Number of preview rows",
                        min_value=10,
                        max_value=min(1000, row_count),
                        value=min(100, row_count),
                        step=10,
                        key="preview_row_count"
                    )

                else:

                    preview_rows = row_count

                st.dataframe(
                    selected_explorer_df.head(preview_rows),
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("### Column Information")

                column_info = pd.DataFrame({
                    "Column": selected_explorer_df.columns,
                    "Data Type": [
                        str(dtype)
                        for dtype in selected_explorer_df.dtypes
                    ],
                    "Missing Values": [
                        int(selected_explorer_df[column].isna().sum())
                        for column in selected_explorer_df.columns
                    ],
                    "Unique Values": [
                        int(selected_explorer_df[column].nunique())
                        for column in selected_explorer_df.columns
                    ]
                })

                st.dataframe(
                    column_info,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("### Missing Value Analysis")

                missing_analysis = (
                    selected_explorer_df.isna()
                    .sum()
                    .reset_index()
                )

                missing_analysis.columns = [
                    "Column",
                    "Missing Values"
                ]

                missing_analysis = missing_analysis[
                    missing_analysis["Missing Values"] > 0
                ]

                if not missing_analysis.empty:

                    fig_missing = px.bar(
                        missing_analysis,
                        x="Column",
                        y="Missing Values",
                        title="Missing Values by Column"
                    )

                    fig_missing = style_fig(fig_missing)

                    st.plotly_chart(
                        fig_missing,
                        use_container_width=True
                    )

                else:

                    st.success(
                        "No missing values detected in this dataset."
                    )

                st.markdown("### Download Selected Dataset")

                csv_data = selected_explorer_df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="Download Dataset as CSV",
                    data=csv_data,
                    file_name=f"{selected_dataset_name.replace(' ', '_')}.csv",
                    mime="text/csv",
                    key="explorer_download_csv"
                )

            else:

                st.info(
                    "The selected dataset is empty or no file has been uploaded."
                )

    # =========================================================================
    # TAB 3 — REPORTS & EXPORTS
    # =========================================================================

    with reports_tab:

        st.subheader("Analytics Reports & Exports")

        st.markdown(
            "Generate downloadable reports from the datasets currently "
            "available in the dashboard."
        )

        report_summary = pd.DataFrame([
            {
                "Metric": "Total Users",
                "Value": len(filtered_users)
            },
            {
                "Metric": "Total Sessions",
                "Value": len(filtered_sessions)
            },
            {
                "Metric": "Feature Events",
                "Value": len(filtered_events)
            },
            {
                "Metric": "Daily Activity Records",
                "Value": len(filtered_daily_activity)
            },
            {
                "Metric": "Wallet Accounts",
                "Value": len(wallet_accounts_df)
            },
            {
                "Metric": "Wallet Ledger Records",
                "Value": len(filtered_wallet_ledger)
            },
            {
                "Metric": "Withdrawal Records",
                "Value": len(filtered_withdrawals)
            },
            {
                "Metric": "Referral Records",
                "Value": len(filtered_referrals)
            },
            {
                "Metric": "Data Quality Missing Cells",
                "Value": total_missing_cells
            },
            {
                "Metric": "Data Quality Duplicate Rows",
                "Value": total_duplicate_rows
            }
        ])

        st.markdown("### Executive Summary")

        st.dataframe(
            report_summary,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Export Executive Summary")

        report_csv = report_summary.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Executive Summary CSV",
            data=report_csv,
            file_name="veloop_executive_summary.csv",
            mime="text/csv",
            key="executive_summary_csv"
        )

        st.markdown("### Export Complete Analytics Workbook")

        excel_buffer = io.BytesIO()

        try:

            with pd.ExcelWriter(
                excel_buffer,
                engine="openpyxl"
            ) as writer:

                report_summary.to_excel(
                    writer,
                    sheet_name="Executive Summary",
                    index=False
                )

                audit_df.to_excel(
                    writer,
                    sheet_name="Data Quality Audit",
                    index=False
                )

                for sheet_name, dataset in {
                    "Users": filtered_users,
                    "Sessions": filtered_sessions,
                    "Feature Events": filtered_events,
                    "Daily Activity": filtered_daily_activity,
                    "Wallet Accounts": wallet_accounts_df,
                    "Wallet Ledger": filtered_wallet_ledger,
                    "Withdrawals": filtered_withdrawals,
                    "Referrals": filtered_referrals
                }.items():

                    if dataset is not None:

                        dataset.head(100000).to_excel(
                            writer,
                            sheet_name=sheet_name[:31],
                            index=False
                        )

            excel_buffer.seek(0)

            st.download_button(
                label="Download Complete Analytics Workbook",
                data=excel_buffer.getvalue(),
                file_name="veloop_analytics_report.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                key="analytics_workbook_download"
            )

        except Exception as error:

            st.warning(
                "Excel export is unavailable. "
                f"Details: {error}"
            )

            st.info(
                "You can still download the executive summary as CSV."
            )

        st.markdown("### Export Notes")

        st.caption(
            "Exports contain the records currently available to the dashboard. "
            "Date and device filters apply to filtered datasets. "
            "Wallet account records are exported from the loaded account dataset."
        )

    # =========================================================================
    # TAB 4 — SYSTEM INFORMATION
    # =========================================================================

    with system_tab:

        st.subheader("Dashboard System Information")

        st.markdown("### Data Source Status")

        system_col1, system_col2 = st.columns(2)

        system_col1.metric(
            "Current Data Source",
            str(DATA_SOURCE)
        )

        system_col2.metric(
            "PostgreSQL Connection",
            "Connected" if DATABASE_CONNECTED else "Unavailable"
        )

        if DATABASE_CONNECTED:

            st.success(
                "PostgreSQL data was loaded successfully."
            )

        else:

            st.warning(
                "PostgreSQL is unavailable or was not selected. "
                "The dashboard may be using CSV / Excel fallback data."
            )

        if DATABASE_ERROR:

            with st.expander("View Database Diagnostic Details"):

                st.code(
                    str(DATABASE_ERROR),
                    language="text"
                )

        st.markdown("### Dataset Row Counts")

        system_dataset_info = []

        for dataset_name, dataset in available_datasets.items():

            system_dataset_info.append({
                "Dataset": dataset_name,
                "Rows": len(dataset),
                "Columns": len(dataset.columns)
            })

        system_dataset_df = pd.DataFrame(
            system_dataset_info
        )

        st.dataframe(
            system_dataset_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Dashboard Configuration")

        configuration_info = pd.DataFrame([
            {
                "Configuration": "Dashboard",
                "Value": "VELOOP Rewards Analytics"
            },
            {
                "Configuration": "Framework",
                "Value": "Streamlit"
            },
            {
                "Configuration": "Database",
                "Value": "PostgreSQL"
            },
            {
                "Configuration": "Fallback",
                "Value": "CSV / Excel"
            },
            {
                "Configuration": "Visualization",
                "Value": "Plotly"
            },
            {
                "Configuration": "Integrity Notice",
                "Value": "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING"
            }
        ])

        st.dataframe(
            configuration_info,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Data Integrity Notice")

        st.info(
            """
            This dashboard is designed for product analytics,
            business intelligence, and analytical testing.

            Data displayed in this dashboard must be interpreted
            according to its actual source.

            Simulated records must not be represented as verified
            production user activity, real financial transactions,
            or actual reward payouts.
            """
        )


# =============================================================================
# GLOBAL DASHBOARD FOOTER
# Keep this outside all section-specific conditional blocks.
# =============================================================================

st.markdown("---")

footer_col1, footer_col2 = st.columns(2)

with footer_col1:

    st.caption(
        "VELOOP Rewards | Product Analytics & Business Intelligence"
    )

with footer_col2:

    st.caption(
        "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING"
    )

st.caption(
    "Analytics are based on the datasets loaded into the dashboard. "
    "Validate source data and business rules before making operational decisions."
)
