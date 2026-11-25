-- VELOOP WALLET & WITHDRAWAL SIMULATION — ADDITIVE PATCH
-- All records are synthetic and for analytical/testing use only.
-- Run after 01_schema_ddl.sql and after users have been loaded.

SET search_path TO veloop, public;

-- Add opening balance so account balances can be reconciled against ledger movements.
ALTER TABLE veloop.wallet_accounts
    ADD COLUMN IF NOT EXISTS opening_balance NUMERIC(14,2) NOT NULL DEFAULT 0.00
    CHECK (opening_balance >= 0.00);

-- Import workflow: first run wallet_import_staging.sql to create persistent staging tables.
-- Import the three CSVs into their matching staging tables (CSV format, Header=yes),
-- then run the INSERT ... SELECT statements in wallet_import_staging.sql.
-- This prevents column-order mistakes and preserves the SERIAL entry_id default.

-- A. Account reconciliation against opening balance and signed ledger movement.
WITH movement AS (
    SELECT account_id,
           SUM(CASE WHEN entry_type='CREDIT' THEN amount ELSE -amount END) AS net_movement
    FROM veloop.wallet_ledger GROUP BY account_id
)
SELECT a.account_id, a.account_type, a.opening_balance, a.current_balance,
       COALESCE(m.net_movement,0) AS ledger_net_movement,
       a.opening_balance + COALESCE(m.net_movement,0) AS expected_balance,
       a.current_balance - (a.opening_balance + COALESCE(m.net_movement,0)) AS difference
FROM veloop.wallet_accounts a
LEFT JOIN movement m USING(account_id)
WHERE a.currency_code='TOKENS'
ORDER BY ABS(a.current_balance - (a.opening_balance + COALESCE(m.net_movement,0))) DESC;

-- B. Double-entry transaction integrity: every transaction must balance.
SELECT transaction_id,
       SUM(CASE WHEN entry_type='DEBIT' THEN amount ELSE 0 END) AS total_debits,
       SUM(CASE WHEN entry_type='CREDIT' THEN amount ELSE 0 END) AS total_credits,
       SUM(CASE WHEN entry_type='DEBIT' THEN amount ELSE -amount END) AS imbalance
FROM veloop.wallet_ledger
GROUP BY transaction_id
HAVING SUM(CASE WHEN entry_type='DEBIT' THEN amount ELSE -amount END) <> 0;

-- C. Withdrawal KPI summary.
SELECT status, COUNT(*) AS withdrawal_count,
       ROUND(SUM(fiat_amount),2) AS requested_fiat_value_inr,
       ROUND(SUM(tokens_debited),2) AS requested_tokens
FROM veloop.withdrawals
GROUP BY status ORDER BY status;

-- D. Settled withdrawal value only (not all requested amounts).
SELECT COUNT(*) AS settled_withdrawals,
       ROUND(SUM(fiat_amount),2) AS settled_fiat_value_inr,
       ROUND(SUM(tokens_debited),2) AS settled_tokens
FROM veloop.withdrawals WHERE status='Settled';

-- E. Pending reserved tokens: processing requests are held in USER_LOCKED accounts.
SELECT COUNT(*) AS processing_withdrawals,
       ROUND(SUM(tokens_debited),2) AS tokens_in_processing
FROM veloop.withdrawals WHERE status='Processing';

-- F. Withdrawal processing time for statuses with processed_at.
SELECT status, COUNT(*) AS records,
       ROUND(AVG(EXTRACT(EPOCH FROM (processed_at-requested_at))/3600.0)::numeric,2) AS avg_processing_hours
FROM veloop.withdrawals WHERE processed_at IS NOT NULL
GROUP BY status ORDER BY status;

-- G. Wallet balance by account type.
SELECT account_type, currency_code, COUNT(*) AS accounts,
       ROUND(SUM(current_balance),2) AS total_balance
FROM veloop.wallet_accounts GROUP BY account_type,currency_code ORDER BY account_type;
