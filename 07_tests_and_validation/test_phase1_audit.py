"""
VELOOP REWARDS — AUTOMATED TEST SUITE: PHASE 1 AUDIT & FOUNDATIONS
Tests directory structure, raw data preservation, Deliverables 02, 03, 19, and simulation disclaimers.
"""

import os
import unittest
import openpyxl
import pandas as pd

class TestPhase1Audit(unittest.TestCase):
    
    def test_01_directory_scaffolding(self):
        """Verify that all core project directories exist."""
        required_dirs = [
            "01_raw_data",
            "02_processed_data",
            "03_analysis_and_models/sql",
            "03_analysis_and_models/notebooks",
            "03_analysis_and_models/profiling",
            "04_deliverables/deliverable_02_product_data_audit",
            "04_deliverables/deliverable_03_data_coverage_matrix",
            "04_deliverables/deliverable_19_assumption_and_verification_register",
            "05_dashboard",
            "06_documentation_and_reports",
            "07_tests_and_validation",
            "08_presentation"
        ]
        for d in required_dirs:
            self.assertTrue(os.path.exists(d), f"Missing required directory: {d}")

    def test_02_raw_data_preservation(self):
        """Verify that original raw datasets in 01_raw_data/ exist and are preserved."""
        raw_files = [
            "VELoop_Rewards_Data_01.xlsx",
            "VELOOP_Simulated_User_Behavior_1000.xlsx"
        ]
        for f in raw_files:
            preserved = os.path.join("01_raw_data", f)
            self.assertTrue(os.path.exists(preserved), f"Missing preserved file: {preserved}")
            self.assertGreater(os.path.getsize(preserved), 100000, f"Raw file too small: {preserved}")
            orig = os.path.join("Data", f)
            if os.path.exists(orig):
                self.assertEqual(os.path.getsize(orig), os.path.getsize(preserved), f"Size mismatch for {f}")

    def test_03_deliverable_03_excel_integrity(self):
        """Verify Deliverable 03 Data Coverage Matrix Excel structure and contents."""
        path = "04_deliverables/deliverable_03_data_coverage_matrix/Data_Coverage_Matrix.xlsx"
        self.assertTrue(os.path.exists(path), "Deliverable 03 Excel file missing")
        
        wb = openpyxl.load_workbook(path, data_only=True)
        self.assertIn("Data_Coverage_Matrix", wb.sheetnames)
        self.assertIn("Analytics_Gaps_Register", wb.sheetnames)
        
        ws_cov = wb["Data_Coverage_Matrix"]
        self.assertGreaterEqual(ws_cov.max_row, 35, "Coverage matrix should have at least 32 feature rows")
        
        # Verify mandatory simulation label
        banner_disclaimer = ws_cov["A3"].value
        self.assertIn("SIMULATED DATA", banner_disclaimer, "Missing simulated data label in banner")

        ws_gaps = wb["Analytics_Gaps_Register"]
        self.assertGreaterEqual(ws_gaps.max_row, 15, "Gaps register should have at least 10 gap rows")

    def test_04_deliverable_19_register_integrity(self):
        """Verify Deliverable 19 Source and Verification Register Excel."""
        path = "04_deliverables/deliverable_19_assumption_and_verification_register/Source_and_Verification_Register.xlsx"
        self.assertTrue(os.path.exists(path), "Deliverable 19 Excel file missing")
        
        wb = openpyxl.load_workbook(path, data_only=True)
        self.assertIn("Source_Verification_Register", wb.sheetnames)
        ws = wb["Source_Verification_Register"]
        self.assertGreaterEqual(ws.max_row, 10, "Register should have at least 10 tracked items")
        self.assertIn("SIMULATED DATA", ws["A3"].value, "Missing simulated data label")

    def test_05_deliverable_02_markdown_report(self):
        """Verify Deliverable 02 Product Data Readiness Audit report."""
        path = "04_deliverables/deliverable_02_product_data_audit/Product_Data_Readiness_Audit.md"
        self.assertTrue(os.path.exists(path), "Deliverable 02 report missing")
        
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("SIMULATED DATA — CREATED FOR ANALYTICAL TESTING", content)
            self.assertIn("Work Package A", content)
            self.assertIn("Registration", content)
            self.assertIn("Withdrawals", content)
            self.assertIn("Gap 1 [Critical]", content)

    def test_06_actual_record_counts(self):
        """Verify actual record counts calculated from raw data."""
        raw_dir = "01_raw_data" if os.path.exists("01_raw_data") else "Data"
        df_users = pd.read_excel(os.path.join(raw_dir, "VELoop_Rewards_Data_01.xlsx"), sheet_name="Users_1000_Clean")
        self.assertEqual(len(df_users), 1000, "Clean users should have exactly 1000 rows")
        
        df_tasks = pd.read_excel(os.path.join(raw_dir, "VELOOP_Simulated_User_Behavior_1000.xlsx"), sheet_name="05_Task_Activity")
        self.assertEqual(len(df_tasks), 9846, "Task activity should have exactly 9846 rows")
        
        df_events = pd.read_excel(os.path.join(raw_dir, "VELOOP_Simulated_User_Behavior_1000.xlsx"), sheet_name="03_Feature_Events")
        self.assertEqual(len(df_events), 35704, "Feature events should have exactly 35704 rows")

    def test_07_event_discrepancy_forensic_metrics(self):
        """Verify the 10-dimension forensic comparison between 03_Feature_Events and 10_Event_Data_Quality_Audit."""
        raw_dir = "01_raw_data" if os.path.exists("01_raw_data") else "Data"
        behavior_wb = os.path.join(raw_dir, "VELOOP_Simulated_User_Behavior_1000.xlsx")
        
        df_events = pd.read_excel(behavior_wb, sheet_name="03_Feature_Events")
        df_audit = pd.read_excel(behavior_wb, sheet_name="10_Event_Data_Quality_Audit")

        # 1. Row counts
        self.assertEqual(len(df_events), 35704)
        self.assertEqual(len(df_audit), 35714)

        # 2. Unique event IDs
        self.assertEqual(df_events["event_id"].nunique(), 35704)
        self.assertEqual(df_audit["event_id"].nunique(), 35704)

        # 3. Duplicate event IDs in audit sheet
        audit_dupes = df_audit[df_audit.duplicated(subset=["event_id"], keep=False)]
        self.assertEqual(len(audit_dupes), 20, "Audit sheet must have exactly 10 duplicate pairs (20 rows)")
        self.assertEqual(audit_dupes["event_id"].nunique(), 10, "Audit sheet must have exactly 10 unique duplicate event IDs")

        # 4. Compare deduplicated audit against original on feature_name and event_status
        audit_dedup = df_audit.drop_duplicates(subset=["event_id"], keep="first").set_index("event_id")
        orig_indexed = df_events.set_index("event_id")

        feature_diffs = (orig_indexed["feature_name"] != audit_dedup.loc[orig_indexed.index, "feature_name"]).sum()
        self.assertEqual(feature_diffs, 5, "Must have exactly 5 feature_name casing differences")

        status_diffs = (orig_indexed["event_status"] != audit_dedup.loc[orig_indexed.index, "event_status"]).sum()
        self.assertEqual(status_diffs, 4, "Must have exactly 4 event_status differences")

    def test_08_csv_ingestion_referential_integrity(self):
        """Verify that all cleaned CSV files have 100% referential integrity without orphan records."""
        users = pd.read_csv("02_processed_data/users_cleaned.csv")
        sessions = pd.read_csv("02_processed_data/sessions_cleaned.csv")
        events = pd.read_csv("02_processed_data/events_cleaned.csv")
        daily = pd.read_csv("02_processed_data/daily_activity_cleaned.csv")
        tasks = pd.read_csv("02_processed_data/tasks_cleaned.csv")
        milestones = pd.read_csv("02_processed_data/milestones_cleaned.csv")

        user_ids = set(users["user_id"])
        session_ids = set(sessions["session_id"])

        # Referential assertions
        self.assertTrue(sessions["user_id"].isin(user_ids).all(), "Orphan user in sessions")
        self.assertTrue(events["user_id"].isin(user_ids).all(), "Orphan user in events")
        self.assertTrue(events["session_id"].isin(session_ids).all(), "Orphan session in events")
        self.assertTrue(daily["user_id"].isin(user_ids).all(), "Orphan user in daily activity")
        self.assertTrue(tasks["user_id"].isin(user_ids).all(), "Orphan user in tasks")
        self.assertTrue(milestones["user_id"].isin(user_ids).all(), "Orphan user in milestones")

if __name__ == "__main__":
    unittest.main()

