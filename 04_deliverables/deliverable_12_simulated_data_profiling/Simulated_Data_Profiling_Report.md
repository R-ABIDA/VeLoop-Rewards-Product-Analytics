# VELOOP REWARDS — SIMULATED DATA PROFILING REPORT
**Deliverable ID:** Deliverable 12  
**Work Package:** Work Package J — Simulated Data Profiling  
**Author:** Data Analyst Intern  
**Organization:** VELOOP Rewards  
**Date:** 2026-11-11  
**Integrity Label:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
**Classification:** Confirmed, Proposed, To Be Verified, Simulated  

---

## 1. Executive Summary & Objective

In accordance with **Work Package J (Sections 16, J1–J3)** of `Data_Analyst_01.pdf`, this report documents the comprehensive profiling of all supplied fictional datasets. 

The primary objective is to evaluate data volume, completeness, relational integrity, and the feasibility of computing core business KPIs against the supplied simulated schemas without fabricating unverified production claims.

### Key Profiling Highlights:
* **Supplied Data Volume:** Across the two supplied workbooks (`VELoop_Rewards_Data_01.xlsx` and `VELOOP_Simulated_User_Behavior_1000.xlsx`), a total of **9 tabular data sheets** containing **67,868 records** were profiled.
* **Referential Integrity is Pristine in Clean Sheets:** 100% of foreign keys in `02_Sessions` (7,913 rows), `03_Feature_Events` (35,704 rows), `04_Daily_Activity` (6,667 rows), `05_Task_Activity` (9,846 rows), and `06_Milestones` (4,799 rows) successfully resolve to valid parent `user_id` records in `Users_1000_Clean`. Zero orphan records exist.
* **KPI Feasibility Confirmed for User & Task Activity:** Engagement and user KPIs (DAU, session duration, task completion rate, active 30d ratio) are fully calculable from the provided data.
* **Financial & Withdrawal KPIs Blocked by Missing Dependencies:** Standalone ledgers for `Withdrawals`, `Wallet Transactions`, and `Referrals` are absent from the supplied files, preventing calculation of cash disbursement metrics, payout latency, and viral coefficient ($K\text{-factor}$).

---

## 2. Granular Sheet Profiling Results (J1)

| Sheet Name | Source File | Records | Columns | Date Range | Primary Key | Unique PKs | Duplicate Rows | Missing Values | Completeness |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Users_1000_Clean` | `VELoop_Rewards_Data_01.xlsx` | 1,000 | 27 | 2026-04-01 to 2026-09-15 | `user_id` | 1,000 | 0 | 119 | 99.56% |
| `Users_Messy_Audit` | `VELoop_Rewards_Data_01.xlsx` | 1,008 | 28 | 2026-04-01 to 2026-09-15 | `user_id` | 1,000 | 8 | 542 | 98.08% |
| `02_Sessions` | `Simulated_User_Behavior.xlsx` | 7,913 | 12 | 2026-04-01 to 2026-09-15 | `session_id` | 7,913 | 0 | 0 | 100.00% |
| `03_Feature_Events` | `Simulated_User_Behavior.xlsx` | 35,704 | 13 | 2026-04-01 to 2026-09-15 | `event_id` | 35,704 | 0 | 0 | 100.00% |
| `04_Daily_Activity` | `Simulated_User_Behavior.xlsx` | 6,667 | 17 | 2026-04-01 to 2026-09-15 | `(user_id, date)` | 6,667 | 0 | 0 | 100.00% |
| `05_Task_Activity` | `Simulated_User_Behavior.xlsx` | 9,846 | 12 | 2026-04-01 to 2026-09-15 | `activity_id` | 9,846 | 0 | 6,275 | 94.69% |
| `06_Milestones` | `Simulated_User_Behavior.xlsx` | 4,799 | 6 | 2026-04-01 to 2026-09-15 | `user_id` | 1,000 | 0 | 0 | 100.00% |
| `07_Feature_Usage` | `Simulated_User_Behavior.xlsx` | 15 | 7 | N/A | `feature_name` | 15 | 0 | 0 | 100.00% |
| `10_Event_Data_Quality_Audit`| `Simulated_User_Behavior.xlsx` | 35,714 | 13 | 2026-04-01 to 2026-09-15 | `event_id` | 35,704 | 10 | 24 | 99.95% |

---

## 3. Relational & Foreign Key Integrity Audit (J2)

Referential integrity was programmatically verified by testing foreign key relationships against the parent `Users_1000_Clean` dataset:

```mermaid
flowchart TD
    Users["Users_1000_Clean\n(1,000 Unique user_id)"]
    
    Users -->|user_id (100% Match / 0 Orphans)| S["02_Sessions\n(7,913 records)"]
    Users -->|user_id (100% Match / 0 Orphans)| FE["03_Feature_Events\n(35,704 records)"]
    Users -->|user_id (100% Match / 0 Orphans)| TA["05_Task_Activity\n(9,846 records)"]
    Users -->|user_id (100% Match / 0 Orphans)| DA["04_Daily_Activity\n(6,667 records)"]
    Users -->|user_id (100% Match / 0 Orphans)| M["06_Milestones\n(4,799 records)"]
    S -->|session_id (100% Match / 0 Orphans)| FE
