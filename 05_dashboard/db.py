"""
VELOOP REWARDS — STREAMLIT & POSTGRESQL INTEGRATION ENGINE
Provides reusable SQLAlchemy and psycopg2 connection management,
error handling, and query caching for the Streamlit dashboard.
"""

import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def get_connection_config():
    """Extract database configuration from Streamlit secrets or environment variables."""
    # Priority 1: Streamlit secrets (.streamlit/secrets.toml)
    if hasattr(st, "secrets") and "postgres" in st.secrets:
        sec = st.secrets["postgres"]
        return {
            "host": sec.get("host", "127.0.0.1"),
            "port": int(sec.get("port", 5432)),
            "user": sec.get("user", "postgres"),
            "password": sec.get("password", ""),
            "dbname": sec.get("dbname", "veloop_rewards")
        }
    
    # Priority 2: Standard environment variables
    return {
        "host": os.getenv("PGHOST", "127.0.0.1"),
        "port": int(os.getenv("PGPORT", "5432")),
        "user": os.getenv("PGUSER", "postgres"),
        "password": os.getenv("PGPASSWORD", None),
        "dbname": os.getenv("PGDATABASE", "veloop_rewards")
    }

@st.cache_resource
def get_db_engine():
    """Create and cache SQLAlchemy engine with connection pooling."""
    cfg = get_connection_config()
    if not cfg["password"]:
        return None, "No password configured in environment (PGPASSWORD) or Streamlit secrets."
    
    try:
        url = f"postgresql+psycopg2://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['dbname']}"
        engine = create_engine(url, pool_pre_ping=True, pool_size=5, max_overflow=10, connect_args={"connect_timeout": 3})
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
        return engine, "Connected successfully."
    except SQLAlchemyError as e:
        return None, f"Connection error: {str(e).splitlines()[0]}"
    except Exception as e:
        return None, f"Unexpected error: {str(e).splitlines()[0]}"

def check_db_health():
    """Check database status and return human-readable diagnostics."""
    engine, msg = get_db_engine()
    if engine is not None:
        return {
            "connected": True,
            "status": "ONLINE",
            "message": "Connected to PostgreSQL database 'veloop_rewards'.",
            "badge_color": "#10B981"
        }
    else:
        return {
            "connected": False,
            "status": "OFFLINE / LOCAL EXCEL FALLBACK",
            "message": f"PostgreSQL not connected ({msg}). Operating in high-speed local CSV/Excel mode.",
            "badge_color": "#F59E0B"
        }

def query_database(sql_query, params=None):
    """Execute SQL query safely and return a pandas DataFrame, or None if unavailable."""
    engine, _ = get_db_engine()
    if engine is None:
        return None
    try:
        with engine.connect() as conn:
            return pd.read_sql(text(sql_query), conn, params=params)
    except Exception as e:
        st.error(f"SQL execution error: {e}")
        return None

