# VELOOP REWARDS — MISSING DEPENDENCIES AND SOURCE REGISTER
**Project:** Product Analytics, Data Readiness & Data Management Blueprint  
**Organization:** VELOOP Rewards  
**Internship Role:** Data Analyst Intern  
**Integrity Label:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
**Classification:** Confirmed & To Be Verified  

---

## 1. Executive Summary of Available vs. Missing Inputs

An initial technical audit of the workspace (`d:\Veloop data Analysis`) was performed to verify all expected assignment inputs, policy documents, and data sources.

In strict compliance with **Section 4 (Dataset Import and Inspection)** and **Section 13 (First Action — Start Now)** of the project brief:
> *"If the dataset is not available, create the project structure and document the missing dependency. Ask me to provide the dataset. Do not silently generate replacement data."*

The findings are formally registered below:

### Summary Matrix

| Input Category | Item Name | Expected Status | Workspace Status | Evidentiary Tier | Analytical Impact & Mitigation Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Official PDF** | `Work_Schedule_and_Performance_Policy_VELOOP_Internship.pdf` | Required policy reference | **Missing from workspace** | To Be Verified | Establishes submission cadence, review policies, and evaluation rubric. **Action:** Requested from user. |
| **Official PDF** | `Data_Analyst_01.pdf` | Primary task assignment | **Missing from workspace** | To Be Verified | Contains detailed work package instructions and appendix guidelines. **Action:** Requested from user. |
| **Supplied Dataset** | `Users` (Clean & Messy Audit) | 1,000 users | **Available** (`VELoop_Rewards_Data_01.xlsx`) | Simulated | 1,000 clean user profiles (27 cols) + 1,008 audit rows (28 cols). Ready for profiling and quality audit. |
| **Supplied Dataset** | `Task Activity` | ~6,000 rows expected | **Available** (`VELOOP_Simulated_User_Behavior_1000.xlsx`) | Simulated | 9,846 task activity rows (12 cols). Exceeds minimum expected threshold. |
| **Supplied Dataset** | `Feature Events` | ~12,000 rows expected | **Available** (`VELOOP_Simulated_User_Behavior_1000.xlsx`) | Simulated | 35,704 feature event rows (13 cols) across 15 features. Exceeds minimum expected threshold. |
| **Supplied Dataset** | `Sessions` | Unspecified | **Available** (`VELOOP_Simulated_User_Behavior_1000.xlsx`) | Simulated | 7,913 session records (12 cols). |
| **Supplied Dataset** | `Daily Activity` | Unspecified | **Available** (`VELOOP_Simulated_User_Behavior_1000.xlsx`) | Simulated | 6,667 daily user rollup records (17 cols). |
| **Supplied Dataset** | `Milestones` | Unspecified | **Available** (`VELOOP_Simulated_User_Behavior_1000.xlsx`) | Simulated | 4,799 milestone achievement records (6 cols). |
| **Supplied Dataset** | `Feature Usage` | Unspecified | **Available** (`VELOOP_Simulated_User_Behavior_1000.xlsx`) | Simulated | 15 aggregated feature adoption summaries (7 cols). |
| **Supplied Dataset** | `Messy Data (Audit)` | 500+ rows expected | **Available** (`Users_Messy_Audit` & `10_Event_Data_Quality_Audit`) | Simulated | 1,008 messy user records + 35,714 event audit records. |
| **Missing Dataset** | `Rewards` (Standalone ledger) | ~5,000 rows expected | **Missing from workbooks** | To Be Verified | Disbursed reward amount, reward unit, and disbursement timestamp ledger missing. Only `reward_status` flag exists in Task Activity. |
| **Missing Dataset** | `Wallet` (Transactions) | ~3,500 rows expected | **Missing from workbooks** | To Be Verified | Double-entry transaction ledger missing. Only static `xp_balance` exists in Users sheet and `wallet_viewed` in Events. |
| **Missing Dataset** | `Withdrawals` (Requests & Payouts) | ~1,200 rows expected | **Missing from workbooks** | To Be Verified | Payout requests, methods (UPI/PayPal), processing times, and rejection statuses missing. |
| **Missing Dataset** | `Referrals` (Relational ledger) | ~900 rows expected | **Missing from workbooks** | To Be Verified | Referrer-to-referee linkage table missing. Only referral event views/shares and acquisition channel text exist. |

---

## 2. Granular Record Count Verification

The following actual counts were calculated directly from the supplied files in `Data/`:

| Dataset / Sheet Name | Source Workbook | Actual Row Count | Column Count | Key Identifiers Available |
| :--- | :--- | :---: | :---: | :--- |
| `Users_1000_Clean` | `VELoop_Rewards_Data_01.xlsx` | **1,000** | 27 | `user_id` (VLUSR000001 – VLUSR001000) |
| `Users_Messy_Audit` | `VELoop_Rewards_Data_01.xlsx` | **1,008** | 28 | `user_id` (Contains duplicates, nulls, invalid formats) |
| `01_Users_1000` | `VELOOP_Simulated_User_Behavior_1000.xlsx` | **1,000** | 16 | `user_id` (Demographics and account attributes) |
| `02_Sessions` | `VELOOP_Simulated_User_Behavior_1000.xlsx` | **7,913** | 12 | `session_id` (SESS0000001 – SESS0007913), `user_id` |
| `03_Feature_Events` | `VELOOP_Simulated_User_Behavior_1000.xlsx` | **35,704** | 13 | `event_id` (EVT00000001 – EVT00035704), `session_id`, `user_id` |
| `04_Daily_Activity` | `VELOOP_Simulated_User_Behavior_1000.xlsx` | **6,667** | 17 | `user_id`, `activity_date` |
| `05_Task_Activity` | `VELOOP_Simulated_User_Behavior_1000.xlsx` | **9,846** | 12 | `activity_id` (ACT0000001 – ACT0009846), `task_id`, `user_id` |
| `06_Milestones` | `VELOOP_Simulated_User_Behavior_1000.xlsx` | **4,799** | 6 | `user_id`, `milestone_type`, `session_id` |
| `07_Feature_Usage` | `VELOOP_Simulated_User_Behavior_1000.xlsx` | **15** | 7 | `feature_name` (Aggregated adoption metrics) |
| `10_Event_Data_Quality_Audit` | `VELOOP_Simulated_User_Behavior_1000.xlsx` | **35,714** | 13 | `event_id` (Contains dirty records for audit) |

---

## 3. Formal Request for Missing Dependencies

To ensure 100% complete adherence to all work packages without fabricating unverified production details:

1. **Official PDF Policy Documents:**
   - Please place `Work_Schedule_and_Performance_Policy_VELOOP_Internship.pdf` and `Data_Analyst_01.pdf` into the workspace root or `Data/` folder.
2. **Missing Standalone Tables (Rewards, Wallet, Withdrawals, Referrals):**
   - If standalone Excel or CSV files exist for the ~5,000 Rewards, ~3,500 Wallet Transactions, ~1,200 Withdrawals, and ~900 Referrals, please provide them.
   - If they are intentionally omitted to test our ability to specify relational architectures and propose realistic simulation schemas, we will formally design their complete logical schemas, specifications, DDL scripts, and document their synthetic data generation methodology under **Section 4 & Work Packages C, D, E**.

