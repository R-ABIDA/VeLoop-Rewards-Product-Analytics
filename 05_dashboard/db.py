
"""
VELOOP REWARDS — POSTGRESQL ONLY
Neon PostgreSQL connection, health diagnostics and table retrieval.

Database: neondb
Schema: veloop
"""

import os
import streamlit as st
import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from streamlit.errors import StreamlitSecretNotFoundError


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

SCHEMA_NAME = "veloop"
DATABASE_NAME = "neondb"

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
    "stg_withdrawals_simulated",
}


# ============================================================
# CONNECTION SETTINGS
# ============================================================

def get_connection_config():
    """Read PostgreSQL settings from Streamlit secrets or environment."""

    try:
        sec = st.secrets["postgres"]
    except (StreamlitSecretNotFoundError, KeyError):
        sec = None

    if sec is not None:
        config = {
            "host": str(sec.get("host", "")).strip(),
            "port": int(sec.get("port", 5432)),
            "user": str(
                sec.get("user", sec.get("username", ""))
            ).strip(),
            "password": str(sec.get("password", "")),
            "dbname": str(
                sec.get("dbname", sec.get("database", DATABASE_NAME))
            ).strip(),
            "sslmode": str(
                sec.get("sslmode", "require")
            ).strip(),
        }

    else:
        config = {
            "host": os.getenv("PGHOST", "").strip(),
            "port": int(os.getenv("PGPORT", "5432")),
            "user": os.getenv("PGUSER", "").strip(),
            "password": os.getenv("PGPASSWORD", ""),
            "dbname": os.getenv(
                "PGDATABASE", DATABASE_NAME
            ).strip(),
            "sslmode": os.getenv(
                "PGSSLMODE", "require"
            ).strip(),
        }

    required_fields = [
        "host",
        "user",
        "password",
        "dbname",
    ]

    missing_fields = [
        field
        for field in required_fields
        if not config[field]
    ]

    if missing_fields:
        raise RuntimeError(
            "Missing PostgreSQL configuration: "
            + ", ".join(missing_fields)
        )

    if config["port"] <= 0 or config["port"] > 65535:
        raise RuntimeError("Invalid PostgreSQL port.")

    if not config["host"]:
        raise RuntimeError("Neon PostgreSQL host is not configured.")

    if "YOUR_" in config["host"].upper():
        raise RuntimeError(
            "Replace the placeholder with your actual Neon host."
        )

    return config


# ============================================================
# DATABASE ENGINE
# ============================================================

@st.cache_resource(show_spinner=False)
def get_db_engine():
    """Create and test the Neon PostgreSQL connection."""

    try:
        config = get_connection_config()

        database_url = URL.create(
            drivername="postgresql+psycopg2",
            username=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"],
            database=config["dbname"],
        )

        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            pool_recycle=1800,
            connect_args={
                "connect_timeout": 10,
                "sslmode": config["sslmode"],
            },
        )

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return engine, (
            f"Connected successfully to PostgreSQL database "
            f"'{config['dbname']}'."
        )

    except SQLAlchemyError as error:
        return None, (
            "PostgreSQL connection error: "
            f"{str(error).splitlines()[0]}"
        )

    except Exception as error:
        return None, (
            "Database configuration or connection error: "
            f"{str(error).splitlines()[0]}"
        )


# ============================================================
# CACHE REFRESH
# ============================================================

def clear_db_cache():
    """Clear the cached PostgreSQL engine and connection result."""

    get_db_engine.clear()


# ============================================================
# DATABASE HEALTH
# ============================================================

def check_db_health():
    """Return the current PostgreSQL connection status."""

    engine, message = get_db_engine()

    if engine is not None:
        return {
            "connected": True,
            "status": "ONLINE",
            "message": message,
            "badge_color": "#10B981",
        }

    return {
        "connected": False,
        "status": "OFFLINE",
        "message": message,
        "badge_color": "#EF4444",
    }


# ============================================================
# SQL QUERY EXECUTION
# ============================================================

def query_database(sql_query, params=None):
    """Execute a SQL query and return a DataFrame."""

    engine, message = get_db_engine()

    if engine is None:
        raise RuntimeError(message)

    try:
        with engine.connect() as connection:
            return pd.read_sql(
                text(sql_query),
                connection,
                params=params,
            )

    except Exception as error:
        raise RuntimeError(
            f"PostgreSQL query failed: {error}"
        ) from error


# ============================================================
# TABLE RETRIEVAL
# ============================================================

def get_table(table_name):
    """Load an approved table from the veloop schema."""

    table_name = str(table_name).strip().lower()

    if table_name not in ALLOWED_TABLES:
        raise ValueError(
            f"Table '{table_name}' is not in the approved table list."
        )

    engine, message = get_db_engine()

    if engine is None:
        raise RuntimeError(message)

    sql_query = (
        f'SELECT * FROM "{SCHEMA_NAME}"."{table_name}"'
    )

    try:
        with engine.connect() as connection:
            return pd.read_sql(
                text(sql_query),
                connection,
            )

    except Exception as error:
        raise RuntimeError(
            f"Unable to load PostgreSQL table "
            f"'{SCHEMA_NAME}.{table_name}': {error}"
        ) from error


# ============================================================
# TABLE ROW COUNT
# ============================================================

def get_table_count(table_name):
    """Return the row count of an approved PostgreSQL table."""

    table_name = str(table_name).strip().lower()

    if table_name not in ALLOWED_TABLES:
        raise ValueError(
            f"Table '{table_name}' is not in the approved table list."
        )

    engine, message = get_db_engine()

    if engine is None:
        raise RuntimeError(message)

    sql_query = (
        f'SELECT COUNT(*) FROM "{SCHEMA_NAME}"."{table_name}"'
    )

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(sql_query)
            ).scalar_one()

        return int(result)

    except Exception as error:
        raise RuntimeError(
            f"Unable to count records in "
            f"'{SCHEMA_NAME}.{table_name}': {error}"
        ) from error
