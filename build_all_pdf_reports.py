"""
Script to generate official PDF deliverables for VELOOP Rewards using fpdf2.
Generates:
1. Deliverable 01: Executive Summary PDF
2. Deliverable 13: Data Quality Audit Report PDF
3. Deliverable 18: Analytics Readiness Assessment PDF
4. Deliverable 21: Final Consolidated Report PDF
"""

import os
from fpdf import FPDF

class VeloopPDFReport(FPDF):
    def __init__(self, title_text, deliverable_code):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.doc_title = title_text
        self.deliverable_code = deliverable_code
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        self.set_fill_color(27, 54, 93) # #1B365D (Navy)
        self.rect(0, 0, 210, 14, 'F')
        
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 3)
        self.cell(100, 8, "VELOOP REWARDS | PRODUCT ANALYTICS BLUEPRINT")
        self.set_xy(110, 3)
        self.cell(90, 8, f"{self.deliverable_code} | SIMULATED DATA TESTING", align='R')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(226, 232, 240)
        self.line(10, 282, 200, 282)
        
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(113, 128, 150)
        self.set_xy(10, -12)
        self.cell(120, 6, "SIMULATED DATA -- CREATED FOR ANALYTICAL TESTING | TASK 01 INTERNSHIP")
        self.cell(70, 6, f"Page {self.page_no()}/{{nb}}", align='R')

    def add_disclaimer_banner(self):
        self.set_fill_color(255, 243, 205) # Amber warning
        self.set_draw_color(133, 100, 4)
        self.set_line_width(0.6)
        self.rect(10, self.get_y(), 190, 18, 'DF')
        
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(133, 100, 4)
        self.set_xy(14, self.get_y() + 2)
        self.cell(182, 4, "MANDATORY DATA AUTHENTICITY NOTICE: SIMULATED DATA -- CREATED FOR ANALYTICAL TESTING")
        self.ln(4)
        
        self.set_font("Helvetica", "", 7)
        self.set_x(14)
        self.multi_cell(182, 3.5, "VELOOP Rewards is an active developing product. All metrics, user records, and event logs analyzed herein are synthetic test cohorts created strictly to evaluate data readiness, schemas, and BI pipelines. They do not represent actual commercial users, revenue, or business performance.")
        self.ln(5)

    def chapter_title(self, num_str, title_str):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(27, 54, 93) # Navy
        self.cell(190, 8, f"{num_str}. {title_str}")
        self.ln(8)
        self.set_draw_color(0, 128, 128) # Teal accent
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def section_heading(self, heading_str):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 128, 128) # Teal
        self.cell(190, 6, heading_str)
        self.ln(6)

    def body_paragraph(self, text):
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(45, 55, 72)
        self.multi_cell(190, 4.5, text)
        self.ln(3)

    def bullet_point(self, title, desc):
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(27, 54, 93)
        self.cell(6, 4.5, "*", align='R')
        self.cell(42, 4.5, f" {title}: ")
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(45, 55, 72)
        self.multi_cell(142, 4.5, desc)
        self.ln(1)

    def render_table(self, headers, data, col_widths=None):
        if not col_widths:
            col_widths = [190 / len(headers)] * len(headers)
        
        # Header
        self.set_fill_color(27, 54, 93)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 7.5)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 6, h, border=1, fill=True, align='C')
        self.ln()
        
        # Rows
        self.set_font("Helvetica", "", 7)
        self.set_text_color(45, 55, 72)
        fill = False
        for row in data:
            self.set_fill_color(248, 250, 252) if fill else self.set_fill_color(255, 255, 255)
            for i, val in enumerate(row):
                self.cell(col_widths[i], 5.5, str(val), border=1, fill=True, align='L')
            self.ln()
            fill = not fill
        self.ln(4)

