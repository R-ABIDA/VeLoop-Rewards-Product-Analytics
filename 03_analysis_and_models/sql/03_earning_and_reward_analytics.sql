-- =============================================================================
-- VELOOP REWARDS — EARNING & REWARD ANALYTICS QUERIES & VIEWS
-- Dialect: PostgreSQL 15+
-- Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Document: Deliverable 05 & Work Package C
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS veloop;
SET search_path TO veloop, public;

-- -----------------------------------------------------------------------------
-- View 1 / Q1: Micro-Task Execution Funnel (Viewed -> Started -> Completed)
-- Source: veloop.task_activity
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_task_conversion_funnel AS
SELECT 
    COUNT(activity_id) AS total_viewed,
    COUNT(CASE WHEN started_datetime IS NOT NULL THEN 1 END) AS total_started,
    COUNT(CASE WHEN task_status = 'Completed' THEN 1 END) AS total_completed,
    COUNT(CASE WHEN task_status = 'Abandoned' THEN 1 END) AS total_abandoned,
    COUNT(CASE WHEN task_status = 'Failed' THEN 1 END) AS total_failed,
    COUNT(CASE WHEN task_status = 'Pending' THEN 1 END) AS total_pending,
    ROUND(COUNT(CASE WHEN started_datetime IS NOT NULL THEN 1 END) * 100.0 / COUNT(activity_id), 2) AS start_rate_pct,
    ROUND(COUNT(CASE WHEN task_status = 'Completed' THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN started_datetime IS NOT NULL THEN 1 END), 0), 2) AS completion_from_start_pct,
    ROUND(COUNT(CASE WHEN task_status = 'Completed' THEN 1 END) * 100.0 / COUNT(activity_id), 2) AS overall_conversion_pct
FROM veloop.task_activity;

-- -----------------------------------------------------------------------------
-- View 2 / Q2: Task Performance and Abandonment by Category
-- Source: veloop.task_activity
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_category_earning_breakdown AS
SELECT 
    category,
    COUNT(activity_id) AS total_attempts,
    COUNT(CASE WHEN task_status = 'Completed' THEN 1 END) AS completed_count,
    COUNT(CASE WHEN task_status = 'Abandoned' THEN 1 END) AS abandoned_count,
    COUNT(CASE WHEN task_status = 'Failed' THEN 1 END) AS failed_count,
    ROUND(COUNT(CASE WHEN task_status = 'Completed' THEN 1 END) * 100.0 / COUNT(activity_id), 1) AS success_rate_pct,
    COUNT(CASE WHEN reward_status = 'Credited' THEN 1 END) AS credited_count,
    ROUND(COUNT(CASE WHEN reward_status = 'Credited' THEN 1 END) * 100.0 / COUNT(activity_id), 1) AS credit_rate_pct,
    COALESCE(SUM(reward_points_allocated), 0) AS total_points_allocated
FROM veloop.task_activity
GROUP BY category
ORDER BY total_attempts DESC;

-- -----------------------------------------------------------------------------
-- View 3 / Q3: Reward Credit Verification & Status Audit
-- Source: veloop.task_activity
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_reward_credit_audit AS
SELECT 
    reward_status,
    COUNT(activity_id) AS task_records,
    ROUND(COUNT(activity_id) * 100.0 / SUM(COUNT(activity_id)) OVER (), 2) AS status_share_pct,
    COUNT(CASE WHEN task_status = 'Completed' THEN 1 END) AS completed_tasks,
    COUNT(CASE WHEN task_status != 'Completed' THEN 1 END) AS non_completed_tasks
FROM veloop.task_activity
GROUP BY reward_status
ORDER BY task_records DESC;
