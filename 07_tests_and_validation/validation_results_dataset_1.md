# Dataset 1 – Data Validation Results

**Dataset:** `VELoop_Rewards_Data_01.csv`  
**Database Table:** `veloop.users`  
**Total Records:** 1,000  
**Validation Status:** Completed

## 1. Record and Uniqueness Checks

| Validation Check | Result | Status |
|---|---:|---|
| Total records | 1,000 | Passed |
| Unique user IDs | 1,000 | Passed |
| Duplicate user IDs | 0 | Passed |
| Unique emails | 1,000 | Passed |
| Duplicate email groups | 0 | Passed |

## 2. Missing Value Checks

| Field | Missing Records | Status |
|---|---:|---|
| User ID | 0 | Passed |
| Email | 0 | Passed |
| Age | 0 | Passed |
| State | 0 | Passed |
| City | 0 | Passed |
| Registration Date | 0 | Passed |

## 3. Data Validity Checks

| Validation Check | Result | Status |
|---|---:|---|
| Invalid ages (below 18 or above 100) | 0 | Passed |
| Future registration dates | 0 | Passed |
| Blank full names | 0 | Passed |
| Blank email values | 0 | Passed |
| Blank state values | 0 | Passed |
| Blank city values | 0 | Passed |
| Invalid account statuses | 0 | Passed |
| Invalid onboarding statuses | 0 | Passed |
| Invalid email verification statuses | 0 | Passed |
| Negative XP balances | 0 | Passed |

## 4. Data Anomaly Identified

| Field | Anomaly | Count |
|---|---|---:|
| `days_since_registration` | Negative values | 4 |

**Observation:** Four records contain negative values in `days_since_registration`. These records should be investigated because the field represents elapsed days since registration.

**Action:** Preserve the original dataset and document this anomaly. Do not modify the source records without approval.

## 5. Validation Summary

- 1,000 records were imported and validated.
- All 1,000 user IDs are unique.
- No duplicate email groups were identified.
- The checked required fields contain no missing values.
- The checked categorical values are valid.
- Four negative `days_since_registration` values were identified for further investigation.

## 6. Conclusion

Dataset 1 passed the reported record uniqueness, missing-value, and validity checks. One data anomaly was identified in `days_since_registration`, affecting four records. The original dataset has been preserved, and the anomaly has been documented for further review.

**Note:** Only the validation checks listed in this document are reported as completed. Additional checks should be documented only after their SQL results have been verified.