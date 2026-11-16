-- =============================================================================
-- VELOOP REWARDS — WALLET & WITHDRAWAL ANALYTICS & RECONCILIATION VIEWS
-- Dialect: PostgreSQL 15+
-- Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Document: Deliverable 06 & Work Package D
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS veloop;
SET search_path TO veloop, public;

-- =============================================================================
-- PART 1: SUPPORTED ANALYTICS FROM ACTUAL SIMULATED DATASETS
-- =============================================================================

-- -----------------------------------------------------------------------------
-- View 1 / Q1: Wallet Interaction Volume and Unique User Penetration
-- Source: veloop.daily_activity
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_wallet_engagement_summary AS
SELECT 
    'Daily Activity Log' AS source_telemetry,
    COUNT(*) AS total_daily_records,
    COUNT(CASE WHEN wallet_activity = 'Yes' THEN 1 END) AS active_wallet_days,
    COUNT(DISTINCT CASE WHEN wallet_activity = 'Yes' THEN user_id END) AS unique_users_with_wallet_activity,
    ROUND(COUNT(DISTINCT CASE WHEN wallet_activity = 'Yes' THEN user_id END) * 100.0 / NULLIF(COUNT(DISTINCT user_id), 0), 2) AS user_wallet_penetration_pct
FROM veloop.daily_activity;

-- -----------------------------------------------------------------------------
-- View 2 / Q2: Wallet Feature Events Breakdown & Event Cadence
-- Source: veloop.feature_events (feature_name = 'Wallet')
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_wallet_events_breakdown AS
SELECT 
    action_type,
    COUNT(event_id) AS total_events,
    COUNT(DISTINCT user_id) AS unique_users,
    COUNT(DISTINCT session_id) AS distinct_sessions,
    ROUND(COUNT(event_id)::NUMERIC / NULLIF(COUNT(DISTINCT user_id), 0), 2) AS avg_events_per_user
FROM veloop.feature_events
WHERE feature_name = 'Wallet'
GROUP BY action_type
ORDER BY total_events DESC;

-- -----------------------------------------------------------------------------
-- View 3 / Q3: User Soft Currency (XP) Wealth Distribution & Concentration
-- Source: veloop.users
-- NOTE: XP represents gamified soft points, NOT fiat or monetary liability.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_user_xp_distribution AS
WITH user_xp_ranked AS (
    SELECT 
        user_id,
        xp_balance,
        NTILE(4) OVER (ORDER BY xp_balance) AS balance_quartile
    FROM veloop.users
)
SELECT 
    balance_quartile,
    COUNT(user_id) AS users_in_quartile,
    MIN(xp_balance) AS min_xp,
    MAX(xp_balance) AS max_xp,
    ROUND(AVG(xp_balance), 1) AS avg_xp,
    SUM(xp_balance) AS total_xp_held,
    ROUND(SUM(xp_balance) * 100.0 / SUM(SUM(xp_balance)) OVER (), 2) AS xp_share_pct
FROM user_xp_ranked
GROUP BY balance_quartile
ORDER BY balance_quartile;

-- =============================================================================
-- PART 2: FUTURE-SOURCE RECONCILIATION TEMPLATES (FOR WHEN REAL TRANSACTIONS ARRIVE)
-- NOTE: No monetary withdrawal or fiat payout records exist in the supplied Excel files.
-- The views below provide double-entry auditing logic for future source data.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- View 4 / Q4: Double-Entry Ledger Mathematical Reconciliation
-- In double-entry bookkeeping, credits must equal debits across system accounts:
-- SUM(DEBIT) - SUM(CREDIT) = 0.00
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_double_entry_reconciliation AS
SELECT 
    transaction_id,
    SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE 0.00 END) AS total_credits,
    SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE 0.00 END) AS total_debits,
    (SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE 0.00 END) - 
     SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE 0.00 END)) AS net_ledger_variance,
    CASE 
        WHEN (SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE 0.00 END) - 
              SUM(CASE WHEN entry_type = 'CREDIT' THEN amount ELSE 0.00 END)) = 0.00 
        THEN 'RECONCILED: Zero Balance Drift'
        ELSE 'IMBALANCE_DETECTED: Ledger Drift Warning'
    END AS reconciliation_status
FROM veloop.wallet_ledger
GROUP BY transaction_id;

-- -----------------------------------------------------------------------------
-- View 5 / Q5: Withdrawal Pipeline SLA Aging Queue (Template for Future Payouts)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_withdrawal_sla_queue_aging AS
SELECT 
    CASE 
        WHEN EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - requested_at)) / 3600.0 < 6.0 THEN '1. Under 6 Hours (On Track)'
        WHEN EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - requested_at)) / 3600.0 BETWEEN 6.0 AND 12.0 THEN '2. 6-12 Hours (Normal)'
        WHEN EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - requested_at)) / 3600.0 BETWEEN 12.0 AND 24.0 THEN '3. 12-24 Hours (Approaching SLA)'
        ELSE '4. 24+ Hours (SLA Breached)'
    END AS sla_aging_bracket,
    COUNT(withdrawal_id) AS pending_payout_requests,
    COALESCE(SUM(fiat_amount), 0.00) AS pending_fiat_volume_inr
FROM veloop.withdrawals
WHERE status IN ('Requested', 'Processing')
GROUP BY 1
ORDER BY 1;
