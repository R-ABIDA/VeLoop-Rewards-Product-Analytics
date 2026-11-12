"""
Unit & Functional Test Suite for Streamlit Dashboard Modules, Navigation,
Filters, Charts, Uploads, and Downloads.
File: 07_tests_and_validation/test_dashboard_interactive.py
"""

import os
import io
import unittest
import pandas as pd
import numpy as np
import plotly.graph_objects as go

class TestDashboardInteractivity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load raw data with fallback sheet names
        f_users = "01_raw_data/VELoop_Rewards_Data_01.xlsx"
        if not os.path.exists(f_users):
            f_users = "Data/VELoop_Rewards_Data_01.xlsx"
        f_behavior = "01_raw_data/VELOOP_Simulated_User_Behavior_1000.xlsx"
        if not os.path.exists(f_behavior):
            f_behavior = "Data/VELOOP_Simulated_User_Behavior_1000.xlsx"

        cls.users = pd.read_excel(f_users, sheet_name="Users_1000_Clean")
        try:
            cls.messy_users = pd.read_excel(f_users, sheet_name="Users_Messy_Audit")
        except Exception:
            cls.messy_users = pd.read_excel(f_users, sheet_name="Users_1008_Messy")
            
        cls.sessions = pd.read_excel(f_behavior, sheet_name="02_Sessions")
        cls.events = pd.read_excel(f_behavior, sheet_name="03_Feature_Events")
        cls.daily = pd.read_excel(f_behavior, sheet_name="04_Daily_Activity")
        cls.tasks = pd.read_excel(f_behavior, sheet_name="05_Task_Activity")
        cls.features = pd.read_excel(f_behavior, sheet_name="07_Feature_Usage")

        cls.users["registration_datetime"] = pd.to_datetime(cls.users["registration_datetime"])
        cls.sessions["session_start"] = pd.to_datetime(cls.sessions["session_start"])
        cls.events["event_datetime"] = pd.to_datetime(cls.events["event_datetime"])
        cls.daily["activity_date"] = pd.to_datetime(cls.daily["activity_date"])
        cls.tasks["task_viewed_at"] = pd.to_datetime(cls.tasks["task_viewed_at"])

        if "primary_device" in cls.users.columns:
            cls.users["device"] = cls.users["primary_device"]
        else:
            cls.users["device"] = cls.users.get("platform", "Android")

        if "task_status" in cls.tasks.columns:
            cls.tasks["status"] = cls.tasks["task_status"]

    def test_01_all_10_modules_defined(self):
        """Verify that all 10 requested modules are in app.py."""
        with open("05_dashboard/app.py", "r", encoding="utf-8") as f:
            code = f.read()

        expected_modules = [
            "Overview",
            "User Analytics",
            "Earning & Rewards",
            "Wallet & Withdrawals",
            "Referral Analytics",
            "Event Analytics",
            "Data Quality",
            "Data Explorer",
            "Reports & Exports",
            "Project Information"
        ]
        for m in expected_modules:
            self.assertIn(f'section == "{m}"', code, f"Module condition missing for: {m}")

    def test_02_filters_logic(self):
        """Verify that date interval and device filters work without errors."""
        # Test Android device filter
        android_users = self.users[self.users["device"] == "Android"]
        self.assertGreater(len(android_users), 0)
        valid_ids = set(android_users["user_id"])
        
        filtered_daily = self.daily[self.daily["user_id"].isin(valid_ids)]
        self.assertGreater(len(filtered_daily), 0)
        
        # Test date range slice
        min_d = self.daily["activity_date"].min()
        mid_d = min_d + pd.Timedelta(days=15)
        date_sliced = self.daily[(self.daily["activity_date"] >= min_d) & (self.daily["activity_date"] <= mid_d)]
        self.assertGreater(len(date_sliced), 0)
        self.assertLessEqual(len(date_sliced), len(self.daily))

    def test_03_charts_generation(self):
        """Verify that Plotly figures render properly across modules."""
        import plotly.express as px
        # Overview DAU chart
        dau_trend = self.daily.groupby("activity_date")["user_id"].nunique().reset_index()
        fig_dau = px.line(dau_trend, x="activity_date", y="user_id")
        self.assertIsInstance(fig_dau, go.Figure)

        # User Demographics chart
        fig_acq = px.pie(self.users, names="acquisition_source")
        self.assertIsInstance(fig_acq, go.Figure)

        # Task funnel
        fig_tsk = px.bar(self.tasks["status"].value_counts().reset_index(), x="status", y="count")
        self.assertIsInstance(fig_tsk, go.Figure)

        # Wallet scatter
        fig_scatter = px.scatter(self.users, x="active_days", y="xp_balance")
        self.assertIsInstance(fig_scatter, go.Figure)

    def test_04_csv_and_excel_upload_parsing(self):
        """Verify CSV and Excel upload parsing pipeline."""
        # Simulated CSV bytes
        csv_data = "user_id,xp_balance,platform\nu1,100,Android\nu2,250,iOS\n"
        csv_file = io.StringIO(csv_data)
        df_csv = pd.read_csv(csv_file)
        self.assertEqual(len(df_csv), 2)
        self.assertIn("xp_balance", df_csv.columns)

        # Simulated Excel bytes
        excel_buf = io.BytesIO()
        df_csv.to_excel(excel_buf, index=False)
        excel_buf.seek(0)
        df_excel = pd.read_excel(excel_buf)
        self.assertEqual(len(df_excel), 2)

    def test_05_download_payloads_exist(self):
        """Verify all download buttons have valid, non-empty binary files on disk."""
        required_downloads = [
            "04_deliverables/deliverable_01_executive_summary/Executive_Summary.pdf",
            "04_deliverables/deliverable_13_data_quality_audit/Data_Quality_Audit_Report.pdf",
            "04_deliverables/deliverable_18_analytics_readiness_assessment/Analytics_Readiness_Assessment.pdf",
            "04_deliverables/deliverable_21_final_consolidated_report/Final_Consolidated_Report.pdf",
            "08_presentation/VELOOP_Rewards_Final_Presentation.pptx",
            "08_presentation/VELOOP_Rewards_Final_Presentation.html",
            "04_deliverables/deliverable_03_data_coverage_matrix/Data_Coverage_Matrix.xlsx",
            "04_deliverables/deliverable_08_event_tracking_plan/Event_Tracking_Plan.xlsx",
            "04_deliverables/deliverable_09_data_dictionary/Data_Dictionary.xlsx",
            "04_deliverables/deliverable_11_kpi_catalogue/KPI_Catalogue.xlsx",
            "02_processed_data/users_cleaned.csv",
            "02_processed_data/events_cleaned.csv"
        ]
        for p in required_downloads:
            self.assertTrue(os.path.exists(p), f"Download target missing: {p}")
            self.assertGreater(os.path.getsize(p), 100, f"Download target empty: {p}")

if __name__ == "__main__":
    unittest.main()
