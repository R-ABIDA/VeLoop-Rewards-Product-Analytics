
-- =====================================================
-- VELoop Rewards - Data Quality Validation
-- Database: veloop_rewards
-- Schema: veloop
-- Datasets are validated separately
-- =====================================================


-- 1. RECORD COUNT AND UNIQUE USERS

SELECT
    'Dataset 1' AS dataset,
    COUNT(*) AS total_records,
    COUNT(DISTINCT user_id) AS unique_users
FROM veloop.users

UNION ALL

SELECT
    'Dataset 2',
    COUNT(*),
    COUNT(DISTINCT user_id)
FROM veloop.simulated_user_behavior;


-- 2. MISSING VALUE CHECKS

SELECT
    'Dataset 1' AS dataset,
    COUNT(*) FILTER (WHERE user_id IS NULL) AS missing_user_id,
    COUNT(*) FILTER (WHERE email IS NULL) AS missing_email,
    COUNT(*) FILTER (WHERE age IS NULL) AS missing_age,
    COUNT(*) FILTER (WHERE state IS NULL) AS missing_state,
    COUNT(*) FILTER (WHERE city IS NULL) AS missing_city,
    COUNT(*) FILTER (WHERE registration_datetime IS NULL)
        AS missing_registration_date
FROM veloop.users

UNION ALL

SELECT
    'Dataset 2',
    COUNT(*) FILTER (WHERE user_id IS NULL),
    COUNT(*) FILTER (WHERE email IS NULL),
    COUNT(*) FILTER (WHERE age IS NULL),
    COUNT(*) FILTER (WHERE state IS NULL),
    COUNT(*) FILTER (WHERE city IS NULL),
    COUNT(*) FILTER (WHERE registration_datetime IS NULL)
FROM veloop.simulated_user_behavior;


-- 3. DUPLICATE EMAIL CHECK

SELECT
    'Dataset 1' AS dataset,
    COUNT(*) AS duplicate_email_groups
FROM (
    SELECT email
    FROM veloop.users
    GROUP BY email
    HAVING COUNT(*) > 1
) d

UNION ALL

SELECT
    'Dataset 2',
    COUNT(*)
FROM (
    SELECT email
    FROM veloop.simulated_user_behavior
    GROUP BY email
    HAVING COUNT(*) > 1
) d;


-- 4. AGE RANGE VALIDATION

SELECT
    'Dataset 1' AS dataset,
    COUNT(*) AS invalid_age_records
FROM veloop.users
WHERE age < 18 OR age > 100

UNION ALL

SELECT
    'Dataset 2',
    COUNT(*)
FROM veloop.simulated_user_behavior
WHERE age < 18 OR age > 100;


-- 5. FUTURE REGISTRATION DATE CHECK

SELECT
    'Dataset 1' AS dataset,
    COUNT(*) AS future_registration_dates
FROM veloop.users
WHERE registration_datetime > CURRENT_TIMESTAMP

UNION ALL

SELECT
    'Dataset 2',
    COUNT(*)
FROM veloop.simulated_user_behavior
WHERE registration_datetime > CURRENT_TIMESTAMP;


-- 6. BLANK TEXT FIELD CHECK

SELECT 'Dataset 1' AS dataset,
       'full_name' AS field,
       COUNT(*) AS blank_records
FROM veloop.users
WHERE TRIM(full_name) = ''

UNION ALL

SELECT 'Dataset 1', 'email', COUNT(*)
FROM veloop.users
WHERE TRIM(email) = ''

UNION ALL

SELECT 'Dataset 1', 'state', COUNT(*)
FROM veloop.users
WHERE TRIM(state) = ''

UNION ALL

SELECT 'Dataset 1', 'city', COUNT(*)
FROM veloop.users
WHERE TRIM(city) = ''

UNION ALL

SELECT 'Dataset 2', 'full_name', COUNT(*)
FROM veloop.simulated_user_behavior
WHERE TRIM(full_name) = ''

UNION ALL

SELECT 'Dataset 2', 'email', COUNT(*)
FROM veloop.simulated_user_behavior
WHERE TRIM(email) = ''

UNION ALL