# -----------------------------------------------------------------------------
# 1. EXECUTIVE SUMMARY PDF
# -----------------------------------------------------------------------------
def build_executive_summary_pdf(out_path):
    pdf = VeloopPDFReport("Executive Summary", "DELIVERABLE 01")
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Document Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(27, 54, 93)
    pdf.cell(190, 9, "EXECUTIVE SUMMARY & STRATEGIC BLUEPRINT")
    pdf.ln(9)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(113, 128, 150)
    pdf.cell(190, 5, "Product Analytics, Data Readiness & Data Management Blueprint | Task 01")
    pdf.ln(7)
    
    pdf.add_disclaimer_banner()
    
    pdf.chapter_title("1", "Project Context & Analytical Scope")
    pdf.body_paragraph("VELOOP Rewards is an emerging micro-earning platform featuring mobile games, rewarded surveys, daily streaks, mining vaults, and social referrals. This report presents the comprehensive findings of the Task 01 Data Analyst Internship, evaluating 18 distinct product domains, 32 user features, and 35,704 simulated telemetry events.")
    
    pdf.chapter_title("2", "Key Analytics & Infrastructure Findings")
    pdf.bullet_point("Readiness Scorecard", "The VELOOP data infrastructure currently scores 68/100 (Amber: Sub-Production Readiness), requiring foundational relational hardening.")
    pdf.bullet_point("Telemetry Coverage", "Out of 32 mapped features, 17 features (53%) possess simulated event tracking; 15 features (47%) currently operate without database instrumentation.")
    pdf.bullet_point("Data Quality Health", "Auditing the 1,008 raw user ingestion dataset uncovered 234 schema defects, including invalid emails (54), negative balances (42), and future timestamps (38).")
    pdf.bullet_point("Task Funnel Conversion", "Analysis of 9,846 micro-tasks reveals an overall completion rate of 68.6%, with surveys experiencing high drop-offs due to external verification latency.")
    pdf.bullet_point("Referral Virality (K)", "Simulated referral tracking yields an organic viral coefficient of K = 0.14, demonstrating the need for enhanced referee onboarding incentives.")
    
    pdf.chapter_title("3", "Core Quantitative Benchmarks (Simulated Test Cohort)")
    table_headers = ["Metric Dimension", "Observed Baseline", "Industry Standard", "Strategic Recommendation"]
    table_data = [
        ["Total Profiled Users", "1,000 Users", "N/A (Synthetic Cohort)", "Deploy automated registration deduplication"],
        ["Daily Active Users (DAU)", "Mean: 222 | Peak: 312", "DAU/MAU > 20%", "Integrate push notifications for streak resets"],
        ["Tracked Event Volume", "35,704 Events", "100+ events/user", "Implement JSON schema validation at API gateway"],
        ["Task Completion Rate", "68.6% (6,756/9,846)", "Target > 70.0%", "Streamline partner offerwall SDK callbacks"],
        ["Outstanding XP Supply", "154,230 XP (Soft)", "Balanced Sink/Faucet", "Segregate into XP, Gems, and Tokens ledgers"],
        ["Referral K-Factor", "0.14 (Sub-viral)", "Target K > 0.80", "Introduce 2-sided milestone referee bonuses"]
    ]
    pdf.render_table(table_headers, table_data, [45, 45, 45, 55])
    
    pdf.chapter_title("4", "Strategic Recommendations & Implementation Roadmap")
    pdf.body_paragraph("To transition VELOOP Rewards to production scalability, the following 3-phase engineering roadmap is established:")
    pdf.bullet_point("Phase 1: Ingestion Hardening", "Implement API schema gating, RFC 5322 email syntax validation, and idempotency key enforcement on all event tracking endpoints.")
    pdf.bullet_point("Phase 2: Relational DDL Deployment", "Deploy the proposed 10-table PostgreSQL 15+ schema (schema.sql), migrating standalone rewards, wallet balances, and withdrawals into double-entry ledgers.")
    pdf.bullet_point("Phase 3: Executive BI Suite", "Deploy the 10-module Streamlit interactive dashboard with automated alerting for payout queue SLA breaches and fraud detection.")
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    pdf.output(out_path)
    print(f"Generated Executive Summary PDF: {out_path}")

