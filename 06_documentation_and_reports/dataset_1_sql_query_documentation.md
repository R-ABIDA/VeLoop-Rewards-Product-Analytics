# VELoop Rewards – Dataset 1 SQL Query Documentation

## 1. Dataset Information

| Item | Details |
|---|---|
| Project | VELoop Rewards – Product Analytics |
| Dataset | VELoop_Rewards_Data_01.csv |
| Database | veloop_rewards |
| Schema | veloop |
| Table | users |
| Total Records | 1,000 |
| SQL Language | PostgreSQL |

## 2. Objective

The objective of this SQL analysis is to examine user profile information and identify patterns related to account status, onboarding, acquisition channels, demographics, devices, verification, consent, XP balances, activity indicators, and registration trends.

## 3. SQL Analyses Performed

| No. | Analysis | SQL Operations Used |
|---:|---|---|
| 1 | Account Status | COUNT, GROUP BY, ORDER BY |
| 2 | Onboarding Status | COUNT, GROUP BY |
| 3 | Acquisition Source | COUNT, GROUP BY |
| 4 | Top 10 States | COUNT, GROUP BY, LIMIT |
| 5 | Top 10 Cities | COUNT, GROUP BY, LIMIT |
| 6 | Age Group Analysis | CASE, COUNT, GROUP BY |
| 7 | Gender Distribution | COUNT, GROUP BY |
| 8 | Platform Analysis | COUNT, GROUP BY |
| 9 | Primary Device Analysis | COUNT, GROUP BY |
| 10 | Email Verification | COUNT, GROUP BY |
| 11 | Consent Status | COUNT, GROUP BY |
| 12 | Marketing Opt-in | COUNT, GROUP BY |
| 13 | XP Analysis | AVG, MIN, MAX, SUM |
| 14 | User Activity | FILTER, COUNT |
| 15 | Registration Trend | DATE_TRUNC, COUNT, GROUP BY |
| 16 | Account Status by State | GROUP BY, COUNT |
| 17 | Onboarding by Acquisition Source | GROUP BY, COUNT |

## 4. Important SQL Concepts Applied

### COUNT()
Counts the number of records in each category.

### GROUP BY
Groups records based on one or more columns.

### ORDER BY
Sorts query results in ascending or descending order.

### LIMIT
Restricts the number of returned records, used for the top 10 states and cities.

### CASE
Creates age categories using conditional logic.

### Window Function
`SUM(COUNT(*)) OVER()` calculates the total grouped count for percentage calculations.

### Aggregate Functions
- `AVG()` calculates the average XP balance.
- `MIN()` identifies the minimum XP balance.
- `MAX()` identifies the maximum XP balance.
- `SUM()` calculates total XP.

### FILTER
Counts records that satisfy a specified condition, used for activity flags.

### DATE_TRUNC()
Groups registration dates by month.

## 5. Execution Summary

| Item | Result |
|---|---|
| Total SQL Analyses | 17 |
| Source Records | 1,000 |
| Source Table | veloop.users |
| Combined Query | Successfully Executed |
| Output | Single result grid |
| Database | PostgreSQL |

## 6. Conclusion

The SQL analysis successfully generated 17 user analytics sections using PostgreSQL. The queries demonstrate the use of aggregation, grouping, filtering, conditional logic, date functions, and window functions to analyze the supplied user dataset.