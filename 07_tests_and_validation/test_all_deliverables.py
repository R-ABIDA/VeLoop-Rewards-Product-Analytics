"""
VELOOP REWARDS — MASTER AUTOMATED TEST SUITE
Validates that all 21 official deliverables, schemas, Excel workbooks, cleaned datasets,
Jupyter notebooks, evidence charts, PowerPoint presentation, PDF reports, and 10 dashboard
modules exist, compile, and adhere to data authenticity standards.
"""

import os
import unittest
import openpyxl
import pandas as pd
import py_compile
import nbformat as nbf

class TestAllDeliverables(unittest.TestCase):

    def test_01_all_21_deliverables_exist(self):
        """Verify that every one of the 21 official required deliverables exists on disk."""
        deliverable_paths = {
            "01_Executive_Summary": "04_deliverables/deliverable_01_executive_summary/Executive_Summary.md",
            "02_Product_Data_Audit": "04_deliverables/deliverable_02_product_data_audit/Product_Data_Readiness_Audit.md",
            "03_Data_Coverage_Matrix": "04_deliverables/deliverable_03_data_coverage_matrix/Data_Coverage_Matrix.xlsx",
            "04_User_Analytics_Spec": "04_deliverables/deliverable_04_user_analytics_spec/User_Analytics_Specification.md",
            "05_Reward_Analytics_Spec": "04_deliverables/deliverable_05_reward_analytics_spec/Reward_Analytics_Specification.md",
            "06_Wallet_Withdrawal_Spec": "04_deliverables/deliverable_06_wallet_withdrawal_spec/Wallet_Withdrawal_Specification.md",
            "07_Referral_Engagement_Spec": "04_deliverables/deliverable_07_referral_engagement_analytics/Referral_Engagement_Analytics.md",
            "08_Event_Tracking_Plan": "04_deliverables/deliverable_08_event_tracking_plan/Event_Tracking_Plan.xlsx",
            "09_Data_Dictionary": "04_deliverables/deliverable_09_data_dictionary/Data_Dictionary.xlsx",
            "10_Logical_Data_Model_SQL": "04_deliverables/deliverable_10_logical_data_model/schema.sql",
            "10_Logical_Data_Model_Doc": "04_deliverables/deliverable_10_logical_data_model/Logical_Data_Model_and_ER_Diagram.md",
            "11_KPI_Catalogue": "04_deliverables/deliverable_11_kpi_catalogue/KPI_Catalogue.xlsx",
            "12_Simulated_Data_Profiling": "04_deliverables/deliverable_12_simulated_data_profiling/Simulated_Data_Profiling_Workbook.xlsx",
            "13_Data_Quality_Audit": "04_deliverables/deliverable_13_data_quality_audit/Data_Quality_Audit_Workbook.xlsx",
            "14_Dashboard_Blueprint": "04_deliverables/deliverable_14_dashboard_blueprint/Dashboard_Blueprint_Specifications.md",
            "15_Developer_Handoff": "04_deliverables/deliverable_15_developer_handoff/Developer_Analytics_Handoff.md",
            "16_Data_Pipeline_Proposal": "04_deliverables/deliverable_16_data_pipeline_proposal/Data_Pipeline_Proposal.md",
            "17_Privacy_and_Governance": "04_deliverables/deliverable_17_privacy_and_governance/Privacy_Governance_and_Change_Management.md",
            "18_Readiness_Assessment": "04_deliverables/deliverable_18_analytics_readiness_assessment/Analytics_Readiness_Assessment.md",
            "19_Source_Register": "04_deliverables/deliverable_19_assumption_and_verification_register/Source_and_Verification_Register.xlsx",
            "20_Implementation_Backlog": "04_deliverables/deliverable_20_implementation_backlog/Implementation_Backlog.md",
            "21_Final_Consolidated_Report": "04_deliverables/deliverable_21_final_consolidated_report/Final_Consolidated_Report.md"
        }
        
        for name, path in deliverable_paths.items():
            self.assertTrue(os.path.exists(path), f"Missing Deliverable: {name} at {path}")
            self.assertGreater(os.path.getsize(path), 100, f"Deliverable file is too small/empty: {path}")

    def test_02_excel_deliverables_integrity(self):
        """Verify all generated Excel workbooks open and have proper sheet counts."""
        excel_files = [
            ("04_deliverables/deliverable_03_data_coverage_matrix/Data_Coverage_Matrix.xlsx", 2),
            ("04_deliverables/deliverable_08_event_tracking_plan/Event_Tracking_Plan.xlsx", 1),
            ("04_deliverables/deliverable_09_data_dictionary/Data_Dictionary.xlsx", 1),
            ("04_deliverables/deliverable_11_kpi_catalogue/KPI_Catalogue.xlsx", 1),
            ("04_deliverables/deliverable_12_simulated_data_profiling/Simulated_Data_Profiling_Workbook.xlsx", 3),
            ("04_deliverables/deliverable_13_data_quality_audit/Data_Quality_Audit_Workbook.xlsx", 2),
            ("04_deliverables/deliverable_19_assumption_and_verification_register/Source_and_Verification_Register.xlsx", 1)
        ]
        for path, min_sheets in excel_files:
            wb = openpyxl.load_workbook(path, data_only=True)
            self.assertGreaterEqual(len(wb.sheetnames), min_sheets, f"Insufficient sheets in {path}")
            ws = wb.active
            self.assertIn("SIMULATED DATA", str(ws["A3"].value), f"Missing simulation label in banner of {path}")

    def test_03_sql_schema_ddl_and_modular_scripts(self):
        """Verify SQL files in 03_analysis_and_models/sql and Deliverable 10 schema.sql."""
        sql_files = [
            "04_deliverables/deliverable_10_logical_data_model/schema.sql",
            "03_analysis_and_models/sql/01_schema_ddl.sql",
            "03_analysis_and_models/sql/02_user_and_engagement_analytics.sql",
            "03_analysis_and_models/sql/03_earning_and_reward_analytics.sql",
            "03_analysis_and_models/sql/04_wallet_and_withdrawal_analytics.sql",
            "03_analysis_and_models/sql/05_referral_virality_analytics.sql",
            "03_analysis_and_models/sql/06_data_quality_audit_checks.sql"
        ]
        for sp in sql_files:
            self.assertTrue(os.path.exists(sp), f"Missing SQL file: {sp}")
            self.assertGreater(os.path.getsize(sp), 200, f"SQL file too small: {sp}")

    def test_04_processed_datasets(self):
        """Verify cleaned processed datasets exist in 02_processed_data/."""
        self.assertTrue(os.path.exists("02_processed_data/users_cleaned.csv"))
        self.assertTrue(os.path.exists("02_processed_data/events_cleaned.csv"))
        
        df_u = pd.read_csv("02_processed_data/users_cleaned.csv")
        self.assertEqual(len(df_u), 1000, "Cleaned users should have exactly 1000 unique records")
        
        df_e = pd.read_csv("02_processed_data/events_cleaned.csv")
        self.assertEqual(len(df_e), 35704, "Cleaned events should have exactly 35704 records")

    def test_05_dashboard_10_modules_compilation(self):
        """Verify that Streamlit app compiles without Python syntax errors and contains all 10 modules."""
        app_path = "05_dashboard/app.py"
        self.assertTrue(os.path.exists(app_path))
        py_compile.compile(app_path, doraise=True)

        with open(app_path, "r", encoding="utf-8") as f:
            app_code = f.read()

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
            self.assertIn(f'"{m}"', app_code, f"Missing dashboard module: {m}")

    def test_06_jupyter_profiling_notebook(self):
        """Verify that the profiling Jupyter notebook exists, is valid, and has executed outputs."""
        nb_path = "03_analysis_and_models/notebooks/01_simulated_data_profiling.ipynb"
        self.assertTrue(os.path.exists(nb_path), f"Missing notebook: {nb_path}")
        nb = nbf.read(nb_path, as_version=4)
        self.assertGreaterEqual(len(nb.cells), 10, "Notebook should have at least 10 cells")
        
        code_cells = [c for c in nb.cells if c.cell_type == "code"]
        self.assertGreaterEqual(len(code_cells), 8, "Notebook should have at least 8 code cells")
        for c in code_cells:
            self.assertIsNotNone(c.execution_count, "Code cell missing execution_count")
            self.assertGreater(len(c.outputs), 0, "Code cell missing execution output")

    def test_07_evidence_charts_exist(self):
        """Verify that all 6 high-resolution evidence charts exist in 08_evidence_charts/."""
        expected_charts = [
            "08_evidence_charts/01_daily_active_users_trend.png",
            "08_evidence_charts/02_feature_adoption_and_event_volume.png",
            "08_evidence_charts/03_task_execution_status_breakdown.png",
            "08_evidence_charts/04_demographic_age_gender_pyramid.png",
            "08_evidence_charts/05_acquisition_channel_distribution.png",
            "08_evidence_charts/06_analytics_readiness_radar.png"
        ]
        for chart in expected_charts:
            self.assertTrue(os.path.exists(chart), f"Missing evidence chart: {chart}")
            self.assertGreater(os.path.getsize(chart), 10000, f"Chart image file too small: {chart}")

    def test_08_presentation_deck_and_pdf_reports(self):
        """Verify that PPTX, HTML5 presentation, and PDF deliverables exist."""
        self.assertTrue(os.path.exists("08_presentation/VELOOP_Rewards_Final_Presentation.pptx"))
        self.assertTrue(os.path.exists("08_presentation/VELOOP_Rewards_Final_Presentation.html"))
        self.assertTrue(os.path.exists("04_deliverables/deliverable_01_executive_summary/Executive_Summary.pdf"))
        self.assertTrue(os.path.exists("04_deliverables/deliverable_13_data_quality_audit/Data_Quality_Audit_Report.pdf"))
        self.assertTrue(os.path.exists("04_deliverables/deliverable_18_analytics_readiness_assessment/Analytics_Readiness_Assessment.pdf"))
        self.assertTrue(os.path.exists("04_deliverables/deliverable_21_final_consolidated_report/Final_Consolidated_Report.pdf"))

    def test_09_mandatory_simulation_disclaimer_presence(self):
        """Verify that critical documents contain the non-negotiable simulation disclaimer."""
        doc_paths = [
            "04_deliverables/deliverable_01_executive_summary/Executive_Summary.md",
            "04_deliverables/deliverable_02_product_data_audit/Product_Data_Readiness_Audit.md",
            "04_deliverables/deliverable_04_user_analytics_spec/User_Analytics_Specification.md",
            "04_deliverables/deliverable_05_reward_analytics_spec/Reward_Analytics_Specification.md",
            "04_deliverables/deliverable_06_wallet_withdrawal_spec/Wallet_Withdrawal_Specification.md",
            "04_deliverables/deliverable_07_referral_engagement_analytics/Referral_Engagement_Analytics.md",
            "04_deliverables/deliverable_10_logical_data_model/Logical_Data_Model_and_ER_Diagram.md",
            "04_deliverables/deliverable_12_simulated_data_profiling/Simulated_Data_Profiling_Report.md",
            "04_deliverables/deliverable_13_data_quality_audit/Data_Quality_Audit_Report.md",
            "04_deliverables/deliverable_14_dashboard_blueprint/Dashboard_Blueprint_Specifications.md",
            "04_deliverables/deliverable_15_developer_handoff/Developer_Analytics_Handoff.md",
            "04_deliverables/deliverable_16_data_pipeline_proposal/Data_Pipeline_Proposal.md",
            "04_deliverables/deliverable_17_privacy_and_governance/Privacy_Governance_and_Change_Management.md",
            "04_deliverables/deliverable_18_analytics_readiness_assessment/Analytics_Readiness_Assessment.md",
            "04_deliverables/deliverable_20_implementation_backlog/Implementation_Backlog.md",
            "04_deliverables/deliverable_21_final_consolidated_report/Final_Consolidated_Report.md",
            "05_dashboard/app.py"
        ]
        for p in doc_paths:
            with open(p, "r", encoding="utf-8") as f:
                txt = f.read()
                self.assertIn("SIMULATED DATA — CREATED FOR ANALYTICAL TESTING", txt, f"Missing mandatory simulation disclaimer in {p}")

    def test_10_data_dictionary_and_event_plan_counts(self):
        """Verify data dictionary has >= 75 fields and event tracking plan has >= 25 events."""
        df_dd = pd.read_excel("04_deliverables/deliverable_09_data_dictionary/Data_Dictionary.xlsx", skiprows=4)
        self.assertGreaterEqual(len(df_dd), 75, f"Data Dictionary has only {len(df_dd)} fields, expected >= 75")
        
        df_ep = pd.read_excel("04_deliverables/deliverable_08_event_tracking_plan/Event_Tracking_Plan.xlsx", skiprows=4)
        self.assertGreaterEqual(len(df_ep), 25, f"Event Tracking Plan has only {len(df_ep)} events, expected >= 25")

if __name__ == "__main__":
    unittest.main()
