# VELOOP REWARDS — PRODUCT ANALYTICS, DATA READINESS & DATA MANAGEMENT BLUEPRINT
**Task:** Data Analyst Internship — Task 01  
**Organization:** VELOOP Rewards & VELOOP CO.  
**Role:** Senior Data Analyst & Analytics Engineering Specialist (Data Analyst Intern)  
**Chief Executive Officer:** Ayan Alam  
**Duration:** 22–25 Days (2 Development Days / 1 Review Day Sprint Cadence)  
**Mandatory Integrity Label:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
**Classification:** Confirmed, Proposed, To Be Verified, Simulated  

---

## 1. Project Overview & Business Context

**VELOOP Rewards** is an early-stage consumer digital rewards and gamified engagement platform in active development. Users interact with rewarded video advertisements, partner app installs, surveys, games, daily check-in streaks, mining rigs, and lucky wheels to earn reward currencies (`XP`, `Gems`, `Tokens`) that can be redeemed for cash withdrawals (via UPI, Paytm, Bank Transfer, PayPal) or digital vouchers.

Because VELOOP is currently in pre-launch development, the platform lacks the massive production telemetry volume required for conventional empirical performance analysis. Therefore, this project establishes the **complete analytical architecture, relational data models, event telemetry specifications, quality control systems, and BI dashboard foundations** required to launch and scale production analytics with zero financial leakage and audit compliance.

---

## 2. Core Objectives

1. **Product Area Mapping:** Audit all 18 core functional domains and 32 features, distinguishing user actions, system outcomes, and business value.
2. **Relational Data Architecture:** Design a normalized star-schema in PostgreSQL 15+ (`schema.sql`) enforcing double-entry financial accounting and referential integrity.
3. **Production Event Tracking:** Formulate 32 production events with exact JSON schemas, Given-When-Then acceptance tests, and Redis 1h stream deduplication.
4. **Enterprise Standardization:** Publish an 81-field Data Dictionary and 35-metric KPI Catalogue with mathematically rigorous definitions.
5. **Data Quality & Hygiene:** Audit 12 anomaly classes across messy test sheets and build an automated 6-stage Quality Control Framework.
6. **Executive Business Intelligence:** Build a functional, interactive 7-section Streamlit analytics dashboard (`05_dashboard/app.py`).

---

## 3. Mandatory Data Authenticity & Integrity Policy

In strict adherence to **Section 2 & Section 34 of `Data_Analyst_01.pdf`**:
* **Simulated Test Data:** All data supplied for this assignment is fictional/simulated. It is never described as actual VELOOP users, revenue, earnings, retention, or conversion rates.
* **Non-Negotiable Disclaimer:** Every dataset, chart, report, and dashboard banner carries the explicit notice:  
  `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`
* **4-Tier Evidentiary Standard:**
  1. `[Confirmed]`: Supported by official source documents.
  2. `[Proposed]`: Professional analytical recommendations formulated by the analyst.
  3. `[To Be Verified]`: Requires confirmation from VELOOP leadership or engineering.
  4. `[Simulated]`: Generated or supplied strictly for analytical testing.

---

## 4. Dataset Description & Ground-Truth Counts

| Dataset / Sheet Name | Source File | Records | Columns | Primary Key | Key Attributes |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `Users_1000_Clean` | `VELoop_Rewards_Data_01.xlsx` | **1,000** | 27 | `user_id` | Master user profiles, acquisition channel, device, verified status, XP balance |
| `Users_Messy_Audit` | `VELoop_Rewards_Data_01.xlsx` | **1,008** | 28 | `user_id` | Contains controlled duplicates, null emails, bad dates, and negative ages |
| `02_Sessions` | `Simulated_User_Behavior.xlsx` | **7,913** | 12 | `session_id` | Contiguous user visits, durations, entry points, and exit drop-off screens |
| `03_Feature_Events` | `Simulated_User_Behavior.xlsx` | **35,704** | 13 | `event_id` | Atomic streaming interaction logs across 15 core product features |
| `04_Daily_Activity` | `Simulated_User_Behavior.xlsx` | **6,667** | 17 | `(user_id, date)` | Pre-aggregated daily user rollups for fast executive reporting |
| `05_Task_Activity` | `Simulated_User_Behavior.xlsx` | **9,846** | 12 | `activity_id` | Task execution sessions across 8 categories; duration, failure reasons |
| `06_Milestones` | `Simulated_User_Behavior.xlsx` | **4,799** | 6 | `user_id` | Milestone achievements (first task, badge, streak, level up) |
| `07_Feature_Usage` | `Simulated_User_Behavior.xlsx` | **15** | 7 | `feature_name` | Summary adoption and repeat usage metrics per feature |
| `10_Event_Data_Quality_Audit` | `Simulated_User_Behavior.xlsx` | **35,714** | 13 | `event_id` | Injected messy events with duplicate IDs and inconsistent lowercase casing |

