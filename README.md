# VELOOP REWARDS — PRODUCT ANALYTICS, DATA READINESS & DATA MANAGEMENT BLUEPRINT

**Organization:** VELOOP Rewards & VELOOP CO.  
**Role:** Senior Data Analyst, Product Analytics Specialist & Analytics Engineer (Data Analyst Intern)  
**Chief Executive Officer:** Ayan Alam  
**Task:** Data Analyst Internship — Task 01 (Comprehensive 21-Deliverable Blueprint)  
**Duration:** 22–25 Days (2 Development Days / 1 Review Day Sprint Rhythm)  
**Integrity Policy:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
**Classification:** Confirmed, Proposed, To Be Verified, Simulated  
**GitHub Repository:** [https://github.com/R-ABIDA/VeLoop-Rewards-Product-Analytics](https://github.com/R-ABIDA/VeLoop-Rewards-Product-Analytics)

---

## 1. Project Overview & Institutional Background

**VELOOP Rewards** is an early-stage consumer digital rewards, gamification, and micro-task monetization ecosystem in active pre-launch development. The platform allows users to engage with rewarded video ads, partner offerwalls, surveys, daily check-in streaks, lucky wheel spins, tap arenas, and cloud mining rigs to accumulate soft rewards (`XP`), premium currency (`Gems`), and platform tokens (`Tokens`) redeemable for real-world fiat cash (UPI, Paytm, Bank Transfer, PayPal) or gift vouchers.

Because VELOOP is currently in active pre-launch development, the platform lacks massive multi-year production event streams. Therefore, this project establishes the **complete analytical architecture, relational data models, event telemetry specifications, data quality control framework, and executive BI dashboard foundations** required to launch, monitor, and scale the business without financial accounting leakage or data corruption.

---

## 2. Business Objectives & Strategic Scope

1. **Product Area & Feature Mapping:** Audit all 18 platform domains and 32 features, mapping client-side User Events to server-side System Events and commercial Business Outcomes.
2. **Relational Data Architecture:** Design a production-grade PostgreSQL 15+ normalized schema (`01_schema_ddl.sql`) enforcing primary keys, foreign keys, check constraints, indexes, and double-entry accounting integrity.
3. **Standardized Event Telemetry Plan:** Formulate 32 standardized production events with 16 engineering attributes, JSON schemas, Given-When-Then acceptance criteria, and 1-hour Redis deduplication rules.
4. **Enterprise Standardization:** Formulate an 81-field Data Dictionary and 35-metric KPI Catalogue with exact mathematical formulas and clear operational limitations.
5. **Data Quality Audit & QC Framework:** Forensically investigate injected quality anomalies across raw sheets and build a 6-stage prevention and automated cleaning pipeline.
6. **Executive Business Intelligence Dashboard:** Build a high-performance, interactive Streamlit BI application (`05_dashboard/app.py`) matching the sample matte charcoal theme (`#212435`) with white navigation sidebar, dynamic date/device filters, and zero fabricated financial data.

---

## 3. Source Workbooks and Worksheets Used

All metrics, data models, and analytical dashboards are strictly derived from the two original Excel workbooks located in [`01_raw_data/`](01_raw_data) (also preserved in [`Data/`](Data)):

### Source Workbook 1: `VELoop_Rewards_Data_01.xlsx` (359 KB)
* **`Users_1000_Clean` (1,000 rows, 27 cols):** Master clean user demographic profiles, registration timestamps, acquisition channels, device types, verification flags, and static soft currency `xp_balance`.
* **`Users_Messy_Audit` (1,008 rows, 28 cols):** Intentionally contaminated audit sheet containing 8 duplicate user IDs, 542 missing demographic cells, extra column `data_environment`, and unformatted dates.
* **`Data_Dictionary` (28 rows):** Baseline field definitions for the users table.
* **`Synthetic_Summary` (14 rows):** High-level summary of simulated cohort distribution.
* **`README_Data_Status` (9 rows):** Metadata and authenticity notice confirming simulated data status.

### Source Workbook 2: `VELOOP_Simulated_User_Behavior_1000.xlsx` (6.39 MB)
* **`01_Users_1000` (1,000 rows, 27 cols):** User profiles matching `Users_1000_Clean`.
* **`02_Sessions` (7,913 rows, 12 cols):** Contiguous user app sessions, durations, entry features, exit drop-off points, and events per session.
* **`03_Feature_Events` (35,704 rows, 13 cols):** Granular atomic interaction events across 15 core features (Watch Ads, Missions, Streak, Tap & Earn, Spin, Wallet, Referral, etc.).
* **`04_Daily_Activity` (6,667 rows, 17 cols):** Daily user activity rollups tracking active flags, duration, daily reward claims, wallet views, and task executions.
* **`05_Task_Activity` (9,846 rows, 12 cols):** Granular task execution sessions across 8 categories (Completed: 5,627 [57.1%], Abandoned: 2,051, Failed: 1,520, Pending: 648).
* **`06_Milestones` (4,799 rows, 6 cols):** Gamification milestone unlock records (first task, badge, streak, level up).
* **`07_Feature_Usage` (15 rows, 7 cols):** Pre-aggregated feature adoption and event volume rollups.
* **`08_Data_Dictionary` (76 rows):** Baseline field definitions for behavioral entities.
* **`09_README_Status` (9 rows):** Status notes confirming simulation environment.
* **`10_Event_Data_Quality_Audit` (35,714 rows, 13 cols):** Intentionally contaminated event stream containing exactly 10 duplicate rows, lowercase feature names, and unverified device strings.

---

## 4. Data Cleaning & Reconciliation Methodology

To ensure 100% reproducible and audit-compliant analytics, an automated cleaning pipeline [`03_analysis_and_models/profiling/clean_and_export_all_datasets.py`](03_analysis_and_models/profiling/clean_and_export_all_datasets.py) was developed:

### 4.1 Forensic Audit & Discrepancy Resolution
1. **The 10-Record Event Discrepancy:** The 10-record difference between `03_Feature_Events` (35,704 rows) and `10_Event_Data_Quality_Audit` (35,714 rows) was forensically verified: `10_Event_Data_Quality_Audit` contains **exactly 10 duplicate rows** for 10 specific event IDs (`EVT00021600`, `EVT00011275`, `EVT00006040`, `EVT00028196`, `EVT00030205`, `EVT00017051`, `EVT00034075`, `EVT00014772`, `EVT00025552`, `EVT00006379`). Deduplicating on `event_id` yields exactly 35,704 rows matching `03_Feature_Events` 1:1. These 10 duplicate records are archived in [`02_processed_data/event_audit_10_duplicates.csv`](02_processed_data/event_audit_10_duplicates.csv).
2. **Messy User Deduplication:** In `Users_Messy_Audit` (1,008 rows), exactly 8 duplicate user IDs (`VLUSR000095`, `VLUSR000217`, `VLUSR000272`, `VLUSR000335`, `VLUSR000409`, `VLUSR000779`, `VLUSR000803`, `VLUSR000813`) were identified and resolved by retaining the primary record, resulting in exactly 1,000 clean user records archived in [`02_processed_data/users_messy_8_duplicates.csv`](02_processed_data/users_messy_8_duplicates.csv).
3. **Standardized Cleaned Outputs:** Cleaned datasets are persisted in [`02_processed_data/`](02_processed_data):
   * `users_cleaned.csv` (1,000 rows, 27 cols, 0 duplicates, 100% valid PKs)
   * `events_cleaned.csv` (35,704 rows, 13 cols, title-cased feature names)
   * `sessions_cleaned.csv` (7,913 rows, 12 cols)
   * `daily_activity_cleaned.csv` (6,667 rows, 17 cols)
   * `tasks_cleaned.csv` (9,846 rows, 12 cols)
   * `milestones_cleaned.csv` (4,799 rows, 6 cols)

---

## 5. Analytics & Models Developed

1. **User & Account Lifecycle Model (Deliverable 04):** Deterministic user states (`Prospect` $\rightarrow$ `Registered` $\rightarrow$ `Onboarded` $\rightarrow$ `Active` $\rightarrow$ `Dormant` $\rightarrow$ `Churned`). Standardized regex schemas for `user_id`, `session_id`, `event_id`, and `transaction_id`.
2. **Earning & Reward Funnel Model (Deliverable 05):** 5-stage lifecycle (**Discovery $\rightarrow$ Start $\rightarrow$ Completion $\rightarrow$ Validation $\rightarrow$ Reward**). Complete decoupling of client task completion (5,627 tasks) from backend financial reward crediting (5,627 credited, 3,571 not credited, 648 pending).
3. **Double-Entry Wallet Model (Deliverable 06):** Immutable double-entry ledger architecture. For every balance movement, balancing debit and credit entries are created. Enforces the invariant:
   $$\sum \text{Debit Amount} - \sum \text{Credit Amount} = 0.00$$
4. **Withdrawal Operations Model (Deliverable 06):** Deterministic payout lifecycle (`Requested` $\rightarrow$ `Under_Review` $\rightarrow$ `Processing` $\rightarrow$ `Completed` / `Rejected` / `Reversed`). 10 formal withdrawal KPIs with exact mathematical formulas and SLA aging brackets.
5. **Referral & Viral Growth Model (Deliverable 07):** Establishes that registration $\ne$ referral conversion. Evaluates observed data (119 users acquired via Referral, 1,913 active days, 2,521 events) and provides future relational attribution schema.

---

## 6. Dashboard Sections & Live Interactive Capabilities

The Streamlit BI dashboard ([`05_dashboard/app.py`](05_dashboard/app.py)) is organized into the **7 official working sections** plus utility modules, featuring a sample-matched dark theme (matte charcoal `#212435`, crisp white navigation sidebar, custom Plotly dark charts, and zero top white space):

1. **Executive Overview:** High-level platform KPIs (Total Users: 1,000, Active Users: 815, Total Sessions: 7,913, Total Events: 35,704, Task Completion Rate: 57.1%), DAU trend line, and feature adoption donut.
2. **User & Account Analytics:** User demographics, age distribution histogram, gender split, device breakdown (Android vs iOS vs Web), and acquisition source distribution.
3. **Engagement & Behavioral Analytics:** Session duration distributions, features per session, feature event frequency chart, and daily active user stickiness.
4. **Earning & Reward Analytics:** Micro-task execution funnel (Viewed $\rightarrow$ Started $\rightarrow$ Completed), task conversion rate, category performance breakdown, and reward status audit.
5. **Wallet Intelligence:** Observed soft currency analytics (XP wealth quartile distribution, 2,172 wallet view events across 810 users, 1,686 active wallet days) and prominent Data Authenticity Notice regarding absence of monetary transactions.
6. **Withdrawal Operations:** Operational payout specifications, SLA aging queue templates (<6h, 6–12h, 12–24h, 24h+), payout rail distributions (UPI, Paytm, Bank Transfer), and clear notice stating simulated data contains no live payout records.
7. **Referral & Viral Growth:** Observed referral acquisition metrics (119 users, 11.9% share, 1,913 active days, 2,521 events), unique 8-character referral code integrity check, and future relational conversion funnel.
8. **Data Quality & Audit (Utility):** 10-duplicate event audit breakdown, 8 messy user duplicate audit, and missing values analysis.
9. **Data Explorer & File Upload (Utility):** Dynamic CSV and Excel file uploader with schema validation, record preview, and column summary stats.
10. **Reports & Document Exports (Utility):** One-click download buttons for all 4 official PDF reports, 7 Excel workbooks, and cleaned CSV datasets.
11. **Project Information & Governance (Utility):** Project metadata, internship scope, and data authenticity policy.

---

## 7. PostgreSQL Schema & SQL File Structure

Located in [`03_analysis_and_models/sql/`](03_analysis_and_models/sql):

| File Name | Purpose & Contents | Tables / Views Created |
| :--- | :--- | :--- |
| **`01_schema_ddl.sql`** | Core relational DDL in PostgreSQL 15+ compatible ANSI SQL. Defines PKs, FKs, NOT NULL, CHECK constraints, and 22 performance indexes. | Tables: `users`, `sessions`, `feature_events`, `daily_activity`, `task_activity`, `milestones`, `wallet_accounts`, `wallet_ledger`, `withdrawals`, `referrals`. |
| **`02_user_and_engagement_analytics.sql`** | User engagement views and queries for DAU, rolling WAU/MAU, stickiness ratio, weekly cohort retention, and session duration brackets. | Views: `v_daily_active_users`, `v_user_retention_cohorts`, `v_session_duration_distribution`. |
| **`03_earning_and_reward_analytics.sql`** | Earning and task analytics queries: task conversion funnel, category performance breakdown, and reward status audit. | Views: `v_task_conversion_funnel`, `v_category_earning_breakdown`, `v_reward_credit_audit`. |
| **`04_wallet_and_withdrawal_analytics.sql`** | Soft currency metrics, double-entry mathematical reconciliation (`SUM(debits) - SUM(credits) = 0.00`), and withdrawal SLA aging queue. | Views: `v_wallet_engagement_summary`, `v_wallet_events_breakdown`, `v_user_xp_distribution`, `v_double_entry_reconciliation`, `v_withdrawal_sla_queue_aging`. |
| **`05_referral_virality_analytics.sql`** | Observed referral acquisition share (119 users), referral activity days, referral code audit, and future relational conversion funnel. | Views: `v_referral_acquisition_summary`, `v_referral_daily_activity`, `v_referral_events_breakdown`, `v_referral_code_audit`, `v_referral_conversion_funnel`. |
| **`06_data_quality_audit_checks.sql`** | Data quality checks: duplicate event IDs, duplicate users, orphan records, impossible timestamps, and unbalanced transactions. | Views: `v_dq_duplicate_events`, `v_dq_duplicate_users`, `v_dq_orphan_events`, `v_dq_impossible_timestamps`, `v_dq_unbalanced_transactions`. |

---

## 8. Step-by-Step Instructions to Run Dashboard Locally

### Prerequisites
* Python 3.10, 3.11, or 3.12 installed.
* Standard terminal (PowerShell, Command Prompt, or Bash).

```bash
# Step 1: Clone or navigate to the repository directory
cd "d:\Veloop data Analysis"

# Step 2: Install required Python dependencies
pip install -r requirements.txt

# Step 3: Launch the Streamlit dashboard
streamlit run 05_dashboard/app.py
```

* **Access the Dashboard:** Open your web browser and navigate to `http://localhost:8501`.
* **Interact with Visuals:** Use the white sidebar on the left to navigate between the 7 core sections and utility tools. Adjust the date range slider or select specific device platforms to filter data dynamically in real time.

---

## 9. Step-by-Step Instructions to Execute Automated Tests

The project includes an enterprise-grade automated test suite containing **26 test cases across 4 test suites**:

```bash
# Execute the full automated test suite with verbose output
python -m unittest discover -s 07_tests_and_validation -p "test_*.py" -v
```

### Running Individual Test Suites:
```bash
# 1. Master deliverables existence and integrity (10 tests)
python -m unittest 07_tests_and_validation/test_all_deliverables.py

# 2. Interactive dashboard filters, charts, and uploads (5 tests)
python -m unittest 07_tests_and_validation/test_dashboard_interactive.py

# 3. Phase 1 foundations and raw data preservation (6 tests)
python -m unittest 07_tests_and_validation/test_phase1_audit.py

# 4. PostgreSQL DDL, views, and double-entry reconciliation (5 tests)
python -m unittest 07_tests_and_validation/test_sql_and_reconciliation.py
```

* **Test Execution Evidence:** Full test execution output is logged in [`07_tests_and_validation/evidence/test_run.log`](07_tests_and_validation/evidence/test_run.log) and [`07_tests_and_validation/evidence/test_execution_report.md`](07_tests_and_validation/evidence/test_execution_report.md).

---

## 10. Data Authenticity & Limitation Notes

> [!WARNING]
> **MANDATORY DATA AUTHENTICITY NOTICE (`SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`):**
> VELOOP Rewards is an active developing product. All metrics, user records, and event logs analyzed herein are synthetic test cohorts created strictly to evaluate data readiness, schemas, and BI pipelines. They do not represent actual commercial users, revenue, or business performance.

1. **Absence of Monetary Transactions:** The raw simulated files contain **no fiat transaction ledgers, withdrawal payout records, or payment gateway feeds**. All soft currency balances represent gamified experience points (`XP`), not real money liabilities. No fake monetary payouts (e.g. ₹125,000 withdrawn) have been fabricated.
2. **Absence of Referral Relational Pairs:** Individual user records contain an 8-character `referral_code`, but no relational mapping table exists linking referring users to referee users. No fake referral pairs or viral coefficients have been invented.
3. **4-Tier Classification Standard:** Every statement in this project is explicitly categorized into:
   * **[Confirmed]:** Directly verified from supplied raw workbooks.
   * **[Proposed]:** Analytical designs or engineering recommendations formulated by the analyst.
   * **[To Be Verified]:** Business parameters requiring confirmation from VELOOP leadership.
   * **[Simulated]:** Data elements generated or supplied for analytical testing.

---

## 11. Public Streamlit Community Cloud Deployment Instructions

The repository is fully configured for zero-configuration deployment to **Streamlit Community Cloud**:

### Deployment Steps:
1. Fork or push the repository to GitHub: `https://github.com/R-ABIDA/VeLoop-Rewards-Product-Analytics`.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with your GitHub account.
3. Click **"New app"**.
4. Configure the deployment parameters:
   * **Repository:** `R-ABIDA/VeLoop-Rewards-Product-Analytics`
   * **Branch:** `main`
   * **Main file path:** `05_dashboard/app.py`
   * **App URL (optional):** `veloop-rewards-analytics`
5. Click **"Deploy!"**.
6. The application uses repository-relative paths (`01_raw_data/`, `02_processed_data/`), standard packages in `requirements.txt`, and requires no external database credentials or environment variables.

---

## 12. Complete 21-Deliverable Checklist

| # | Code | Deliverable Name | File Link(s) | Status |
| :-: | :--- | :--- | :--- | :---: |
| **01** | `DEL-01` | Executive Summary | [Executive_Summary.md](04_deliverables/deliverable_01_executive_summary/Executive_Summary.md), [PDF](04_deliverables/deliverable_01_executive_summary/Executive_Summary.pdf) | **Verified 100%** |
| **02** | `DEL-02` | Product Data Readiness Audit | [Product_Data_Readiness_Audit.md](04_deliverables/deliverable_02_product_data_audit/Product_Data_Readiness_Audit.md) | **Verified 100%** |
| **03** | `DEL-03` | Data Coverage Matrix & Gaps Register | [Data_Coverage_Matrix.xlsx](04_deliverables/deliverable_03_data_coverage_matrix/Data_Coverage_Matrix.xlsx), [MD](04_deliverables/deliverable_03_data_coverage_matrix/Data_Coverage_Matrix.md) | **Verified 100%** |
| **04** | `DEL-04` | User & Account Analytics Specification | [User_Analytics_Specification.md](04_deliverables/deliverable_04_user_analytics_spec/User_Analytics_Specification.md) | **Verified 100%** |
| **05** | `DEL-05` | Earning & Reward Analytics Specification | [Reward_Analytics_Specification.md](04_deliverables/deliverable_05_reward_analytics_spec/Reward_Analytics_Specification.md) | **Verified 100%** |
| **06** | `DEL-06` | Wallet & Withdrawal Specification | [Wallet_Withdrawal_Specification.md](04_deliverables/deliverable_06_wallet_withdrawal_spec/Wallet_Withdrawal_Specification.md) | **Verified 100%** |
| **07** | `DEL-07` | Referral & Engagement Analytics | [Referral_Engagement_Analytics.md](04_deliverables/deliverable_07_referral_engagement_analytics/Referral_Engagement_Analytics.md) | **Verified 100%** |
| **08** | `DEL-08` | Event Tracking Plan (32 Events, 16 Attrs) | [Event_Tracking_Plan.xlsx](04_deliverables/deliverable_08_event_tracking_plan/Event_Tracking_Plan.xlsx), [MD](04_deliverables/deliverable_08_event_tracking_plan/Event_Tracking_Plan.md) | **Verified 100%** |
| **09** | `DEL-09` | Enterprise Data Dictionary (81 Fields) | [Data_Dictionary.xlsx](04_deliverables/deliverable_09_data_dictionary/Data_Dictionary.xlsx), [MD](04_deliverables/deliverable_09_data_dictionary/Data_Dictionary.md) | **Verified 100%** |
| **10** | `DEL-10` | Logical Data Model & Physical DDL | [Logical_Data_Model_and_ER_Diagram.md](04_deliverables/deliverable_10_logical_data_model/Logical_Data_Model_and_ER_Diagram.md), [schema.sql](04_deliverables/deliverable_10_logical_data_model/schema.sql) | **Verified 100%** |
| **11** | `DEL-11` | Enterprise KPI Catalogue (35 KPIs) | [KPI_Catalogue.xlsx](04_deliverables/deliverable_11_kpi_catalogue/KPI_Catalogue.xlsx), [MD](04_deliverables/deliverable_11_kpi_catalogue/KPI_Catalogue.md) | **Verified 100%** |
| **12** | `DEL-12` | Simulated Data Profiling Report | [Simulated_Data_Profiling_Workbook.xlsx](04_deliverables/deliverable_12_simulated_data_profiling/Simulated_Data_Profiling_Workbook.xlsx), [MD](04_deliverables/deliverable_12_simulated_data_profiling/Simulated_Data_Profiling_Report.md) | **Verified 100%** |
| **13** | `DEL-13` | Data Quality Audit & QC Framework | [Data_Quality_Audit_Workbook.xlsx](04_deliverables/deliverable_13_data_quality_audit/Data_Quality_Audit_Workbook.xlsx), [MD](04_deliverables/deliverable_13_data_quality_audit/Data_Quality_Audit_Report.md), [PDF](04_deliverables/deliverable_13_data_quality_audit/Data_Quality_Audit_Report.pdf) | **Verified 100%** |
| **14** | `DEL-14` | Dashboard Blueprint Specification | [Dashboard_Blueprint_Specifications.md](04_deliverables/deliverable_14_dashboard_blueprint/Dashboard_Blueprint_Specifications.md) | **Verified 100%** |
| **15** | `DEL-15` | Developer Analytics Handoff | [Developer_Analytics_Handoff.md](04_deliverables/deliverable_15_developer_handoff/Developer_Analytics_Handoff.md) | **Verified 100%** |
| **16** | `DEL-16` | Data Pipeline Proposal & Architecture | [Data_Pipeline_Proposal.md](04_deliverables/deliverable_16_data_pipeline_proposal/Data_Pipeline_Proposal.md) | **Verified 100%** |
| **17** | `DEL-17` | Privacy, Governance & Change Mgmt | [Privacy_Governance_and_Change_Management.md](04_deliverables/deliverable_17_privacy_and_governance/Privacy_Governance_and_Change_Management.md) | **Verified 100%** |
| **18** | `DEL-18` | Analytics Readiness Assessment | [Analytics_Readiness_Assessment.md](04_deliverables/deliverable_18_analytics_readiness_assessment/Analytics_Readiness_Assessment.md), [PDF](04_deliverables/deliverable_18_analytics_readiness_assessment/Analytics_Readiness_Assessment.pdf) | **Verified 100%** |
| **19** | `DEL-19` | Source & Verification Register | [Source_and_Verification_Register.xlsx](04_deliverables/deliverable_19_assumption_and_verification_register/Source_and_Verification_Register.xlsx), [MD](04_deliverables/deliverable_19_assumption_and_verification_register/Source_and_Verification_Register.md) | **Verified 100%** |
| **20** | `DEL-20` | Implementation Backlog | [Implementation_Backlog.md](04_deliverables/deliverable_20_implementation_backlog/Implementation_Backlog.md) | **Verified 100%** |
| **21** | `DEL-21` | Final Consolidated Report | [Final_Consolidated_Report.md](04_deliverables/deliverable_21_final_consolidated_report/Final_Consolidated_Report.md), [PDF](04_deliverables/deliverable_21_final_consolidated_report/Final_Consolidated_Report.pdf) | **Verified 100%** |
