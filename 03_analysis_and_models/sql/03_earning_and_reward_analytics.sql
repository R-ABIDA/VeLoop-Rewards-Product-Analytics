-- =============================================================================
-- VELOOP REWARDS — EARNING & REWARD ANALYTICS QUERIES
-- Work Package C | Deliverable 05
-- Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Dialect: PostgreSQL 15+
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Q1: Micro-Task Execution Funnel (Viewed -> Started -> Completed)
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(task_activity_id) AS total_viewed,
    COUNT(CASE WHEN task_started_at IS NOT NULL THEN 1 END) AS total_started,
    COUNT(CASE WHEN status = 'Completed' THEN 1 END) AS total_completed,
    COUNT(CASE WHEN status = 'Abandoned' THEN 1 END) AS total_abandoned,
    COUNT(CASE WHEN status = 'Failed' THEN 1 END) AS total_failed,
    ROUND(COUNT(CASE WHEN task_started_at IS NOT NULL THEN 1 END) * 100.0 / COUNT(task_activity_id), 2) AS start_rate_pct,
    ROUND(COUNT(CASE WHEN status = 'Completed' THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN task_started_at IS NOT NULL THEN 1 END), 0), 2) AS completion_from_start_pct,
    ROUND(COUNT(CASE WHEN status = 'Completed' THEN 1 END) * 100.0 / COUNT(task_activity_id), 2) AS overall_conversion_pct
FROM veloop.task_activity;

-- -----------------------------------------------------------------------------
-- Q2: Task Performance and Abandonment by Category
-- -----------------------------------------------------------------------------
SELECT 
    c.task_type,
    COUNT(a.task_activity_id) AS total_attempts,
    COUNT(CASE WHEN a.status = 'Completed' THEN 1 END) AS completed_count,
    COUNT(CASE WHEN a.status = 'Abandoned' THEN 1 END) AS abandoned_count,
    ROUND(COUNT(CASE WHEN a.status = 'Completed' THEN 1 END) * 100.0 / COUNT(a.task_activity_id), 1) AS success_rate_pct,
    ROUND(AVG(a.duration_seconds) / 60.0, 2) AS avg_duration_minutes,
    SUM(CASE WHEN a.status = 'Completed' THEN c.payout_xp ELSE 0 END) AS total_xp_disbursed
FROM veloop.task_catalog c
JOIN veloop.task_activity a ON c.task_id = a.task_id
GROUP BY c.task_type
ORDER BY total_attempts DESC;

-- -----------------------------------------------------------------------------
-- Q3: Reward Credit vs Reversal Audit
-- -----------------------------------------------------------------------------
SELECT 
    source_feature,
    reward_type,
    COUNT(reward_id) AS total_grants,
    SUM(amount) AS total_amount_granted,
    COUNT(CASE WHEN verification_status = 'Credited' THEN 1 END) AS clean_credits,
    COUNT(CASE WHEN verification_status = 'Pending' THEN 1 END) AS pending_credits,
    COUNT(CASE WHEN verification_status = 'Reversed' THEN 1 END) AS reversed_fraud_credits,
    ROUND(COUNT(CASE WHEN verification_status = 'Reversed' THEN 1 END) * 100.0 / COUNT(reward_id), 2) AS fraud_reversal_rate_pct
FROM veloop.rewards_ledger
GROUP BY source_feature, reward_type
ORDER BY total_amount_granted DESC;

