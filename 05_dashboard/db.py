
"""
VELOOP REWARDS — STREAMLIT & POSTGRESQL INTEGRATION
PostgreSQL connection, health diagnostics and table retrieval.
Schema: veloop
Database: veloop_rewards
"""

import os
import streamlit as st
import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from streamlit.errors import StreamlitSecretNotFoundError


# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

SCHEMA_NAME = "veloop"

ALLOWED_TABLES = {
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
    "milestones",
    "task_activity",
    "simulated_user_behavior",
    "data_quality_audit_log",
    "stg_daily_activity_cleaned",
    "stg_feature_events_cleaned",
    "stg_wallet_accounts_simulated",
    "stg_wallet_ledger_simulated",
    "stg_withdrawals_simulated"
}


def get_connection_config():
    """Read PostgreSQL settings from Streamlit secrets or environment."""

    try:
        sec = st.secrets["postgres"]
    except (StreamlitSecretNotFoundError, KeyError):
        sec = None

    if sec is not None:
        return {
            "host": sec.get("host", "127.0.0.1"),
            "port": int(sec.get("port", 5432)),
            "user": sec.get("user", "postgres"),
            "password": sec.get("password", ""),
            "dbname": sec.get("dbname", "veloop_rewards")
        }

    return {
        "host": os.getenv("PGHOST", "127.0.0.1"),
        "port": int(os.getenv("PGPORT", "5432")),
        "user": os.getenv("PGUSER", "postgres"),
        "password": os.getenv("PGPASSWORD", ""),
        "dbname": os.getenv("PGDATABASE", "veloop_rewards")
    }


# =============================================================================
# DATABASE ENGINE
# =============================================================================

@st.cache_resource
def get_db_engine():
    """Create and test the PostgreSQL connection."""

    cfg = get_connection_config()

    if not cfg["password"]:
        return None, "PostgreSQL password is not configured."

    try:

        url = URL.create(
            drivername="postgresql+psycopg2",
            username=cfg["user"],
            password=cfg["password"],
            host=cfg["host"],
            port=cfg["port"],
            database=cfg["dbname"]
        )

        engine = create_engine(
            url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            connect_args={"connect_timeout": 5}
        )

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return engine, "Connected successfully."

    except SQLAlchemyError as e:

        return None, (
            f"Database connection error: {str(e).splitlines()[0]}"
        )

    except Exception as e:

        return None, (
            f"Unexpected error: {str(e).splitlines()[0]}"
        )


# =============================================================================
# DATABASE HEALTH
# =============================================================================

def check_db_health():
    """Return PostgreSQL connection status."""

    engine, msg = get_db_engine()

    if engine is not None:

        return {
            "connected": True,
            "status": "ONLINE",
            "message": "Connected to PostgreSQL database 'veloop_rewards'.",
            "badge_color": "#10B981"
        }

    return {
        "connected": False,
        "status": "OFFLINE / LOCAL EXCEL FALLBACK",
        "message": f"PostgreSQL not connected: {msg}",
        "badge_color": "#F59E0B"
    }


# =============================================================================
# GENERIC SQL QUERY
# =============================================================================

def query_database(sql_query, params=None):
    """Execute SQL and return a DataFrame."""

    engine, msg = get_db_engine()

    if engine is None:
        raise RuntimeError(msg)

    try:

        with engine.connect() as conn:

            return pd.read_sql(
                text(sql_query),
                conn,
                params=params
            )

    except Exception as e:

        raise RuntimeError(
            f"SQL execution error: {str(e)}"
        ) from e


# =============================================================================
# GET TABLE — REQUIRED BY APP.PY
# =============================================================================

def get_table(table_name):
    """
    Retrieve a complete PostgreSQL table as a Pandas DataFrame.

    All tables are read from the 'veloop' schema.
    """

    table_name = str(table_name).strip().lower()

    if table_name not in ALLOWED_TABLES:

        raise ValueError(
            f"Table '{table_name}' is not in the approved table list."
        )

    engine, msg = get_db_engine()

    if engine is None:
        raise RuntimeError(msg)

    sql_query = (
        f'SELECT * FROM "{SCHEMA_NAME}"."{table_name}"'
    )

    try:

        with engine.connect() as conn:

            dataframe = pd.read_sql(
                text(sql_query),
                conn
            )

        return dataframe

    except Exception as e:

        raise RuntimeError(
            f"Unable to load table '{SCHEMA_NAME}.{table_name}': {str(e)}"
        ) from e


# =============================================================================
# TABLE ROW COUNT
# =============================================================================

def get_table_count(table_name):
    """Return the number of records in an approved table."""

    table_name = str(table_name).strip().lower()

    if table_name not in ALLOWED_TABLES:
        raise ValueError("Table is not approved.")

    engine, msg = get_db_engine()

    if engine is None:
        raise RuntimeError(msg)

    sql_query = (
        f'SELECT COUNT(*) FROM "{SCHEMA_NAME}"."{table_name}"'
    )

    with engine.connect() as conn:

        return int(
            conn.execute(text(sql_query)).scalar_one()
        )