```

### Relational Verification Matrix:
1. **`Users` $\rightarrow$ `Sessions`:** 1,000 parent users $\rightarrow$ 7,913 session records. Zero orphans. Integrity Status: **100% Valid**.
2. **`Users` $\rightarrow$ `Feature_Events`:** 1,000 parent users $\rightarrow$ 35,704 events. Zero orphans. Integrity Status: **100% Valid**.
3. **`Users` $\rightarrow$ `Task_Activity`:** 1,000 parent users $\rightarrow$ 9,846 task executions. Zero orphans. Integrity Status: **100% Valid**.
4. **`Users` $\rightarrow$ `Daily_Activity`:** 1,000 parent users $\rightarrow$ 6,667 daily rollups. Zero orphans. Integrity Status: **100% Valid**.
5. **`Users` $\rightarrow$ `Milestones`:** 1,000 parent users $\rightarrow$ 4,799 milestone events. Zero orphans. Integrity Status: **100% Valid**.
6. **`Sessions` $\rightarrow$ `Feature_Events`:** 7,913 sessions $\rightarrow$ 35,704 events. Every event resolves to a valid session. Integrity Status: **100% Valid**.

---

## 4. KPI Calculability & Feasibility Audit (J3)

A representative sample of proposed KPIs was tested directly against the supplied data to determine whether they can actually be computed:

| KPI Tested | Domain | Calculability Status | Simulated Calculated Value | Data Limitations & Gaps Identified |
| :--- | :---: | :---: | :---: | :--- |
| **Daily Active Users (DAU)** | User | **Fully Calculable** | Mean 44.4 active users/day | Fully supported by `04_Daily_Activity` (`active_flag = 'Yes'`). |
| **Task Completion Rate** | Engagement | **Fully Calculable** | **57.15%** (5,627 / 9,846 tasks) | Fully supported by `05_Task_Activity`. |
| **Average Session Duration** | Engagement | **Fully Calculable** | **52.3 seconds** | Fully supported by `02_Sessions`. |
| **Active 30d User Ratio** | User | **Fully Calculable** | **32.50%** (325 / 1,000 users) | Fully supported by `Users_1000_Clean`. |
| **Total Circulating XP** | Wallet | **Fully Calculable** | **172,480 XP** | Calculated from `Users_1000_Clean.xp_balance`. Lacks historical time-series ledger. |
| **Withdrawal Request Volume** | Withdrawals | **BLOCKED** | *Cannot Calculate* | Missing standalone `withdrawals` table; zero withdrawal events in stream. |
| **Withdrawal Fulfillment Rate** | Withdrawals | **BLOCKED** | *Cannot Calculate* | Missing settlement status webhooks and completed disbursement records. |
| **Average Payout Latency** | Withdrawals | **BLOCKED** | *Cannot Calculate* | Missing submission timestamps and bank credit timestamps. |
| **Viral Coefficient ($K\text{-factor}$)** | Referrals | **BLOCKED** | *Cannot Calculate* | Referral share events exist, but referee-to-referrer relational link is absent. |
| **Net Currency Velocity** | Wallet | **BLOCKED** | *Cannot Calculate* | Double-entry transaction ledger absent; only static point balance is stored. |

---

## 5. Artifact References

* **Deliverable 12 Excel Workbook:** [`04_deliverables/deliverable_12_simulated_data_profiling/Simulated_Data_Profiling_Workbook.xlsx`](file:///d:/Veloop%20data%20Analysis/04_deliverables/deliverable_12_simulated_data_profiling/Simulated_Data_Profiling_Workbook.xlsx)
* **Underlying Raw Datasets:** [`01_raw_data/VELoop_Rewards_Data_01.xlsx`](file:///d:/Veloop%20data%20Analysis/01_raw_data/VELoop_Rewards_Data_01.xlsx) and [`01_raw_data/VELOOP_Simulated_User_Behavior_1000.xlsx`](file:///d:/Veloop%20data%20Analysis/01_raw_data/VELOOP_Simulated_User_Behavior_1000.xlsx)

