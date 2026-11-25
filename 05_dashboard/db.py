
"""
VELOOP REWARDS — STREAMLIT & POSTGRESQL INTEGRATION
Neon PostgreSQL connection, health diagnostics and table retrieval.
Schema: veloop
Database: neondb
"""

import os
import streamlit as st
import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from streamlit.errors import StreamlitSecretNotFoundError


SCHEMA_NAME = "veloop"

ALLOWED_TABLES = {
    "users", "sessions", "feature_events", "daily_activity",
    "wallet_accounts", "wallet_ledger", "withdrawals",
    "referrals", "event_catalog", "event_validation_test_log",
    "milestones", "task_activity", "simulated_user_behavior",
    "data_quality_audit_log", "stg_daily_activity_cleaned",
    "stg_feature_events_cleaned", "stg_wallet_accounts_simulated",
    "stg_wallet_ledger_simulated", "stg_withdrawals_simulated"
}


def get_connection_config():
    """Read Neon settings from Streamlit secrets or environment."""

    try:
        sec = st.secrets["postgres"]
    except (StreamlitSecretNotFoundError, KeyError):
        sec = None

    if sec is not None:
        return {
            "host": sec.get("host", ""),
            "port": int(sec.get("port", 5432)),
            "user": sec.get("user", sec.get("username", "neondb_owner")),
            "password": sec.get("password", ""),
            "dbname": sec.get("dbname", sec.get("database", "neondb")),
            "sslmode": sec.get("sslmode", "require")
        }

    return {
        "host": os.getenv("PGHOST", ""),
        "port": int(os.getenv("PGPORT", "5432")),
        "user": os.getenv("PGUSER", "neondb_owner"),
        "password": os.getenv("PGPASSWORD", ""),
        "dbname": os.getenv("PGDATABASE", "neondb"),
        "sslmode": os.getenv("PGSSLMODE", "require")
    }


@st.cache_resource
def get_db_engine():
    """Create and test the PostgreSQL connection."""

    cfg = get_connection_config()

    if not cfg["host"]:
        return None, "Neon PostgreSQL host is not configured."

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
            connect_args={
                "connect_timeout": 10,
                "sslmode": cfg["sslmode"]
            }
        )

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return engine, "Connected successfully."

    except SQLAlchemyError as e:
        return None, f"Database connection error: {str(e).splitlines()[0]}"

    except Exception as e:
        return None, f"Unexpected error: {str(e).splitlines()[0]}"


def check_db_health():
    engine, msg = get_db_engine()

    if engine is not None:
        return {
            "connected": True,
            "status": "ONLINE",
            "message": "Connected to Neon PostgreSQL.",
            "badge_color": "#10B981"
        }

    return {
        "connected": False,
        "status": "OFFLINE / FALLBACK",
        "message": f"PostgreSQL not connected: {msg}",
        "badge_color": "#F59E0B"
    }


def query_database(sql_query, params=None):
    engine, msg = get_db_engine()

    if engine is None:
        raise RuntimeError(msg)

    try:
        with engine.connect() as conn:
            return pd.read_sql(text(sql_query), conn, params=params)
    except Exception as e:
        raise RuntimeError(f"SQL execution error: {e}") from e


def get_table(table_name):
    table_name = str(table_name).strip().lower()

    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Table '{table_name}' is not approved.")

    engine, msg = get_db_engine()

    if engine is None:
        raise RuntimeError(msg)

    sql_query = f'SELECT * FROM "{SCHEMA_NAME}"."{table_name}"'

    try:
        with engine.connect() as conn:
            return pd.read_sql(text(sql_query), conn)
    except Exception as e:
        raise RuntimeError(
            f"Unable to load table '{SCHEMA_NAME}.{table_name}': {e}"
        ) from e


def get_table_count(table_name):
    table_name = str(table_name).strip().lower()

    if table_name not in ALLOWED_TABLES:
        raise ValueError("Table is not approved.")

    engine, msg = get_db_engine()

    if engine is None:
        raise RuntimeError(msg)

    sql_query = f'SELECT COUNT(*) FROM "{SCHEMA_NAME}"."{table_name}"'

    with engine.connect() as conn:
        return int(conn.execute(text(sql_query)).scalar_one())
