# VELOOP REWARDS — SOURCE AND VERIFICATION REGISTER
**Deliverable ID:** Deliverable 19  
**Work Package:** Work Package S — Assumption & Verification Register  
**Author:** Data Analyst Intern  
**Organization:** VELOOP Rewards  
**Date:** 2026-11-11  
**Integrity Label:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
**Classification:** Confirmed, Proposed, To Be Verified, Simulated  

---

## 1. Executive Summary & Governance Directive

In strict adherence to **Section 6 & Section 25 of `Data_Analyst_01.pdf`**:
> *"The analyst must maintain a Source & Verification Register. The analyst must not silently convert assumptions into facts. Whenever the intern doesn't know something, they must record it. This prevents the analyst from guessing."*

In early-stage product analytics, undocumented assumptions lead to catastrophic schema redesigns and erroneous business conclusions. This register records every assumption, unknown engineering implementation detail, missing source input, and commercial policy rule.

---

## 2. Living Technical Assumptions & Verification Register

| Item ID | Unknown / Assumption Detail | Why It Matters to Analytics | Official Source Checked | Risk Level | Verification Owner | Verification Status | Operational Notes & Recommended Action |
| :---: | :--- | :--- | :--- | :---: | :--- | :---: | :--- |
| **A001** | Missing official PDF files (`Work_Schedule...pdf` & `Data_Analyst_01.pdf`) in original local directory | Establishes submission cadence, review policies, and evaluation rubric | Local workspace directory audit | **Medium** | Intern / Admin | **Confirmed from User Stream** | Transcribed and verified via user image stream; exact instructions incorporated. |
| **A002** | Absence of standalone `withdrawals` table (~1,200 expected records) | Required for computing payout request volume, processing latency, and method distribution | Raw Excel workbooks (`Data/`) | **High** | Lead Data Engineer | **Documented Missing Dependency** | Proposed relational schema in WP-D & WP-H; simulated operational model for dashboard demonstration. |
| **A003** | Absence of standalone `wallet_transactions` ledger (~3,500 expected records) | Required for balance auditing, double-entry reconciliation, and currency velocity | Raw Excel workbooks (`Data/`) | **High** | Lead Architect | **Documented Missing Dependency** | Proposed immutable double-entry ledger in WP-D & WP-H; verified mathematically against clean `xp_balance`. |
| **A004** | Absence of standalone `rewards` disbursement ledger (~5,000 expected records) | Required to distinguish task completion signals from backend financial credits | Raw Excel workbooks (`Data/`) | **High** | Backend Engineering | **Documented Missing Dependency** | Designed distinct `rewards_ledger` entity in WP-C & WP-H to decouple completion from disbursement. |
| **A005** | Absence of relational `referrals` attribution table (~900 expected records) | Required to link referee to referrer, calculate viral coefficient ($K$), and pay commissions | Raw Excel workbooks (`Data/`) | **High** | Growth / Backend | **Documented Missing Dependency** | Designed relational `referrals` entity in WP-E & WP-H with `referring_user_id` $\rightarrow$ `referred_user_id`. |
| **A006** | Commercial exchange rate between platform XP, Gems, Tokens, and fiat cash (INR/USD) | Required to calculate real dollar liability of circulating user point balances | Exchange Center sheet; product docs | **High** | Product Management / CFO | **To Be Verified** | Assumed 100 XP = 1.00 INR for analytical demonstration; requires official business confirmation. |
| **A007** | Production database engine and cloud hosting environment | Determines exact SQL dialect, indexing strategy, and pipeline orchestration tools | Assignment Technology Stack Guidelines | **Medium** | DevOps / Infrastructure | **Proposed Standard PostgreSQL** | Standardized on PostgreSQL 15+ compatible ANSI DDL with JSONB payload support. |
| **A008** | Minimum withdrawal threshold and transaction fee policy | Required to validate withdrawal request eligibility and calculate net platform disbursement | Withdrawal feature requirements | **Medium** | Finance Operations | **Proposed Standard Policy** | Assumed minimum threshold of 100 INR and 0% user fee for early growth; requires commercial sign-off. |
| **A009** | Third-party ad network revenue share and eCPM payouts | Required to calculate true gross margin per ad view and user unit economics | AdMob / Unity partner contracts | **High** | Commercial Partnerships | **To Be Verified** | Assumed average eCPM of $2.50 USD for rewarded video ads; requires finance confirmation. |
| **A010** | Policy on account deletion and PII retention window | Determines data retention lifecycle and GDPR/DPDP compliance procedures | Privacy policy / Legal team | **Medium** | Legal / Compliance | **Proposed Standard GDPR** | Proposed 30-day grace period followed by hard anonymization of analytical data marts. |

---

## 3. Artifact Reference
* **Deliverable 19 Excel Workbook:** [`04_deliverables/deliverable_19_assumption_and_verification_register/Source_and_Verification_Register.xlsx`](file:///d:/Veloop%20data%20Analysis/04_deliverables/deliverable_19_assumption_and_verification_register/Source_and_Verification_Register.xlsx)

