# Dataset 1 – User Profile Analytics

## 1. Dataset Overview

This dataset contains 1,000 user records provided for the VELoop Rewards Product Analytics project.

It is used to analyse user profiles, registration patterns, account status, onboarding progress, acquisition sources, and other user-level attributes.

## 2. Source Information

| Item | Details |
|---|---|
| Dataset | VELoop Rewards User Dataset |
| Source file | `users_import_data.csv` |
| Database Platform | Neon |
| Database Engine | PostgreSQL |
| Schema | `veloop` |
| Table | `veloop.users` |
| Total records | 1,000 |
| Unique user IDs | 1,000 |

## 3. Analytics Performed

The following analyses were performed using SQL:

1. Account status distribution
2. Onboarding status distribution
3. User acquisition source analysis
4. Top 10 states by user count
5. Top 10 cities by user count
6. Age-group distribution
7. Gender distribution
8. Platform distribution
9. Device distribution
10. Email verification status
11. Consent status
12. Marketing opt-in distribution
13. XP balance analysis
14. 7-day and 30-day activity flags
15. Monthly registration trend
16. Account status by state
17. Onboarding status by acquisition source

## 4. Tools and Technologies

- **Neon:** Cloud-hosted PostgreSQL database platform.
- **PostgreSQL:** Relational database engine used to store and query user records.
- **SQL:** Data querying, validation, aggregation, and analysis.
- **pgAdmin 4:** Database administration and SQL query execution.
- **Excel / CSV:** Source data inspection and validation.

## 5. Key Findings

- The dataset contains 1,000 unique user records.
- Active accounts represent 56.8% of users.
- Onboarding completion is 72.2%.
- Organic Search is the largest acquisition source at 24.4%.
- The 25–34 age group represents the largest age segment at 44.8%.
- Android is the most common device category at 65.9%.
- Email verification is complete for 85.5% of users.
- Consent is accepted by 92.3% of users.

## 6. Data Quality

Initial validation identified:

- No duplicate user IDs.
- No duplicate email addresses.
- No missing values in the checked key fields.
- No invalid age values in the checked range.
- Four records have negative `days_since_registration` values and require investigation.

The original dataset values were preserved. No source records were silently modified.

## 7. Important Limitation

This dataset supports user-profile and registration-related analysis. It does not contain detailed wallet transactions, withdrawal events, referral transactions, or session-level activity records.

Therefore, those business areas are not treated as completed transaction analytics based on this dataset.

## 8. Conclusion

Dataset 1 provides a foundation for understanding the VELoop Rewards user base. Its SQL analysis helps identify user demographics, account status, onboarding progress, acquisition patterns, and registration trends.

