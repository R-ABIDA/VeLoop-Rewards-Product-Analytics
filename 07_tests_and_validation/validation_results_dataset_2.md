# Dataset 2 – SQL Analysis and Validation Results

## 1. Dataset Information

- Database: `veloop_rewards`
- Schema: `veloop`
- Table: `simulated_user_behavior`
- Total records: 1,000
- Unique user IDs: 1,000

## 2. SQL Analysis Execution

| No. | Analysis | Status |
|---:|---|---|
| 1 | Account Status | Completed |
| 2 | Onboarding Status | Completed |
| 3 | Verification Status | Completed |
| 4 | Acquisition Source | Completed |
| 5 | Top 10 States | Completed |
| 6 | Top 10 Cities | Completed |
| 7 | Age Group | Completed |
| 8 | Gender | Completed |
| 9 | Primary Device | Completed |
| 10 | Platform | Completed |
| 11 | Referral Source Detail | Completed |
| 12 | Monthly Registration | Completed |
| 13 | Account Status by State | Completed |
| 14 | Onboarding by Acquisition | Completed |
| 15 | Verification by Account Status | Completed |
| 16 | Referral Code Availability | Completed |
| 17 | Duplicate Referral Codes | Completed |
| 18 | Data Quality Summary | Completed |

## 3. Confirmed Results

- Total records: 1,000
- Unique user IDs: 1,000
- Unique emails: 1,000
- Missing names: 0
- Missing emails: 0
- Missing ages: 0
- Missing states: 0
- Missing cities: 0
- Missing registration dates: 0
- Missing referral details: 846
- Duplicate referral codes: 2 codes

## 4. Duplicate Referral Codes

| Code | Duplicate Count |
|---|---:|
| VL644238 | 2 |
| VL901676 | 2 |

## 5. Validation Conclusion

All 18 SQL analysis sections executed successfully and returned output.

The results were checked against the supplied Dataset 2 SQL output. The dataset has 1,000 records and 1,000 unique user IDs.

The duplicate referral codes and missing referral-source details are recorded as observations for further review. The original dataset remains unchanged.

## 6. Evidence

The original combined SQL output from pgAdmin is saved separately as:

`dataset_2_sql_analysis_output.txt`

The SQL query used for execution should also be saved in this folder as:

`dataset_2_combined_analysis.sql`

**Important:** This validation covers Dataset 2 only. Dataset 1 remains separate.