---

## 5. Technology Stack

* **Language & Analysis:** Python 3.10+ (NumPy, Pandas)
* **Database & Schema Modeling:** PostgreSQL 15+ compatible DDL, Standard SQL
* **Spreadsheet Engineering:** Microsoft Excel (`.xlsx`) via `openpyxl` with styled headers, gridlines, and conditional styling
* **Interactive Business Intelligence:** Streamlit, Plotly Express, Plotly Graph Objects
* **Documentation & Diagrams:** GitHub Flavored Markdown, Mermaid.js
* **Quality Assurance:** Python `unittest`, `py_compile`

---

## 6. Project Directory Scaffolding

```
d:\Veloop data Analysis\
├── 01_raw_data/                                  # Preserved original source Excel files (untouched)
├── 02_processed_data/                             # Cleaned, standardized, reproducible CSV datasets
│   ├── users_cleaned.csv                         # Exactly 1,000 deduplicated, formatted user records
│   └── events_cleaned.csv                        # Exactly 35,704 standardized, title-cased events
├── 03_analysis_and_models/                       # Technical scripts, profiling engines, and DDL
│   ├── sql/                                      # PostgreSQL database schemas
│   ├── notebooks/                                # Jupyter profiling notebooks
│   └── profiling/                                # OpenPyXL generators and automated audit scripts
├── 04_deliverables/                              # All 21 official required deliverables
│   ├── deliverable_01_executive_summary/         # Deliverable 01: 4-Page Executive Summary
│   ├── deliverable_02_product_data_audit/        # Deliverable 02: Product Data Readiness Audit Report
│   ├── deliverable_03_data_coverage_matrix/      # Deliverable 03: Data Coverage Matrix (.xlsx)
│   ├── deliverable_04_user_analytics_spec/       # Deliverable 04: User Analytics Specification
│   ├── deliverable_05_reward_analytics_spec/     # Deliverable 05: Earning & Reward Analytics Spec
│   ├── deliverable_06_wallet_withdrawal_spec/    # Deliverable 06: Wallet & Withdrawal Analytics Spec
│   ├── deliverable_07_referral_engagement_analytics/ # Deliverable 07: Referral & Engagement Spec
│   ├── deliverable_08_event_tracking_plan/       # Deliverable 08: Event Tracking Plan (.xlsx)
│   ├── deliverable_09_data_dictionary/           # Deliverable 09: Enterprise Data Dictionary (.xlsx)
│   ├── deliverable_10_logical_data_model/        # Deliverable 10: ER Diagram & schema.sql
│   ├── deliverable_11_kpi_catalogue/             # Deliverable 11: KPI Catalogue (.xlsx)
│   ├── deliverable_12_simulated_data_profiling/  # Deliverable 12: Profiling Workbook (.xlsx) & Report
│   ├── deliverable_13_data_quality_audit/        # Deliverable 13: Quality Audit Workbook (.xlsx) & Report
│   ├── deliverable_14_dashboard_blueprint/       # Deliverable 14: Dashboard Blueprint Specifications
│   ├── deliverable_15_developer_handoff/         # Deliverable 15: Developer Analytics Handoff
│   ├── deliverable_16_data_pipeline_proposal/    # Deliverable 16: Pipeline Proposal & Architecture
│   ├── deliverable_17_privacy_and_governance/    # Deliverable 17: Privacy, Governance & Change Log
│   ├── deliverable_18_analytics_readiness_assessment/ # Deliverable 18: Readiness Assessment Scorecard
│   ├── deliverable_19_assumption_and_verification_register/ # Deliverable 19: Source & Verification Register (.xlsx)
│   ├── deliverable_20_implementation_backlog/    # Deliverable 20: Prioritized Implementation Backlog
│   └── deliverable_21_final_consolidated_report/ # Deliverable 21: Final Consolidated Technical Report
├── 05_dashboard/                                 # Interactive Streamlit BI Application
│   └── app.py                                    # Functional 7-section executive dashboard
├── 06_documentation_and_reports/                 # General documentation and reference assets
├── 07_tests_and_validation/                      # Automated Python unit and integrity test suites
│   ├── test_phase1_audit.py                      # Phase 1 initialization tests
│   └── test_all_deliverables.py                  # Master validation suite for all 21 deliverables
├── 08_presentation/                              # Executive PowerPoint & HTML slide decks
│   ├── VELOOP_Rewards_Final_Presentation.md      # 14-slide presentation speaker deck
│   └── VELOOP_Rewards_Final_Presentation.html    # Interactive HTML5 slide deck with keyboard controls
├── Data/                                         # Original input workbooks
├── requirements.txt                              # Python package dependencies
├── REQUIREMENTS_AND_DELIVERABLES_TRACKER.md      # Master progress tracking matrix
├── PHASED_IMPLEMENTATION_PLAN.md                 # 25-day roadmap following 2-dev / 1-review rhythm
├── MISSING_DEPENDENCIES_AND_SOURCE_REGISTER.md   # Documentation of missing inputs
└── README.md                                     # Project master documentation (This File)
```

