# VELOOP REWARDS — DOCUMENTATION & REPORTS

**Project:** Product Analytics, Data Readiness & Data Management  
**Integrity notice:** SIMULATED DATA — CREATED FOR ANALYTICAL TESTING

## Master deliverables

The 21 deliverables are organized under [`04_deliverables/`](../04_deliverables/). The consolidated report is available at [Deliverable 21](../04_deliverables/deliverable_21_final_consolidated_report/Final_Consolidated_Report.md).

## Supporting documentation

- [Executive Summary](../04_deliverables/deliverable_01_executive_summary/Executive_Summary.md)
- [Product Data Readiness Audit](../04_deliverables/deliverable_02_product_data_audit/Product_Data_Readiness_Audit.md)
- [Data Coverage Matrix](../04_deliverables/deliverable_03_data_coverage_matrix/Data_Coverage_Matrix.md)
- [Wallet & Withdrawal Specification](../04_deliverables/deliverable_06_wallet_withdrawal_spec/Wallet_Withdrawal_Specification.md)
- [Referral & Engagement Specification](../04_deliverables/deliverable_07_referral_engagement_analytics/Referral_Engagement_Analytics.md)
- [32-Event Tracking Plan](../04_deliverables/deliverable_08_event_tracking_plan/Event_Tracking_Plan.md)
- [Data Dictionary](../04_deliverables/deliverable_09_data_dictionary/Data_Dictionary.md)
- [Logical Data Model and DDL](../04_deliverables/deliverable_10_logical_data_model/Logical_Data_Model_and_ER_Diagram.md)
- [Data Quality Audit](../04_deliverables/deliverable_13_data_quality_audit/Data_Quality_Audit_Report.md)
- [Dashboard Blueprint](../04_deliverables/deliverable_14_dashboard_blueprint/Dashboard_Blueprint_Specifications.md)
- [Developer Handoff](../04_deliverables/deliverable_15_developer_handoff/Developer_Analytics_Handoff.md)
- [Source & Verification Register](../04_deliverables/deliverable_19_assumption_and_verification_register/Source_and_Verification_Register.md)
- [Implementation Backlog](../04_deliverables/deliverable_20_implementation_backlog/Implementation_Backlog.md)

## Dashboard

The current Streamlit application exposes seven primary analytical sections:

1. Overview
2. User Analytics
3. Earning & Rewards
4. Wallet & Withdrawal
5. Referral & Virality
6. Feature & Engagement
7. Data Quality & Audit

Run locally from the project root:

```bash
python -m pip install -r requirements.txt
python -m streamlit run 05_dashboard/app.py
```

The dashboard uses PostgreSQL when configured. Keep local database credentials in `.streamlit/secrets.toml` or environment variables; do not commit secrets. Public deployment must be verified separately before a live URL is published.

## Evidence and limitations

- Test scripts and saved execution evidence are in [`07_tests_and_validation/`](../07_tests_and_validation/).
- Database execution evidence must distinguish successful local PostgreSQL runs from dry runs or runs blocked by authentication.
- Wallet, withdrawal and user-behavior records are simulated analytical data, not real customer transactions.
- Referral conversion requires actual referrer–referee relationship records; referral event counts alone do not prove successful referrals.
- The dashboard must show unavailable where the underlying source table has no records.

