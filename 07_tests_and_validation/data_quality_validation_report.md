# VELoop Rewards – Data Quality Validation Report

## 1. Introduction

Data quality validation was performed on the two original VELoop Rewards datasets using PostgreSQL.

The main objective was to verify data completeness, consistency, uniqueness, and validity before performing further data analysis.

Both datasets were imported and validated separately without merging or modifying the original records.

## 2. Dataset Information

| Description | Dataset 1 | Dataset 2 |
|---|---|---|
| Database schema | veloop | veloop |
| Table name | users | simulated_user_behavior |
| Total records | 1,000 | 1,000 |
| Unique user IDs | 1,000 | 1,000 |

## 3. Data Quality Checks Performed

The following validation checks were performed using SQL queries.

| No. | Validation Check | Dataset 1 | Dataset 2 |
|---|---|---|---|
| 1 | Total record count | Passed | Passed |
| 2 | Unique user IDs | Passed | Passed |
| 3 | Missing user IDs | 0 | 0 |
| 4 | Missing email values | 0 | 0 |
| 5 | Missing age values | 0 | 0 |
| 6 | Missing state values | 0 | 0 |
| 7 | Missing city values | 0 | 0 |
| 8 | Missing registration dates | 0 | 0 |
| 9 | Duplicate email groups | 0 | 0 |
| 10 | Age range validation (18–100) | 0 | 0 |
| 11 | Future registration dates | 0 | 0 |
| 12 | Blank checked text fields | 0 | 0 |
| 13 | Duplicate user IDs | 0 | 0 |
| 14 | Unexpected categorical values | 0 | 0 |

## 4. Additional Validation

### Dataset 1

- Negative XP balance records: 0.
- Negative values in `days_since_registration`: 4.
- The negative registration-day values require further investigation.

### Dataset 2

- Contains 1,000 records.
- Contains 1,000 unique user IDs.
- No duplicate user IDs were identified.

## 5. SQL Validation Methodology

PostgreSQL SQL queries were used to perform the following checks:

1. Record count and unique user identification.
2. Missing value detection.
3. Duplicate email detection.
4. Age range validation.
5. Registration date validation.
6. Blank text field detection.
7. Categorical value validation.
8. Negative numerical value detection.
9. Duplicate user ID detection.

## 6. Observations

- Both datasets contain 1,000 records.
- All user IDs are unique within their respective datasets.
- No missing values were found in the checked core fields.
- No duplicate email groups were identified.
- No unexpected categorical values were identified in the tested status fields.
- Four negative `days_since_registration` values were identified in Dataset 1 and require investigation.

## 7. Conclusion

The initial data quality validation indicates that both datasets are suitable for proceeding with the planned user-profile analysis, subject to reviewing the identified exceptions and completing the remaining validation checks.

The datasets have been maintained separately to preserve their original structure and information.

**Project:** VELoop Rewards – Product Analytics Dashboard  
**Domain:** Data Analysis  
**Database:** PostgreSQL  
**Schema:** veloop