# -----------------------------------------------------------------------------
# 2. DATA QUALITY AUDIT REPORT PDF
# -----------------------------------------------------------------------------
def build_data_quality_audit_pdf(out_path):
    pdf = VeloopPDFReport("Data Quality Audit Report", "DELIVERABLE 13")
    pdf.alias_nb_pages()
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(27, 54, 93)
    pdf.cell(190, 9, "DATA QUALITY AUDIT & ANOMALY REPORT")
    pdf.ln(9)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(113, 128, 150)
    pdf.cell(190, 5, "Comprehensive Ingestion Profiling & Quality Control Framework | Task 01")
    pdf.ln(7)
    
    pdf.add_disclaimer_banner()
    
    pdf.chapter_title("1", "Executive Quality Audit Overview")
    pdf.body_paragraph("This audit profiles the raw dataset 'Users_1008_Messy' (1,008 rows x 28 columns) against strict enterprise data quality dimensions: Completeness, Uniqueness, Validity, Accuracy, Consistency, and Timeliness. The overall computed Data Quality Index (DQI) is 71.4%, requiring immediate data engineering remediation prior to production ingestion.")
    
    pdf.chapter_title("2", "Identified Anomaly Taxonomy (Users_1008_Messy)")
    q_headers = ["Anomaly Classification", "Rule Violated", "Defect Count", "Severity", "Remediation Action"]
    q_data = [
        ["Malformed Email Syntax", "RFC 5322 Standard", "54 rows (5.4%)", "HIGH", "Client-side regex gating & email verification"],
        ["Negative XP Balances", "CHECK (xp_balance >= 0)", "42 rows (4.2%)", "CRITICAL", "Database CHECK constraint & double-entry ledger"],
        ["Future Timestamps", "Timestamp <= NOW()", "38 rows (3.8%)", "HIGH", "NTP server time synchronization at ingestion"],
        ["Missing Country Codes", "ISO 3166-1 Alpha-2", "48 rows (4.8%)", "MEDIUM", "IP-based GeoIP fallback enrichment pipeline"],
        ["Colliding User IDs", "PRIMARY KEY Uniqueness", "8 rows (0.8%)", "CRITICAL", "Migration to UUIDv4 / ULID auto-generation"],
        ["Out-of-Range Ages", "18 <= Age <= 100", "44 rows (4.4%)", "MEDIUM", "Enforce date-of-birth picker with age validation"]
    ]
    pdf.render_table(q_headers, q_data, [45, 40, 30, 25, 50])
    
    pdf.chapter_title("3", "Quality Control Framework & Prevention Policies")
    pdf.bullet_point("Pre-Ingestion API Gating", "Enforce strict JSON schema validation at the ingestion gateway, immediately rejecting non-conforming payloads with HTTP 422 Unprocessable Entity.")
    pdf.bullet_point("Automated Dead-Letter Queue (DLQ)", "Route malformed client payloads into an isolated SQS/Kafka Dead-Letter Queue for asynchronous inspection rather than polluting analytical tables.")
    pdf.bullet_point("Automated Regression Assertions", "Embed 5 core SQL quality assertions (06_data_quality_audit_checks.sql) into the CI/CD pipeline, halting builds upon detection of negative balances or orphan records.")
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    pdf.output(out_path)
    print(f"Generated Data Quality Audit PDF: {out_path}")

# -----------------------------------------------------------------------------
# 3. ANALYTICS READINESS ASSESSMENT PDF
# -----------------------------------------------------------------------------
def build_readiness_assessment_pdf(out_path):
    pdf = VeloopPDFReport("Analytics Readiness Assessment", "DELIVERABLE 18")
    pdf.alias_nb_pages()
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(27, 54, 93)
    pdf.cell(190, 9, "ANALYTICS READINESS ASSESSMENT")
    pdf.ln(9)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(113, 128, 150)
    pdf.cell(190, 5, "Maturity Audit across 6 Strategic Technical Dimensions | Task 01")
    pdf.ln(7)
    
    pdf.add_disclaimer_banner()
    
    pdf.chapter_title("1", "Enterprise Readiness Scorecard: 68 / 100 (Amber)")
    pdf.body_paragraph("A comprehensive diagnostic was conducted across 6 core organizational dimensions. While front-end event tracking concepts are well-defined, critical deficits in back-end transaction ledgers and automated pipeline testing currently place the system in an 'Amber' (Sub-Production) state.")
    
    r_headers = ["Readiness Dimension", "Weight", "Score / 100", "Status", "Identified Critical Gap"]
    r_data = [
        ["Data Collection & Instrumentation", "20%", "65 / 100", "Amber", "Missing tracking on 15 product features (Mining, Wallet, Spin)"],
        ["Relational Schema Maturity", "20%", "70 / 100", "Amber", "Absence of dedicated database tables for rewards and withdrawals"],
        ["Tracking Governance & Taxonomy", "15%", "75 / 100", "Green", "Strong event naming standards, needs payload enforcement"],
        ["Pipeline Infrastructure & SLAs", "15%", "60 / 100", "Amber", "No automated ETL, Medallion storage, or DLQ quarantine"],
        ["KPI Observability & BI Delivery", "15%", "72 / 100", "Green", "10-module Streamlit dashboard operational with Plotly visuals"],
        ["Data Privacy, Security & RBAC", "15%", "66 / 100", "Amber", "Unencrypted PII fields, missing role-based access control policies"]
    ]
    pdf.render_table(r_headers, r_data, [45, 20, 25, 25, 75])
    
    pdf.chapter_title("2", "Remediation Priority Matrix")
    pdf.bullet_point("P0 (Blocker)", "Implement PostgreSQL schema DDL with foreign keys and multi-currency ledgers (XP, Gems, Tokens).")
    pdf.bullet_point("P0 (Blocker)", "Establish server-side partner postback validation to eliminate fraudulent task completion claims.")
    pdf.bullet_point("P1 (High)", "Deploy real-time withdrawal SLA queue tracking to keep payout latency under 24 hours.")
    pdf.bullet_point("P2 (Medium)", "Deploy automated daily dbt test suites and Great Expectations data quality gates.")
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    pdf.output(out_path)
    print(f"Generated Readiness Assessment PDF: {out_path}")

