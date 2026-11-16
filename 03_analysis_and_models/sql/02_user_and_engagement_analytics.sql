-- =============================================================================
-- VELOOP REWARDS — USER & ENGAGEMENT ANALYTICS QUERIES & VIEWS
-- Dialect: PostgreSQL 15+
-- Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Document: Deliverable 04 & Work Package B
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS veloop;
SET search_path TO veloop, public;

-- -----------------------------------------------------------------------------
-- View 1 / Q1: Daily Active Users (DAU), Rolling Trends and Stickiness
-- Source: veloop.daily_activity
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_daily_active_users AS
WITH daily_active AS (
    SELECT 
        activity_date,
        COUNT(DISTINCT user_id) AS dau
    FROM veloop.daily_activity
    WHERE active_flag = 'Yes'
    GROUP BY activity_date
),
rolling_active AS (
    SELECT
        activity_date,
        dau,
        -- Rolling 7-day active users (WAU proxy)
        ROUND(AVG(dau) OVER (ORDER BY activity_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 1) AS rolling_wau_avg,
        -- Rolling 30-day active users (MAU proxy)
        ROUND(AVG(dau) OVER (ORDER BY activity_date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW), 1) AS rolling_mau_avg
    FROM daily_active
)
SELECT 
    activity_date,
    dau,
    rolling_wau_avg AS smoothed_wau,
    rolling_mau_avg AS smoothed_mau,
    ROUND((dau / NULLIF(rolling_mau_avg, 0) * 100), 2) AS dau_to_mau_stickiness_pct
FROM rolling_active
ORDER BY activity_date DESC;

-- -----------------------------------------------------------------------------
-- View 2 / Q2: User Retention Cohorts by Registration Week
-- Source: veloop.users & veloop.daily_activity
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_user_retention_cohorts AS
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
    WHERE active_flag = 'Yes'
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
-- View 3 / Q3: Session Duration Distribution and Event Intensity
-- Source: veloop.sessions
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_session_duration_distribution AS
SELECT 
    CASE 
        WHEN session_duration_seconds < 60 THEN '1. Under 1 Min'
        WHEN session_duration_seconds BETWEEN 60 AND 180 THEN '2. 1-3 Min (Micro)'
        WHEN session_duration_seconds BETWEEN 180 AND 600 THEN '3. 3-10 Min (Medium)'
        WHEN session_duration_seconds BETWEEN 600 AND 1800 THEN '4. 10-30 Min (Deep)'
        ELSE '5. 30+ Min (Extended)'
    END AS duration_bracket,
    COUNT(session_id) AS total_sessions,
    ROUND(COUNT(session_id) * 100.0 / SUM(COUNT(session_id)) OVER (), 2) AS session_share_pct,
    ROUND(AVG(events_in_session), 1) AS avg_events_per_session
FROM veloop.sessions
GROUP BY 1
ORDER BY 1;
