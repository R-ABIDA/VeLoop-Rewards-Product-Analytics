# VELoop Rewards – Product Analytics

## Project Overview

VELoop Rewards – Product Analytics is a data analysis project focused on understanding user profiles, account status, onboarding progress, acquisition sources, and registration patterns using SQL and PostgreSQL.

The project uses two separately supplied datasets. Each dataset is imported, validated, and analysed independently to preserve its original structure.

## Project Objectives

- Analyse user profile information.
- Understand account status and onboarding progress.
- Identify user acquisition patterns.
- Examine user distribution across states and cities.
- Analyse age groups, device categories, and platform information.
- Evaluate available user activity indicators.
- Perform SQL-based data quality checks.
- Generate meaningful business insights from the available data.

## Datasets

### Dataset 1 – User Profile Dataset

**Source:** `VELoop_Rewards_Data_01.csv`

- Records: 1,000
- PostgreSQL table: `veloop.users`
- Unique user IDs: 1,000

Analyses include account status, onboarding, acquisition source, geography, demographics, device distribution, verification, consent, XP balance, activity flags, and monthly registrations.

### Dataset 2 – Simulated User Behavior Dataset

**Source:** `VELOOP_Simulated_User_Behavior_1000.csv`

- Records: 1,000
- PostgreSQL table: `veloop.simulated_user_behavior`
- Unique user IDs: 1,000

This dataset is analysed independently using the available user-profile fields and SQL validation checks.

**Important:** The two datasets are not merged. Their records and analysis results are maintained separately.

## Technology Stack

| Technology | Purpose |
|---|---|
| PostgreSQL | Database management |
| SQL | Data analysis and validation |
| pgAdmin 4 | Database query execution |
| Excel | Dataset inspection |
| CSV | Source data format |

## Project Structure

```text
VeLoop-Rewards-Product-Analytics/
│
├── 01_raw_data/
│   ├── VELoop_Rewards_Data_01.csv
│   └── VELOOP_Simulated_User_Behavior_1000.csv
│
├── 02_sql_queries/
│   ├── dataset_1_combined_analysis.sql
│   └── dataset_2_combined_analysis.sql
│
├── 06_documentation_and_reports/
│   ├── README_dataset_1.md
│   ├── README_dataset_2.md
│   ├── dataset_1_user_analytics_report.md
│   ├── dataset_1_business_insights.md
│   ├── dataset_1_sql_analysis_output.md
│   ├── dataset_2_user_profile_analytics_report.md
│   └── dataset_2_sql_analysis_output.txt
│
└── 07_tests_and_validation/
    ├── validation_results_dataset_1.md
    └── validation_results_dataset_2.md
```

*The structure above describes the intended documentation and deliverables. Keep your existing repository folders and filenames if they differ.*

## Dataset 1 – Key Findings

- 56.8% of users have Active accounts.
- 72.2% of users completed onboarding.
- Organic Search is the largest acquisition source at 24.4%.
- The 25–34 age group represents 44.8% of users.
- Android is the most common device category at 65.9%.
- 85.5% of users have verified email addresses.
- 92.3% of users have accepted consent.

## Data Quality Validation

Data quality checks include:

- Total record count.
- Unique user ID validation.
- Duplicate email checks.
- Missing value checks.
- Age range validation.
- Date validation.
- Status value checks.
- Negative XP balance checks.

Four negative `days_since_registration` values were identified in Dataset 1 and require investigation. Original source data was preserved.

## Business Insights

The analysis helps identify:

- User account distribution.
- Onboarding completion gaps.
- Acquisition source contribution.
- Geographic user concentration.
- User demographic patterns.
- Device preferences.
- Email verification and consent status.
- Available user activity indicators.

## Project Limitations

The two profile-focused source datasets described in this legacy analysis do not themselves contain verified detailed transaction or event-level records for:

- Wallet transactions.
- Withdrawals.
- Referral transactions.
- Session events.
- Feature usage events.
- Task activity events.

These areas should not be presented as completed transaction-level analytics without the required source data.

## Conclusion

This project demonstrates the use of PostgreSQL and SQL for data cleaning checks, data validation, exploratory analysis, and business insight generation.

The two supplied datasets are maintained separately to ensure accurate analysis and preserve source data integrity.

## Scope clarification — 25 November 2026

This README documents the earlier two-dataset profile-analysis workstream only. The wider VELOOP project now also includes a simulated behavioral workbook, cleaned event/task/session files, and separate simulated wallet/withdrawal CSVs. Those additional files are test data and do not constitute production transactions or payment evidence. For the current seven-section dashboard, repository layout, automated test result, and database verification boundary, see [`README.md`](README.md) and [`PROJECT_IMPLEMENTATION_STATUS.md`](PROJECT_IMPLEMENTATION_STATUS.md).