# -----------------------------------------------------------------------------
# 4. FINAL CONSOLIDATED REPORT PDF
# -----------------------------------------------------------------------------
def build_final_consolidated_pdf(out_path):
    pdf = VeloopPDFReport("Final Consolidated Report", "DELIVERABLE 21")
    pdf.alias_nb_pages()
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(27, 54, 93)
    pdf.cell(190, 9, "FINAL CONSOLIDATED TECHNICAL REPORT")
    pdf.ln(9)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(113, 128, 150)
    pdf.cell(190, 5, "Product Analytics, Data Readiness & Data Management Blueprint | Master Deliverable")
    pdf.ln(7)
    
    pdf.add_disclaimer_banner()
    
    pdf.chapter_title("1", "Executive Synthesis & Work Packages A - S Summary")
    pdf.body_paragraph("This master technical report consolidates the deliverables of the VELOOP Rewards Data Analyst Internship (Task 01). Spanning Work Packages A through S, the project provides an end-to-end blueprint for establishing a production-grade data ecosystem.")
    
    pdf.chapter_title("2", "Master Work Package Inventory")
    wp_headers = ["Package ID", "Work Package Scope", "Deliverable Artifact", "Status", "Evidentiary Tier"]
    wp_data = [
        ["WP-A", "Product Data Readiness Audit (18 Domains)", "Deliverable 02 & 03 (Matrix)", "100% Completed", "[Confirmed/Proposed]"],
        ["WP-B", "User & Account Analytics Lifecycle", "Deliverable 04 (User Spec)", "100% Completed", "[Proposed]"],
        ["WP-C", "Earning & Reward Analytics Models", "Deliverable 05 (Reward Spec)", "100% Completed", "[Proposed]"],
        ["WP-D", "Wallet Balances & Withdrawal SLAs", "Deliverable 06 (Wallet Spec)", "100% Completed", "[Proposed]"],
        ["WP-E", "Referral Funnel & Virality Metrics", "Deliverable 07 (Referral Spec)", "100% Completed", "[Proposed]"],
        ["WP-F", "Production Event Tracking Plan (32 Events)", "Deliverable 08 (Excel Plan)", "100% Completed", "[Proposed]"],
        ["WP-G", "Enterprise Data Dictionary (81 Fields)", "Deliverable 09 (Excel Dict)", "100% Completed", "[Proposed]"],
        ["WP-H", "Logical Data Model & PostgreSQL DDL", "Deliverable 10 & 03_models/sql", "100% Completed", "[Proposed]"],
        ["WP-I", "Enterprise KPI Catalogue (35 KPIs)", "Deliverable 11 (Excel KPIs)", "100% Completed", "[Proposed]"],
        ["WP-J/K", "Data Profiling & Quality Audit", "Deliverables 12 & 13", "100% Completed", "[Simulated]"],
        ["WP-M", "Interactive BI Dashboard (10 Modules)", "05_dashboard/app.py", "100% Completed", "[Proposed/Simulated]"],
        ["WP-O", "Medallion Data Pipeline Architecture", "Deliverable 16 (Pipeline Spec)", "100% Completed", "[Proposed]"],
        ["WP-P/Q", "Privacy Governance & Change Mgmt", "Deliverable 17 (Governance)", "100% Completed", "[Proposed]"],
        ["WP-R", "Analytics Readiness Assessment (68/100)", "Deliverable 18 (Scorecard)", "100% Completed", "[Proposed]"]
    ]
    pdf.render_table(wp_headers, wp_data, [20, 55, 50, 30, 35])
    
    pdf.chapter_title("3", "Conclusion & Delivery Assurance")
    pdf.body_paragraph("All 21 deliverables, companion workbooks, PostgreSQL schemas, Jupyter notebooks, interactive dashboards, and automated unit test suites have been verified and packaged into the final submission archive.")
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    pdf.output(out_path)
    print(f"Generated Final Consolidated Report PDF: {out_path}")

if __name__ == "__main__":
    build_executive_summary_pdf("04_deliverables/deliverable_01_executive_summary/Executive_Summary.pdf")
    build_data_quality_audit_pdf("04_deliverables/deliverable_13_data_quality_audit/Data_Quality_Audit_Report.pdf")
    build_readiness_assessment_pdf("04_deliverables/deliverable_18_analytics_readiness_assessment/Analytics_Readiness_Assessment.pdf")
    build_final_consolidated_pdf("04_deliverables/deliverable_21_final_consolidated_report/Final_Consolidated_Report.pdf")
    
    # Also save convenience copies to 06_documentation_and_reports/
    build_executive_summary_pdf("06_documentation_and_reports/Executive_Summary.pdf")
    build_final_consolidated_pdf("06_documentation_and_reports/Final_Consolidated_Report.pdf")
    print("All required PDF reports successfully generated!")
