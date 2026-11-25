# VELoop Rewards – SQL Validation Results

## 1. Dataset Record Validation

| Dataset | Total Records | Unique User IDs | Duplicate User IDs |
|---|---:|---:|---:|
| Dataset 1 | 1,000 | 1,000 | 0 |
| Dataset 2 | 1,000 | 1,000 | 0 |

**Result:** Both datasets contain 1,000 unique user records.

## 2. Missing Value Validation

| Field | Dataset 1 Missing | Dataset 2 Missing |
|---|---:|---:|
| User ID | 0 | 0 |
| Email | 0 | 0 |
| Age | 0 | 0 |
| State | 0 | 0 |
| City | 0 | 0 |
| Registration Date | 0 | 0 |

**Result:** No missing values were found in the checked fields.

## 3. Duplicate and Validity Checks

| Validation | Dataset 1 | Dataset 2 |
|---|---:|---:|
| Duplicate email groups | 0 | 0 |
| Age outside 18–100 | 0 | 0 |
| Future registration dates | 0 | 0 |
| Blank checked text fields | 0 | 0 |
| Duplicate user IDs | 0 | 0 |

## 4. Categorical Validation

| Dataset | Category | Invalid Records |
|---|---|---:|
| Dataset 1 | Account Status | 0 |
| Dataset 1 | Onboarding Status | 0 |
| Dataset 1 | Email Verification | 0 |
| Dataset 2 | Account Status | 0 |
| Dataset 2 | Onboarding Status | 0 |
| Dataset 2 | Verification Status | 0 |

## 5. Numerical Validation

| Dataset | Check | Result |
|---|---|---:|
| Dataset 1 | Negative XP balances | 0 |
| Dataset 1 | Negative days since registration | 4 |

**Observation:** Four negative `days_since_registration` values require further investigation.

## 6. Pending Validation Results

The following checks require their actual SQL outputs before final sign-off:

- Negative lifetime sessions.
- Negative active days.
- Negative ages.
- Login date before registration date.
- Missing last login dates.
- Missing referral codes.
- Duplicate referral code groups.

## 7. Final Status

The confirmed SQL checks have been documented. The remaining checks and the four negative registration-day values must be reviewed before declaring the data-quality assessment complete.

Both original datasets remain separate in PostgreSQL.

## 8. Fresh Automated Test Run — 25 November 2026

The updated automated suite was executed using:

```bash
python -m unittest discover -s 07_tests_and_validation -p 'test_*.py'
```

**Result: 40 tests run, 40 passed, 0 failures, 0 errors.** See `evidence/test_execution_report.md` and `evidence/test_run.log` for the recorded result and verification boundary. This does not substitute for live PostgreSQL execution or public Streamlit deployment verification.
