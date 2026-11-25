# VELOOP Rewards — Product Analytics & BI Project

**Project:** VELOOP Rewards — Product Analytics, Data Readiness & Data Management  
**Role:** Data Analyst Intern  
**Integrity notice:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
**GitHub:** https://github.com/R-ABIDA/VeLoop-Rewards-Product-Analytics  
**Documentation status:** Updated 25 November 2026

> **Important:** The workbooks and generated transaction files in this repository contain simulated/test data. They do not represent actual VELOOP customers, real revenue, real payouts, or production business performance.

## 1. Project overview

This project builds a product-analytics foundation for a digital rewards application. It includes source-workbook profiling, data cleaning, SQL analytics, PostgreSQL schema design, wallet/withdrawal simulation, event-tracking specifications, a Streamlit dashboard, 21 analytical deliverables, automated tests, and a presentation.

Evidence is classified as **observed in supplied files**, **simulated**, **proposed**, or **not verified**. A design or file being present does not prove production deployment.

## 2. Repository structure

| Folder / file | Purpose |
|---|---|
| `01_raw_data/` | Original simulated Excel source workbooks |
| `02_processed_data/` | Cleaned CSV datasets and audit extracts |
| `03_analysis_and_models/profiling/` | Profiling, cleaning, audit, and deliverable-generation scripts |
| `03_analysis_and_models/sql/` | PostgreSQL DDL, analytical SQL, and ingestion script |
| `04_deliverables/` | The 21 documented project deliverables |
| `05_dashboard/` | Streamlit dashboard (`app.py`) and PostgreSQL helper (`db.py`) |
| `06_documentation_and_reports/` | Dataset reports and supporting documentation |
| `07_tests_and_validation/` | Automated tests, validation queries, and evidence |
| `08_evidence_charts/` | Generated charts used in the reports |
| `08_presentation/` | Presentation source files and exports |
| `Wallet & Withdrawal Simulation/` | Simulated wallet accounts, ledger, withdrawals, and SQL |
| `requirements.txt` | Python dependencies |
| `PROJECT_IMPLEMENTATION_STATUS.md` | Current implementation and verification boundary |

## 3. Source data and cleaning outputs

Primary workbooks: `01_raw_data/VELoop_Rewards_Data_01.xlsx` and `01_raw_data/VELOOP_Simulated_User_Behavior_1000.xlsx`.

Workbook/cleaned-file simulated counts include 1,000 users, 7,913 sessions, 35,704 feature events, 6,667 daily-activity rows, 9,846 task-activity rows, and 4,799 milestone rows. These are source-file counts, not guaranteed PostgreSQL runtime counts.

Cleaned outputs in `02_processed_data/` include `users_cleaned.csv`, `sessions_cleaned.csv`, `events_cleaned.csv`, `daily_activity_cleaned.csv`, `tasks_cleaned.csv`, and `milestones_cleaned.csv`, plus duplicate/discrepancy audit extracts. The 35,714-row audit event sheet differs from the 35,704 clean event sheet by ten duplicate records; see `04_deliverables/deliverable_13_data_quality_audit/Event_Discrepancy_Forensic_Audit.md`.

## 4. Dashboard — current implemented navigation

Launch from the project root:

```bash
pip install -r requirements.txt
streamlit run 05_dashboard/app.py
```

The source code implements seven sections: **Overview**, **User Analytics**, **Earning & Rewards**, **Wallet & Withdrawal**, **Referral & Virality**, **Feature & Engagement**, and **Data Quality & Audit**. The sidebar uses Streamlit `st.sidebar` and `st.radio`.

The current source styling is light corporate blue: page background `#F3F6FB`, sidebar `#142B4A`, primary blue `#2463A6`, and white cards. It is not the earlier matte-charcoal theme.

The app attempts PostgreSQL first and uses file fallback if database loading fails. Dashboard values depend on active filters and the source successfully loaded. The simulated-data notice must remain visible. Workbook task rows are not equivalent to task records loaded into PostgreSQL. Referral telemetry is not a verified referrer/referee relationship. Simulated withdrawal records are not proof of real payout settlement.

## 5. Wallet and withdrawal simulation

`Wallet & Withdrawal Simulation/` contains 2,001 simulated wallet-account rows, 2,680 simulated ledger rows, and 180 simulated withdrawal rows. They support analytical and reconciliation testing only; they do not represent actual customer funds or bank payments.

## 6. SQL and data model

`03_analysis_and_models/sql/` contains the schema DDL, six analytical SQL scripts, and `load_to_postgres.py`. These files define a proposed/analytical model. A schema file existing in the repository does not prove successful deployment. The archived PostgreSQL evidence currently says `AUTH_REQUIRED_NOT_VERIFIED`.

## 7. Deliverables

`04_deliverables/` contains the 21 authored deliverables, from executive summary and data audit through event tracking, data dictionary, KPI catalogue, dashboard blueprint, governance, implementation backlog, and final report. Artifact presence does not mean every proposed capability is production implemented.

## 8. Automated tests

Run:

```bash
python -m unittest discover -s 07_tests_and_validation -p "test_*.py"
```

**Updated archive test result:** 40 passed, 0 failed, 0 errors in the review environment. This does not verify PostgreSQL credentials/server availability, public Streamlit deployment, production integrations, or real payment settlement.

## 9. Configuration and security

Configure PostgreSQL locally using Streamlit secrets or environment variables. Never commit `.streamlit/secrets.toml`, `.env` files containing credentials, API keys, or tokens. The secrets file is excluded from this cleaned archive. If a real password was previously included in a shared archive or public commit, rotate it before reuse.

## 10. Status and evidence

See [`PROJECT_IMPLEMENTATION_STATUS.md`](PROJECT_IMPLEMENTATION_STATUS.md) and `07_tests_and_validation/evidence/` for dated verification details.

---
**Integrity policy:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`
