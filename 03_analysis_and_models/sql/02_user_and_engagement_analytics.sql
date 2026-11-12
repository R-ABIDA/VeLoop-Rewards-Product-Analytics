-- =============================================================================
-- VELOOP REWARDS — USER & ENGAGEMENT ANALYTICS QUERIES
-- Work Packages B & E | Deliverable 04 & 07
-- Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Dialect: PostgreSQL 15+
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Q1: Daily Active Users (DAU), WAU, MAU and Stickiness Ratio
-- -----------------------------------------------------------------------------
WITH daily_active AS (
    SELECT 
        activity_date,
        COUNT(DISTINCT user_id) AS dau
    FROM veloop.daily_activity
    WHERE qualifying_event = TRUE
    GROUP BY activity_date
),
rolling_active AS (
    SELECT
        activity_date,
        dau,
        -- Rolling 7-day active users (WAU proxy)
        AVG(dau) OVER (ORDER BY activity_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_wau_avg,
        -- Rolling 30-day active users (MAU proxy)
        AVG(dau) OVER (ORDER BY activity_date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS rolling_mau_avg
    FROM daily_active
)
SELECT 
    activity_date,
    dau,
    ROUND(rolling_wau_avg, 1) AS smoothed_wau,
    ROUND(rolling_mau_avg, 1) AS smoothed_mau,
    ROUND((dau / NULLIF(rolling_mau_avg, 0) * 100), 2) AS dau_to_mau_stickiness_pct
FROM rolling_active
ORDER BY activity_date DESC;

-- -----------------------------------------------------------------------------
-- Q2: User Retention Cohorts by Registration Week
-- -----------------------------------------------------------------------------
WITH user_cohorts AS (
    SELECT 
        user_id,
        DATE_TRUNC('week', registration_datetime)::DATE AS cohort_week
    FROM veloop.users
),
user_activities AS (
    SELECT 
        user_id,
        DATE_TRUNC('week', activity_date)::DATE AS activity_week
    FROM veloop.daily_activity
    GROUP BY user_id, DATE_TRUNC('week', activity_date)
)
SELECT 
    c.cohort_week,
    COUNT(DISTINCT c.user_id) AS cohort_size,
    COUNT(DISTINCT CASE WHEN a.activity_week = c.cohort_week THEN a.user_id END) AS week_0_active,
    COUNT(DISTINCT CASE WHEN a.activity_week = c.cohort_week + INTERVAL '1 week' THEN a.user_id END) AS week_1_active,
    COUNT(DISTINCT CASE WHEN a.activity_week = c.cohort_week + INTERVAL '2 weeks' THEN a.user_id END) AS week_2_active,
    COUNT(DISTINCT CASE WHEN a.activity_week = c.cohort_week + INTERVAL '3 weeks' THEN a.user_id END) AS week_3_active,
    COUNT(DISTINCT CASE WHEN a.activity_week = c.cohort_week + INTERVAL '4 weeks' THEN a.user_id END) AS week_4_active
FROM user_cohorts c
LEFT JOIN user_activities a ON c.user_id = a.user_id
GROUP BY c.cohort_week
ORDER BY c.cohort_week;

-- -----------------------------------------------------------------------------
-- Q3: Session Duration Distribution and Event Intensity
-- -----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN session_duration_minutes < 1.0 THEN '1. Under 1 Min'
        WHEN session_duration_minutes BETWEEN 1.0 AND 3.0 THEN '2. 1-3 Min (Micro)'
        WHEN session_duration_minutes BETWEEN 3.0 AND 10.0 THEN '3. 3-10 Min (Medium)'
        WHEN session_duration_minutes BETWEEN 10.0 AND 30.0 THEN '4. 10-30 Min (Deep)'
        ELSE '5. 30+ Min (Extended/Idle)'
    END AS duration_bracket,
    COUNT(session_id) AS total_sessions,
    ROUND(COUNT(session_id) * 100.0 / SUM(COUNT(session_id)) OVER (), 2) AS session_share_pct,
    ROUND(AVG(events_count), 1) AS avg_events_per_session
FROM veloop.sessions
GROUP BY 1
ORDER BY 1;

