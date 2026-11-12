-- =============================================================================
-- VELOOP REWARDS — WALLET & WITHDRAWAL ANALYTICS QUERIES
-- Work Package D | Deliverable 06
-- Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Dialect: PostgreSQL 15+
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Q1: User XP & Token Balance Quartiles and Wealth Concentration
-- -----------------------------------------------------------------------------
SELECT 
    NTILE(4) OVER (ORDER BY xp_balance) AS balance_quartile,
    COUNT(user_id) AS users_in_tier,
    MIN(xp_balance) AS min_xp_in_tier,
    MAX(xp_balance) AS max_xp_in_tier,
    ROUND(AVG(xp_balance), 1) AS avg_xp_in_tier,
    SUM(xp_balance) AS total_xp_held,
    ROUND(SUM(xp_balance) * 100.0 / SUM(SUM(xp_balance)) OVER (), 2) AS wealth_share_pct
FROM veloop.users
GROUP BY user_id, xp_balance
ORDER BY balance_quartile;

-- -----------------------------------------------------------------------------
-- Q2: Withdrawal Queue Aging and SLA Compliance (< 24h)
-- -----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - requested_at)) / 3600.0 < 6.0 THEN '1. Under 6 Hours'
        WHEN EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - requested_at)) / 3600.0 BETWEEN 6.0 AND 12.0 THEN '2. 6-12 Hours'
        WHEN EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - requested_at)) / 3600.0 BETWEEN 12.0 AND 24.0 THEN '3. 12-24 Hours'
        WHEN EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - requested_at)) / 3600.0 BETWEEN 24.0 AND 48.0 THEN '4. 24-48 Hours (SLA Breach Risk)'
        ELSE '5. 48+ Hours (SLA Breached)'
    END AS queue_age_bracket,
    COUNT(withdrawal_id) AS pending_requests,
    SUM(fiat_amount) AS pending_volume_inr
FROM veloop.withdrawals
WHERE status IN ('Requested', 'Processing')
GROUP BY 1
ORDER BY 1;

-- -----------------------------------------------------------------------------
-- Q3: Payout Rails Share & Mean Settlement Latency
-- -----------------------------------------------------------------------------
SELECT 
    payout_method,
    COUNT(withdrawal_id) AS total_requests,
    COUNT(CASE WHEN status = 'Completed' THEN 1 END) AS settled_payouts,
    COUNT(CASE WHEN status = 'Rejected' THEN 1 END) AS rejected_payouts,
    SUM(CASE WHEN status = 'Completed' THEN fiat_amount ELSE 0 END) AS settled_volume_inr,
    ROUND(AVG(CASE WHEN status = 'Completed' THEN EXTRACT(EPOCH FROM (processed_at - requested_at)) / 3600.0 END), 2) AS mean_settlement_hours
FROM veloop.withdrawals
GROUP BY payout_method
ORDER BY settled_volume_inr DESC;