SELECT 'Dataset 2', 'state', COUNT(*)
FROM veloop.simulated_user_behavior
WHERE TRIM(state) = ''

UNION ALL

SELECT 'Dataset 2', 'city', COUNT(*)
FROM veloop.simulated_user_behavior
WHERE TRIM(city) = '';


-- 7. DUPLICATE USER ID CHECK

SELECT
    'Dataset 1' AS dataset,
    COUNT(*) - COUNT(DISTINCT user_id) AS duplicate_user_ids
FROM veloop.users

UNION ALL

SELECT
    'Dataset 2',
    COUNT(*) - COUNT(DISTINCT user_id)
FROM veloop.simulated_user_behavior;


-- 8. CATEGORICAL VALUE VALIDATION

SELECT 'Dataset 1 - Account Status' AS validation,
       COUNT(*) AS invalid_records
FROM veloop.users
WHERE account_status NOT IN
('Active', 'Inactive', 'Pending Verification', 'Suspended')

UNION ALL

SELECT 'Dataset 1 - Onboarding Status', COUNT(*)
FROM veloop.users
WHERE onboarding_status NOT IN
('Completed', 'Started', 'Not Started')

UNION ALL

SELECT 'Dataset 1 - Email Verification', COUNT(*)
FROM veloop.users
WHERE email_verification_status NOT IN ('Verified', 'Pending')

UNION ALL

SELECT 'Dataset 2 - Account Status', COUNT(*)
FROM veloop.simulated_user_behavior
WHERE account_status NOT IN
('Active', 'Inactive', 'Pending Verification', 'Suspended')

UNION ALL

SELECT 'Dataset 2 - Onboarding Status', COUNT(*)
FROM veloop.simulated_user_behavior
WHERE onboarding_status NOT IN
('Completed', 'Started', 'Not Started')

UNION ALL

SELECT 'Dataset 2 - Verification Status', COUNT(*)
FROM veloop.simulated_user_behavior
WHERE verification_status NOT IN ('Verified', 'Pending');


-- 9. NEGATIVE XP CHECK (DATASET 1 ONLY)

SELECT COUNT(*) AS negative_xp_records
FROM veloop.users
WHERE xp_balance < 0;


-- 10. NEGATIVE ACTIVITY CHECK (DATASET 1 ONLY)

SELECT
    COUNT(*) FILTER (WHERE lifetime_sessions < 0)
        AS negative_session_records,
    COUNT(*) FILTER (WHERE active_days < 0)
        AS negative_active_days
FROM veloop.users;


-- 11. NEGATIVE REGISTRATION DAYS CHECK

SELECT COUNT(*) AS negative_registration_days
FROM veloop.users
WHERE days_since_registration < 0;


-- 12. LOGIN BEFORE REGISTRATION CHECK

SELECT COUNT(*) AS login_before_registration
FROM veloop.users
WHERE last_login_datetime < registration_datetime;


-- 13. MISSING LAST LOGIN CHECK

SELECT COUNT(*) AS missing_last_login
FROM veloop.users
WHERE last_login_datetime IS NULL;


-- 14. MISSING REFERRAL CODE CHECK - DATASET 1

SELECT COUNT(*) AS missing_referral_codes
FROM veloop.users
WHERE referral_code IS NULL
   OR TRIM(referral_code) = '';


-- 15. MISSING REFERRAL CODE CHECK - DATASET 2

SELECT COUNT(*) AS missing_referral_codes
FROM veloop.simulated_user_behavior
WHERE referral_code IS NULL
   OR TRIM(referral_code) = '';


-- 16. DUPLICATE REFERRAL CODE CHECK - DATASET 1

SELECT COUNT(*) AS duplicate_referral_code_groups
FROM (
    SELECT referral_code
    FROM veloop.users
    WHERE referral_code IS NOT NULL
    GROUP BY referral_code
    HAVING COUNT(*) > 1
) duplicates;


-- 17. DUPLICATE REFERRAL CODE CHECK - DATASET 2

SELECT COUNT(*) AS duplicate_referral_code_groups
FROM (
    SELECT referral_code
    FROM veloop.simulated_user_behavior
    WHERE referral_code IS NOT NULL
    GROUP BY referral_code
    HAVING COUNT(*) > 1
) duplicates;
