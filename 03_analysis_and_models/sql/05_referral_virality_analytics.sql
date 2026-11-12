-- =============================================================================
-- VELOOP REWARDS — REFERRAL & VIRAL GROWTH ANALYTICS QUERIES
-- Work Package E | Deliverable 07
-- Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Dialect: PostgreSQL 15+
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Q1: 4-Stage Referral Funnel Drop-Off
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(referral_id) AS links_created,
    COUNT(CASE WHEN status IN ('Invite_Shared', 'User_Registered', 'User_Activated', 'Bonus_Credited') THEN 1 END) AS invites_shared,
    COUNT(CASE WHEN registered_at IS NOT NULL THEN 1 END) AS referees_registered,
    COUNT(CASE WHEN activated_at IS NOT NULL THEN 1 END) AS referees_activated,
    ROUND(COUNT(CASE WHEN registered_at IS NOT NULL THEN 1 END) * 100.0 / NULLIF(COUNT(referral_id), 0), 2) AS registration_conversion_pct,
    ROUND(COUNT(CASE WHEN activated_at IS NOT NULL THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN registered_at IS NOT NULL THEN 1 END), 0), 2) AS activation_from_signup_pct
FROM veloop.referrals;

-- -----------------------------------------------------------------------------
-- Q2: Top Affiliate Referrers Leaderboard
-- -----------------------------------------------------------------------------
SELECT 
    r.referrer_user_id,
    u.username,
    u.platform,
    COUNT(r.referral_id) AS total_invites_sent,
    COUNT(r.referee_user_id) AS successful_signups,
    COUNT(CASE WHEN r.status = 'Bonus_Credited' THEN 1 END) AS paid_conversions,
    ROUND(COUNT(r.referee_user_id) * 100.0 / COUNT(r.referral_id), 1) AS conversion_rate_pct
FROM veloop.referrals r
JOIN veloop.users u ON r.referrer_user_id = u.user_id
GROUP BY r.referrer_user_id, u.username, u.platform
ORDER BY successful_signups DESC
LIMIT 15;

