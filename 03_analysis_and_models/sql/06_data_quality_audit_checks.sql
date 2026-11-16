-- =============================================================================
-- VELOOP REWARDS — DATA QUALITY AUDIT & RECONCILIATION CHECKS (VIEWS)
-- Dialect: PostgreSQL 15+
-- Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Document: Deliverable 13 & Work Package G
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS veloop;
SET search_path TO veloop, public;

-- -----------------------------------------------------------------------------
-- View 1: Event Record Count Reconciliation (03_Feature_Events vs Audit)
-- Identifies duplicate event records injected for QA pipeline testing
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_dq_duplicate_events AS
SELECT 
    event_id,
    user_id,
    event_datetime,
    feature_name,
    action_type,
    COUNT(*) AS occurrence_count
FROM veloop.feature_events
GROUP BY event_id, user_id, event_datetime, feature_name, action_type
HAVING COUNT(*) > 1;

-- -----------------------------------------------------------------------------
-- View 2: User Identity Completeness & Duplicate Users Audit
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_dq_duplicate_users AS
SELECT 
    user_id,
    email,
    COUNT(*) AS occurrence_count
FROM veloop.users
GROUP BY user_id, email
HAVING COUNT(*) > 1;

-- -----------------------------------------------------------------------------
-- View 3: Orphan Events Check (Events with no matching User ID)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_dq_orphan_events AS
SELECT 
    e.event_id,
    e.user_id,
    e.session_id,
    e.event_datetime
FROM veloop.feature_events e
LEFT JOIN veloop.users u ON e.user_id = u.user_id
WHERE u.user_id IS NULL;

-- -----------------------------------------------------------------------------
-- View 4: Temporal & Logical Sequence Inconsistencies
-- Session duration must match or exceed start/end delta
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_dq_impossible_timestamps AS
SELECT 
    session_id,
    user_id,
    session_start,
    session_end,
    session_duration_seconds
FROM veloop.sessions
WHERE session_end IS NOT NULL 
  AND session_end < session_start;

-- -----------------------------------------------------------------------------
-- View 5: Double-Entry Ledger Balance Health Check (Future Payout System)
-- Mathematical Rule: SUM(Credits) - SUM(Debits) must equal 0.00
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_dq_unbalanced_transactions AS
SELECT 
    transaction_id,
    SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE -amount END) AS net_imbalance
FROM veloop.wallet_ledger
GROUP BY transaction_id
HAVING SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE -amount END) != 0.00;
