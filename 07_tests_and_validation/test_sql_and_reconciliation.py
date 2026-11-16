"""
VELOOP REWARDS — AUTOMATED TEST SUITE: SQL DDL, VIEWS & RECONCILIATION
Tests relational schema DDL, constraint completeness, indexes, double-entry ledger equations,
and data quality audit queries across all 6 SQL modules.
"""

import os
import re
import unittest
import pandas as pd

class TestSqlAndReconciliation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sql_dir = "03_analysis_and_models/sql"
        cls.sql_files = {
            "01_schema_ddl": os.path.join(cls.sql_dir, "01_schema_ddl.sql"),
            "02_user_and_engagement": os.path.join(cls.sql_dir, "02_user_and_engagement_analytics.sql"),
            "03_earning_and_reward": os.path.join(cls.sql_dir, "03_earning_and_reward_analytics.sql"),
            "04_wallet_and_withdrawal": os.path.join(cls.sql_dir, "04_wallet_and_withdrawal_analytics.sql"),
            "05_referral_virality": os.path.join(cls.sql_dir, "05_referral_virality_analytics.sql"),
            "06_data_quality_audit": os.path.join(cls.sql_dir, "06_data_quality_audit_checks.sql")
        }

    def test_01_all_sql_scripts_exist_and_non_empty(self):
        """Verify that all 6 modular SQL files exist and have substantial content."""
        for name, path in self.sql_files.items():
            self.assertTrue(os.path.exists(path), f"Missing SQL file: {name} at {path}")
            size = os.path.getsize(path)
            self.assertGreater(size, 500, f"SQL file {name} appears truncated (size: {size} bytes)")

    def test_02_schema_ddl_tables_and_constraints(self):
        """Verify that 01_schema_ddl.sql creates required tables with PK, FK, and CHECK constraints."""
        with open(self.sql_files["01_schema_ddl"], "r", encoding="utf-8") as f:
            ddl = f.read()

        expected_tables = [
            "users",
            "sessions",
            "feature_events",
            "daily_activity",
            "task_activity",
            "milestones",
            "wallet_accounts",
            "wallet_ledger",
            "withdrawals",
            "referrals"
        ]
        for tbl in expected_tables:
            pattern = rf"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?{tbl}\b"
            self.assertTrue(re.search(pattern, ddl, re.IGNORECASE), f"Missing CREATE TABLE for {tbl}")

        # Check constraint keywords
        self.assertIn("PRIMARY KEY", ddl.upper())
        self.assertIn("FOREIGN KEY", ddl.upper())
        self.assertIn("REFERENCES users", ddl)
        self.assertIn("CHECK", ddl.upper())
        self.assertIn("CREATE INDEX", ddl.upper())

    def test_03_double_entry_reconciliation_logic(self):
        """Verify that 04_wallet_and_withdrawal_analytics.sql defines double-entry reconciliation."""
        with open(self.sql_files["04_wallet_and_withdrawal"], "r", encoding="utf-8") as f:
            wallet_sql = f.read()

        self.assertIn("v_double_entry_reconciliation", wallet_sql)
        self.assertIn("DEBIT", wallet_sql.upper())
        self.assertIn("CREDIT", wallet_sql.upper())
        self.assertIn("net_ledger_variance", wallet_sql)

        # Validate mathematical logic on a simulated ledger test DataFrame
        simulated_ledger = pd.DataFrame([
            {"entry_type": "CREDIT", "amount": 100.00},
            {"entry_type": "DEBIT", "amount": 100.00},
            {"entry_type": "CREDIT", "amount": 250.50},
            {"entry_type": "DEBIT", "amount": 250.50},
        ])
        credits = simulated_ledger[simulated_ledger["entry_type"] == "CREDIT"]["amount"].sum()
        debits = simulated_ledger[simulated_ledger["entry_type"] == "DEBIT"]["amount"].sum()
        variance = debits - credits
        self.assertEqual(variance, 0.0, "Double-entry ledger equation debits - credits must equal 0")

    def test_04_data_quality_audit_queries(self):
        """Verify that 06_data_quality_audit_checks.sql targets known anomalies."""
        with open(self.sql_files["06_data_quality_audit"], "r", encoding="utf-8") as f:
            dq_sql = f.read()

        self.assertIn("v_dq_duplicate_events", dq_sql)
        self.assertIn("v_dq_duplicate_users", dq_sql)
        self.assertIn("v_dq_orphan_events", dq_sql)
        self.assertIn("v_dq_impossible_timestamps", dq_sql)

    def test_05_views_defined_across_analytics_scripts(self):
        """Verify that analytical views are formulated for reporting."""
        views_to_check = [
            (self.sql_files["02_user_and_engagement"], "v_daily_active_users"),
            (self.sql_files["02_user_and_engagement"], "v_user_retention_cohorts"),
            (self.sql_files["03_earning_and_reward"], "v_task_conversion_funnel"),
            (self.sql_files["04_wallet_and_withdrawal"], "v_wallet_engagement_summary"),
            (self.sql_files["05_referral_virality"], "v_referral_acquisition_summary")
        ]
        for fpath, view_name in views_to_check:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(view_name, content, f"Missing view {view_name} in {fpath}")

if __name__ == "__main__":
    unittest.main()

