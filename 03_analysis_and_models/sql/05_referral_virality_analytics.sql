-- =============================================================================
-- VELOOP REWARDS — REFERRAL & VIRAL GROWTH ANALYTICS & VIEWS
-- Dialect: PostgreSQL 15+
-- Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Document: Deliverable 07 & Work Package E
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS veloop;
SET search_path TO veloop, public;

-- =============================================================================
-- PART 1: SUPPORTED ANALYTICS FROM ACTUAL SIMULATED DATASETS
-- =============================================================================

-- -----------------------------------------------------------------------------
-- View 1 / Q1: Referral Acquisition Share & Source Detail Breakdown
-- Source: veloop.users
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_referral_acquisition_summary AS
SELECT 
    acquisition_source,
    COALESCE(referral_source_detail, 'Direct/Non-Referral') AS referral_source_detail,
    COUNT(user_id) AS acquired_users,
    ROUND(COUNT(user_id) * 100.0 / SUM(COUNT(user_id)) OVER (), 2) AS share_of_cohort_pct
FROM veloop.users
GROUP BY acquisition_source, referral_source_detail
ORDER BY acquired_users DESC;

-- -----------------------------------------------------------------------------
-- View 2 / Q2: Referral Activity Days & User Engagement Penetration
-- Source: veloop.daily_activity
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_referral_daily_activity AS
SELECT 
    'Daily Activity Cadence' AS metric_scope,
    COUNT(*) AS total_user_days,
    COUNT(CASE WHEN referral_activity = 'Yes' THEN 1 END) AS referral_active_user_days,
    COUNT(DISTINCT CASE WHEN referral_activity = 'Yes' THEN user_id END) AS unique_users_with_referral_activity,
    ROUND(COUNT(DISTINCT CASE WHEN referral_activity = 'Yes' THEN user_id END) * 100.0 / NULLIF(COUNT(DISTINCT user_id), 0), 2) AS user_referral_penetration_pct
FROM veloop.daily_activity;

-- -----------------------------------------------------------------------------
-- View 3 / Q3: Referral-Related Behavioral Feature Events Breakdown
-- Source: veloop.feature_events (feature_name = 'Referral')
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_referral_events_breakdown AS
SELECT 
    action_type,
    COUNT(event_id) AS event_volume,
    COUNT(DISTINCT user_id) AS unique_initiating_users,
    COUNT(DISTINCT session_id) AS unique_sessions,
    ROUND(COUNT(event_id)::NUMERIC / NULLIF(COUNT(DISTINCT user_id), 0), 2) AS avg_events_per_user
FROM veloop.feature_events
WHERE feature_name = 'Referral'
GROUP BY action_type
ORDER BY event_volume DESC;

-- -----------------------------------------------------------------------------
-- View 4 / Q4: Referral Code Data Quality & Format Integrity
-- Source: veloop.users
-- Validates: 8-character alphanumeric syntax (e.g., 'VL850800') and uniqueness
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_referral_code_audit AS
SELECT 
    COUNT(user_id) AS total_users,
    COUNT(referral_code) AS total_codes_assigned,
    COUNT(DISTINCT referral_code) AS unique_codes,
    COUNT(CASE WHEN referral_code IS NULL OR referral_code = '' THEN 1 END) AS missing_codes,
    COUNT(CASE WHEN LENGTH(referral_code) != 8 OR referral_code NOT LIKE 'VL%' THEN 1 END) AS invalid_format_codes,
    CASE 
        WHEN COUNT(user_id) = COUNT(DISTINCT referral_code) 
         AND COUNT(CASE WHEN referral_code IS NULL OR referral_code = '' THEN 1 END) = 0
         AND COUNT(CASE WHEN LENGTH(referral_code) != 8 OR referral_code NOT LIKE 'VL%' THEN 1 END) = 0
        THEN 'PASS: 100% Unique, Non-Null, Valid Format'
        ELSE 'FAIL: Format Anomalies Detected'
    END AS referral_code_audit_status
FROM veloop.users;

-- =============================================================================
-- PART 2: FUTURE-SOURCE RELATIONSHIP QUERIES (FOR WHEN REFERRER-REFEREE PAIRS ARRIVE)
-- NOTE: In the supplied simulated data, referral codes are present on individual user records,
-- but no referrer_user_id -> referee_user_id pair mapping exists.
-- The queries below provide the relational templates for future conversion tracking.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- View 5 / Q5: Verified Referrer-Referee Conversion Funnel (Future Specification)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_referral_conversion_funnel AS
SELECT 
    COUNT(referral_id) AS links_created,
    COUNT(CASE WHEN status IN ('Invite_Sent', 'Registered', 'Activated', 'Reward_Disbursed') THEN 1 END) AS invites_sent,
    COUNT(CASE WHEN referee_user_id IS NOT NULL THEN 1 END) AS verified_referees_registered,
    COUNT(CASE WHEN status IN ('Activated', 'Reward_Disbursed') THEN 1 END) AS verified_referees_activated,
    COUNT(CASE WHEN status = 'Reward_Disbursed' THEN 1 END) AS bonus_disbursed_conversions,
    ROUND(COUNT(CASE WHEN referee_user_id IS NOT NULL THEN 1 END) * 100.0 / NULLIF(COUNT(referral_id), 0), 2) AS signup_conversion_pct
FROM veloop.referrals;
