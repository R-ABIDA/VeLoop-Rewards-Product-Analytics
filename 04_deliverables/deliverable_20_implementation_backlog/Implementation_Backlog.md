# VELOOP REWARDS — PRIORITIZED IMPLEMENTATION BACKLOG
**Deliverable ID:** Deliverable 20  
**Work Package:** Final Implementation Backlog  
**Author:** Data Analyst Intern  
**Organization:** VELOOP Rewards  
**Date:** 2026-11-11  
**Integrity Label:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
**Classification:** Confirmed, Proposed, To Be Verified, Simulated  

---

## 1. Executive Summary & Backlog Governance

The **Implementation Backlog** translates all findings from the Product Data Readiness Audit, Data Quality Audit, and Analytics Gap Assessment into a structured, engineering-ready execution plan.

In accordance with **Section 26 of `Data_Analyst_01.pdf`**, all requirements are strictly bifurcated into:
1. **Stage 1: Pre-Launch Requirements (Non-Negotiable Production Blockers):** Core data structures, financial ledgers, anti-fraud controls, and event tracking that must be active before public user onboarding.
2. **Stage 2: Post-Launch Improvements (Continuous Optimization):** Advanced analytics dashboards, machine-learning attribution models, automated self-service reporting, and warehouse migrations.

---

## 2. Pre-Launch Implementation Backlog (Production Blockers)

| Priority | Requirement Name | Technical Description | Business & Analytical Rationale | Critical Dependency | Engineering Owner | Target Stage | Implementation Status |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **Critical** | **Stable User Identifier** | Enforce immutable `user_id` format (`^VLUSR[0-9]{6}$`) across all platforms. | Required for deterministic cross-event tracking and long-term user retention cohorting. | Auth Service DB | Engineering (Backend) | Pre-Launch | **Ready for Dev** |
| **Critical** | **Double-Entry Transaction Ledger** | Deploy `wallet_transactions` table with immutable IDs, signed amounts, and reference links. | Required for financial reconciliation, preventing balance drift, and auditing currency velocity. | Wallet Microservice | Engineering (Backend) | Pre-Launch | **Ready for Dev** |
| **Critical** | **Withdrawal Lifecycle & Payout Table** | Establish `withdrawals` table tracking `Requested` $\rightarrow$ `Processing` $\rightarrow$ `Completed` / `Rejected`. | Prevents duplicate cash disbursements via gateway and enables payout SLA monitoring (< 24h). | Payment Gateway API | Engineering (Backend) | Pre-Launch | **Ready for Dev** |
| **Critical** | **Relational Referral Attribution** | Deploy `referrals` entity mapping `referring_user_id` to `referred_user_id` with activation dates. | Required to measure true viral coefficient ($K$), prevent self-referral fraud, and pay bonuses. | Referral Engine | Engineering (Backend) | Pre-Launch | **Ready for Dev** |
| **High** | **Production Event Tracking Plan** | Instrument core 32 events in mobile SDK with envelope schema and UTC timestamps. | Core telemetry foundation for feature adoption, drop-off funnels, and executive BI. | Client Telemetry SDK | Engineering (Frontend) | Pre-Launch | **Ready for Dev** |
| **High** | **Stream Ingestion Deduplication** | Implement in-memory Redis cache (1h TTL) checking `(event_id, sequence_number)` on ingestion. | Eliminates $5\%\text{--}15\%$ event count inflation caused by mobile network retry loops. | API Ingestion Gateway | DevOps / Backend | Pre-Launch | **Ready for Dev** |
| **High** | **Automated Data Quality Gates** | Deploy schema validation (Pydantic) routing malformed payloads to a Dead Letter Queue (DLQ). | Prevents broken JSON strings and corrupt data from crashing downstream ETL pipelines. | Ingestion Pipeline | Data Engineering | Pre-Launch | **Ready for Dev** |
| **High** | **PII Masking & Sanitization** | Implement SHA-256 email hashing and name masking in analytical warehouse marts. | Guarantees compliance with DPDP and GDPR data privacy regulations; protects user data. | Analytical Data Marts | Data Engineering | Pre-Launch | **Ready for Dev** |
| **High** | **Anti-Cheat Payload Enrichment** | Require `tap_count` and `taps_per_second` in `tap_completed`; require `rng_hash` in `spin_completed`. | Essential for anti-fraud heuristics to detect autoclicker bots and wheel manipulation. | Client Telemetry SDK | Client Engineering | Pre-Launch | **Ready for Dev** |

---

## 3. Post-Launch Implementation Backlog (Optimization & Scaling)

| Priority | Requirement Name | Technical Description | Business & Analytical Rationale | Critical Dependency | Engineering Owner | Target Stage | Implementation Status |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **Medium** | **Automated dbt Transformations** | Schedule hourly dbt Core ELT models materializing dimensional facts and daily KPI rollups. | Replaces manual SQL scripts with automated, version-controlled analytics transformations. | Analytical Warehouse | Analytics Engineering | Post-Launch | **Proposed** |
| **Medium** | **Customer Support Telemetry** | Instrument `help_search_executed`, `faq_viewed`, and `ticket_submitted` events. | Identifies user UX friction, bug prevalence, and onboarding confusion points. | Support Portal / App | Frontend Team | Post-Launch | **Proposed** |
| **Medium** | **Multi-Currency Segregation** | Split user balance interface into distinct ledgers for `XP`, `Gems`, and `Tokens`. | Enables sustainable multi-currency game economy modeling and tokenomics tracking. | Economy Service | Product / Design | Post-Launch | **Proposed** |
| **Medium** | **Automated Slack / Email KPI Digest** | Scheduled Python bot delivering daily morning executive summary of DAU, revenue, and payouts. | Keeps executive leadership aligned on daily operational health without manual report pulling. | Analytical Data Layer | Data Analyst | Post-Launch | **Proposed** |
| **Low** | **Predictive Churn ML Pipeline** | Train logistic regression / XGBoost model predicting 30-day user churn probability from D7 activity. | Enables automated targeted push notification campaigns for at-risk users before churn occurs. | 6+ Months Prod Data | Data Science | Post-Launch | **Future Roadmap** |
| **Low** | **Enterprise BI Tool Migration** | Evaluate migrating from Streamlit to hosted Metabase or Apache Superset. | Provides advanced drag-and-drop self-service slicing for non-technical operations staff. | Cloud Analytics DB | BI Lead | Post-Launch | **Future Roadmap** |