---

## 7. Installation & Local Setup

### 7.1 Prerequisites
* Python 3.10, 3.11, 3.12, or 3.13 installed.
* Standard terminal (PowerShell, Command Prompt, or Bash).

### 7.2 Environment Installation
```bash
# Clone or navigate to the workspace
cd "d:\Veloop data Analysis"

# Install required dependencies
pip install -r requirements.txt
```

---

## 8. Execution Instructions

### 8.1 Run Data Profiling & Quality Audit Engine
Executes automated profiling across all 9 sheets, cleans messy datasets, and outputs Deliverables 12 & 13:
```bash
python 03_analysis_and_models/profiling/run_profiling_and_quality_audit.py
```

### 8.2 Regenerate Excel Workbooks (Deliverables 03, 08, 09, 11, 19)
```bash
python 03_analysis_and_models/profiling/build_work_package_a_and_trackers.py
python 03_analysis_and_models/profiling/generate_deliverables_08_09_11.py
```

### 8.3 Launch Interactive Streamlit BI Dashboard
Launches the 7-section executive analytics dashboard locally:
```bash
streamlit run 05_dashboard/app.py
```
* **Local Web Interface:** Open `http://localhost:8501` in your browser.
* **Sections Available:** Executive Overview, User Analytics, Engagement, Rewards, Wallet, Withdrawals, Referrals.

### 8.4 Open Interactive Final Presentation
Open `08_presentation/VELOOP_Rewards_Final_Presentation.html` directly in Google Chrome or Microsoft Edge. Use the `←` and `→` arrow keys to navigate the 14 executive slides.

---

## 9. Automated Testing & Verification Suite

To verify that all 21 deliverables exist, Excel workbooks are structurally valid, SQL schemas are intact, and simulation disclaimers are present:
```bash
python -m unittest 07_tests_and_validation/test_all_deliverables.py
```
* **Test Result:** `Ran 7 tests ... OK (All passing)`.

---

## 10. Known Limitations & Future Improvements

1. **Simulated Withdrawals & Transactions:** Standalone tables for withdrawals and double-entry wallet transactions were not provided in the raw files. These have been formally specified in `schema.sql` and modeled for demonstration in the dashboard.
2. **Attribution Linking:** Referral share events exist, but referee-to-referrer database keys must be deployed in the production auth service before viral coefficient ($K$) can be computed dynamically.
3. **Automated Orchestration:** Post-launch improvements should deploy Apache Airflow or GitHub Actions to automate the hourly execution of dbt Core models.

