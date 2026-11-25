
-- 1. ACCOUNT STATUS DISTRIBUTION
SELECT
    account_status,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM veloop.simulated_user_behavior
GROUP BY account_status
ORDER BY total_users DESC;


-- 2. ONBOARDING STATUS DISTRIBUTION
SELECT
    onboarding_status,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM veloop.simulated_user_behavior
GROUP BY onboarding_status
ORDER BY total_users DESC;


-- 3. EMAIL VERIFICATION STATUS
SELECT
    verification_status,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM veloop.simulated_user_behavior
GROUP BY verification_status
ORDER BY total_users DESC;


-- 4. ACQUISITION SOURCE ANALYSIS
SELECT
    acquisition_source,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM veloop.simulated_user_behavior
GROUP BY acquisition_source
ORDER BY total_users DESC;


-- 5. TOP 10 STATES BY USER COUNT
SELECT
    state,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM veloop.simulated_user_behavior), 2) AS percentage
FROM veloop.simulated_user_behavior
GROUP BY state
ORDER BY total_users DESC
LIMIT 10;


-- 6. TOP 10 CITIES BY USER COUNT
SELECT
    city,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM veloop.simulated_user_behavior), 2) AS percentage
FROM veloop.simulated_user_behavior
GROUP BY city
ORDER BY total_users DESC
LIMIT 10;


-- 7. AGE GROUP DISTRIBUTION
SELECT
    CASE
        WHEN age < 18 THEN 'Below 18'
        WHEN age BETWEEN 18 AND 24 THEN '18-24'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55+'
    END AS age_group,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM veloop.simulated_user_behavior
GROUP BY age_group
ORDER BY MIN(age);


-- 8. GENDER DISTRIBUTION
SELECT
    gender,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM veloop.simulated_user_behavior
GROUP BY gender
ORDER BY total_users DESC;


-- 9. PRIMARY DEVICE ANALYSIS
SELECT
    primary_device,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM veloop.simulated_user_behavior
GROUP BY primary_device
ORDER BY total_users DESC;


-- 10. PLATFORM ANALYSIS
SELECT
    platform,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM veloop.simulated_user_behavior
GROUP BY platform
ORDER BY total_users DESC;


-- 11. REFERRAL SOURCE DETAIL
SELECT
    COALESCE(referral_source_detail, 'Not specified') AS referral_source,
    COUNT(*) AS total_users,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM veloop.simulated_user_behavior
GROUP BY referral_source_detail
ORDER BY total_users DESC;


-- 12. MONTHLY REGISTRATION TREND
SELECT
    DATE_TRUNC('month', registration_datetime)::DATE AS registration_month,
    COUNT(*) AS new_users
FROM veloop.simulated_user_behavior
GROUP BY DATE_TRUNC('month', registration_datetime)
ORDER BY registration_month;


-- 13. ACCOUNT STATUS BY STATE
SELECT
    state,
    account_status,
    COUNT(*) AS total_users
FROM veloop.simulated_user_behavior
GROUP BY state, account_status
ORDER BY state, account_status;


-- 14. ONBOARDING STATUS BY ACQUISITION SOURCE
SELECT
    acquisition_source,
    onboarding_status,
    COUNT(*) AS total_users
FROM veloop.simulated_user_behavior
GROUP BY acquisition_source, onboarding_status
ORDER BY acquisition_source, onboarding_status;


-- 15. VERIFICATION STATUS BY ACCOUNT STATUS
SELECT
    account_status,
    verification_status,
    COUNT(*) AS total_users
FROM veloop.simulated_user_behavior
GROUP BY account_status, verification_status
ORDER BY account_status, verification_status;


-- 16. REFERRAL CODE AVAILABILITY
SELECT
    COUNT(*) AS total_users,
    COUNT(referral_code) AS users_with_referral_code,
    COUNT(*) - COUNT(referral_code) AS users_without_referral_code,
    COUNT(DISTINCT referral_code) AS unique_referral_codes
FROM veloop.simulated_user_behavior;


-- 17. DUPLICATE REFERRAL CODE CHECK
SELECT
    referral_code,
    COUNT(*) AS users_using_code
FROM veloop.simulated_user_behavior
GROUP BY referral_code
HAVING COUNT(*) > 1
ORDER BY users_using_code DESC;


-- 18. DATA QUALITY SUMMARY
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT user_id) AS unique_user_ids,
    COUNT(DISTINCT email) AS unique_emails,
    COUNT(*) FILTER (WHERE full_name IS NULL) AS missing_names,
    COUNT(*) FILTER (WHERE email IS NULL) AS missing_emails,
    COUNT(*) FILTER (WHERE age IS NULL) AS missing_ages,
    COUNT(*) FILTER (WHERE state IS NULL) AS missing_states,
    COUNT(*) FILTER (WHERE city IS NULL) AS missing_cities,
    COUNT(*) FILTER (WHERE registration_datetime IS NULL) AS missing_registration_dates,
    COUNT(*) FILTER (WHERE referral_source_detail IS NULL) AS missing_referral_details
FROM veloop.simulated_user_behavior;
