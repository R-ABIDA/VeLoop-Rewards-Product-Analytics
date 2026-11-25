-- ============================================================
-- VELOOP REWARDS - DATASET 1
-- COMPLETE USER ANALYTICS
-- Database: veloop_rewards
-- Schema: veloop
-- Table: users
-- Total Records: 1000
-- Total Analyses: 17
-- ============================================================

-- 1. ACCOUNT STATUS
SELECT account_status, COUNT(*) AS total_users,
ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM veloop.users
GROUP BY account_status
ORDER BY total_users DESC;

-- 2. ONBOARDING STATUS
SELECT onboarding_status, COUNT(*) AS total_users,
ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM veloop.users
GROUP BY onboarding_status
ORDER BY total_users DESC;

-- 3. ACQUISITION SOURCE
SELECT acquisition_source, COUNT(*) AS total_users,
ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM veloop.users
GROUP BY acquisition_source
ORDER BY total_users DESC;

-- 4. TOP 10 STATES
SELECT state, COUNT(*) AS total_users
FROM veloop.users
GROUP BY state
ORDER BY total_users DESC
LIMIT 10;

-- 5. TOP 10 CITIES
SELECT city, COUNT(*) AS total_users
FROM veloop.users
GROUP BY city
ORDER BY total_users DESC
LIMIT 10;

-- 6. AGE GROUP ANALYSIS
SELECT
CASE
    WHEN age < 18 THEN 'Below 18'
    WHEN age BETWEEN 18 AND 24 THEN '18-24'
    WHEN age BETWEEN 25 AND 34 THEN '25-34'
    WHEN age BETWEEN 35 AND 44 THEN '35-44'
    WHEN age BETWEEN 45 AND 54 THEN '45-54'
    ELSE '55+'
END AS age_group,
COUNT(*) AS total_users
FROM veloop.users
WHERE age IS NOT NULL
GROUP BY age_group
ORDER BY MIN(age);

-- 7. GENDER DISTRIBUTION
SELECT gender, COUNT(*) AS total_users
FROM veloop.users
GROUP BY gender
ORDER BY total_users DESC;

-- 8. PLATFORM ANALYSIS
SELECT platform, COUNT(*) AS total_users
FROM veloop.users
GROUP BY platform
ORDER BY total_users DESC;

-- 9. PRIMARY DEVICE ANALYSIS
SELECT primary_device, COUNT(*) AS total_users
FROM veloop.users
GROUP BY primary_device
ORDER BY total_users DESC;

-- 10. EMAIL VERIFICATION
SELECT email_verification_status, COUNT(*) AS total_users
FROM veloop.users
GROUP BY email_verification_status
ORDER BY total_users DESC;

-- 11. CONSENT STATUS
SELECT consent_status, COUNT(*) AS total_users
FROM veloop.users
GROUP BY consent_status
ORDER BY total_users DESC;

-- 12. MARKETING OPT-IN
SELECT marketing_opt_in, COUNT(*) AS total_users
FROM veloop.users
GROUP BY marketing_opt_in
ORDER BY total_users DESC;

-- 13. XP ANALYSIS
SELECT
COUNT(*) AS total_users,
ROUND(AVG(xp_balance), 2) AS average_xp,
MIN(xp_balance) AS minimum_xp,
MAX(xp_balance) AS maximum_xp,
ROUND(SUM(xp_balance), 2) AS total_xp
FROM veloop.users;

-- 14. USER ACTIVITY
SELECT
COUNT(*) FILTER (WHERE is_active_7d = TRUE) AS active_7d,
COUNT(*) FILTER (WHERE is_active_30d = TRUE) AS active_30d,
COUNT(*) FILTER (WHERE is_active_7d = FALSE) AS inactive_7d,
COUNT(*) FILTER (WHERE is_active_30d = FALSE) AS inactive_30d
FROM veloop.users;

-- 15. REGISTRATION TREND
SELECT
DATE_TRUNC('month', registration_datetime)::date AS registration_month,
COUNT(*) AS registered_users
FROM veloop.users
WHERE registration_datetime IS NOT NULL
GROUP BY registration_month
ORDER BY registration_month;

-- 16. ACCOUNT STATUS BY STATE
SELECT state, account_status, COUNT(*) AS total_users
FROM veloop.users
GROUP BY state, account_status
ORDER BY state, total_users DESC;

-- 17. ONBOARDING BY ACQUISITION SOURCE
SELECT acquisition_source, onboarding_status,
COUNT(*) AS total_users
FROM veloop.users
GROUP BY acquisition_source, onboarding_status
ORDER BY acquisition_source, total_users DESC;
