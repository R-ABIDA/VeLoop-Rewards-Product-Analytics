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
        """Verify that original raw datasets in Data/ are preserved in 01_raw_data/."""
        raw_files = [
            "VELoop_Rewards_Data_01.xlsx",
            "VELOOP_Simulated_User_Behavior_1000.xlsx"
        ]
        for f in raw_files:
            orig = os.path.join("Data", f)
            preserved = os.path.join("01_raw_data", f)
            self.assertTrue(os.path.exists(orig), f"Missing original file: {orig}")
            self.assertTrue(os.path.exists(preserved), f"Missing preserved file: {preserved}")
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
        df_users = pd.read_excel("Data/VELoop_Rewards_Data_01.xlsx", sheet_name="Users_1000_Clean")
        self.assertEqual(len(df_users), 1000, "Clean users should have exactly 1000 rows")
        
        df_tasks = pd.read_excel("Data/VELOOP_Simulated_User_Behavior_1000.xlsx", sheet_name="05_Task_Activity")
        self.assertEqual(len(df_tasks), 9846, "Task activity should have exactly 9846 rows")
        
        df_events = pd.read_excel("Data/VELOOP_Simulated_User_Behavior_1000.xlsx", sheet_name="03_Feature_Events")
        self.assertEqual(len(df_events), 35704, "Feature events should have exactly 35704 rows")

if __name__ == "__main__":
    unittest.main()

