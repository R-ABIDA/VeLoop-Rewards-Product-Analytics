# Dataset 2 – Simulated User Behavior Analytics

## 1. Dataset Overview

This dataset contains 1,000 records provided for the VELoop Rewards Product Analytics project.

It is stored separately from Dataset 1 and is used for additional user-profile analysis based on the columns available in the supplied file.

## 2. Source Information

| Item | Details |
|---|---|
| Dataset | VELoop Simulated User Behavior |
| Source file | `VELOOP_Simulated_User_Behavior_1000.csv` |
| Database Platform | Neon |
| Database Engine | PostgreSQL |
| Schema | `veloop` |
| Table | `veloop.simulated_user_behavior` |
| Total records | 1,000 |
| Unique user IDs | 1,000 |

## 3. Analytics Performed

SQL queries were used to examine the available records, including:

- Total records and unique user IDs
- Unique email addresses
- Missing values in important columns
- User profile information
- Available categorical distributions
- Numeric field summaries
- Data consistency and validation checks

Only analyses supported by the actual columns in this dataset should be included in the final results.

## 4. Tools and Technologies

- **Neon:** Cloud-hosted PostgreSQL database platform.
- **PostgreSQL:** Relational database engine used to store and query the dataset.
- **SQL:** Data exploration, aggregation, and validation.
- **pgAdmin 4:** Database administration and SQL query execution.
- **Excel / CSV:** Source data inspection and validation.

## 5. Data Quality

The initial validation output confirmed:

- 1,000 total records.
- 1,000 unique user IDs.
- No duplicate user IDs.
- No duplicate email addresses.
- No missing values in the checked fields.

The original source dataset was preserved. No source records were silently modified.

## 6. Important Limitation

Although the source filename includes the term "Simulated User Behavior", the supplied records primarily contain user-profile attributes.

The dataset does not provide verified event-level records for sessions, feature usage, task activity, wallet transactions, withdrawals, or referrals.

Therefore, actual behavioral-event analytics cannot be claimed from this dataset alone. Those analyses require their respective event-level or transaction-level source tables.

## 7. Conclusion

Dataset 2 provides a separate source of user-level information for the VELoop Rewards analytics project. It was imported and analysed independently to maintain the original dataset structure and avoid combining records from different sources.

