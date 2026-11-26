
"""
VELOOP REWARDS — NEON POSTGRESQL CONNECTION
Database: neondb
Schema: veloop
"""

import os
import streamlit as st
import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from streamlit.errors import StreamlitSecretNotFoundError

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


def get_connection_config():
    try:
        sec = st.secrets["postgres"]
    except (StreamlitSecretNotFoundError, KeyError):
        sec = None

    if sec is not None:
        cfg = {
            "host": str(sec.get("host", "")).strip(),
            "port": int(sec.get("port", 5432)),
            "user": str(sec.get("user", "")).strip(),
            "password": str(sec.get("password", "")),
            "dbname": str(sec.get("dbname", DATABASE_NAME)).strip(),
            "sslmode": str(sec.get("sslmode", "require")).strip(),
        }
    else:
        cfg = {
            "host": os.getenv("PGHOST", "").strip(),
            "port": int(os.getenv("PGPORT", "5432")),
            "user": os.getenv("PGUSER", "").strip(),
            "password": os.getenv("PGPASSWORD", ""),
            "dbname": os.getenv("PGDATABASE", DATABASE_NAME).strip(),
            "sslmode": os.getenv("PGSSLMODE", "require").strip(),
        }

    required = ["host", "user", "password", "dbname"]
    missing = [key for key in required if not cfg[key]]

    if missing:
        raise RuntimeError(
            "Missing PostgreSQL configuration: " + ", ".join(missing)
        )

    if "YOUR_" in cfg["host"].upper():
        raise RuntimeError("Invalid Neon hostname.")

    return cfg


@st.cache_resource
def get_db_engine():
    try:
        cfg = get_connection_config()

        url = URL.create(
            drivername="postgresql+psycopg2",
            username=cfg["user"],
            password=cfg["password"],
            host=cfg["host"],
            port=cfg["port"],
            database=cfg["dbname"],
        )

        engine = create_engine(
            url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            connect_args={
                "connect_timeout": 10,
                "sslmode": cfg["sslmode"],
            },
        )

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return engine, "Connected successfully to Neon PostgreSQL."

    except Exception as exc:
        return None, f"PostgreSQL connection failed: {str(exc).splitlines()[0]}"


def clear_db_cache():
    get_db_engine.clear()


def check_db_health():
    engine, message = get_db_engine()

    if engine is not None:
        return {
            "connected": True,
            "status": "ONLINE",
            "message": f"Connected to PostgreSQL database '{DATABASE_NAME}'.",
            "badge_color": "#10B981",
        }

    return {
        "connected": False,
        "status": "OFFLINE",
        "message": message,
        "badge_color": "#EF4444",
    }


def query_database(sql_query, params=None):
    engine, message = get_db_engine()

    if engine is None:
        raise RuntimeError(message)

    try:
        with engine.connect() as conn:
            return pd.read_sql(text(sql_query), conn, params=params)
    except Exception as exc:
        raise RuntimeError(
            f"PostgreSQL query failed: {exc}"
        ) from exc


def get_table(table_name):
    table_name = str(table_name).strip().lower()

    if table_name not in ALLOWED_TABLES:
        raise ValueError(
            f"Table '{table_name}' is not in the approved table list."
        )

    engine, message = get_db_engine()

    if engine is None:
        raise RuntimeError(message)

    sql_query = f'SELECT * FROM "{SCHEMA_NAME}"."{table_name}"'

    try:
        with engine.connect() as conn:
            return pd.read_sql(text(sql_query), conn)
    except Exception as exc:
        raise RuntimeError(
            f"Unable to load PostgreSQL table "
            f"'{SCHEMA_NAME}.{table_name}': {exc}"
        ) from exc


def get_table_count(table_name):
    table_name = str(table_name).strip().lower()

    if table_name not in ALLOWED_TABLES:
        raise ValueError("Table is not in the approved table list.")

    engine, message = get_db_engine()

    if engine is None:
        raise RuntimeError(message)

    sql_query = f'SELECT COUNT(*) FROM "{SCHEMA_NAME}"."{table_name}"'

    with engine.connect() as conn:
        return int(conn.execute(text(sql_query)).scalar_one())
