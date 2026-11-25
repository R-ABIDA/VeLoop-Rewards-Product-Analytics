-- Run after the wallet_accounts opening_balance migration.
-- Permanent staging tables allow pgAdmin's Import/Export tool to use a separate connection.
CREATE TABLE IF NOT EXISTS veloop.stg_wallet_accounts_simulated (account_id text,user_id text,currency_code text,account_type text,opening_balance numeric,current_balance numeric,status text);
CREATE TABLE IF NOT EXISTS veloop.stg_wallet_ledger_simulated (transaction_id text,account_id text,entry_type text,amount numeric,balance_after numeric,reference_type text,reference_id text,narration text,created_at timestamptz);
CREATE TABLE IF NOT EXISTS veloop.stg_withdrawals_simulated (withdrawal_id text,user_id text,tokens_debited numeric,fiat_currency text,fiat_amount numeric,payout_rail text,beneficiary_account_masked text,status text,requested_at timestamptz,processed_at timestamptz,payout_reference text,failure_reason text);

-- Import the CSV files into these three staging tables using pgAdmin Import/Export.
-- Select CSV format and enable Header. Before re-importing, empty the staging tables:
-- TRUNCATE veloop.stg_wallet_accounts_simulated, veloop.stg_wallet_ledger_simulated, veloop.stg_withdrawals_simulated;

-- Make ledger imports idempotent by enforcing one row per transaction/account pair.
CREATE UNIQUE INDEX IF NOT EXISTS uq_wallet_ledger_tx_account
    ON veloop.wallet_ledger(transaction_id, account_id);

INSERT INTO veloop.wallet_accounts(account_id,user_id,currency_code,account_type,current_balance,status,opening_balance)
SELECT account_id,user_id,currency_code,account_type,current_balance,status,opening_balance
FROM veloop.stg_wallet_accounts_simulated
ON CONFLICT (account_id) DO UPDATE SET
    user_id=EXCLUDED.user_id, currency_code=EXCLUDED.currency_code,
    account_type=EXCLUDED.account_type, current_balance=EXCLUDED.current_balance,
    status=EXCLUDED.status, opening_balance=EXCLUDED.opening_balance;

INSERT INTO veloop.wallet_ledger(transaction_id,account_id,entry_type,amount,balance_after,reference_type,reference_id,narration,created_at)
SELECT transaction_id,account_id,entry_type,amount,balance_after,reference_type,reference_id,narration,created_at
FROM veloop.stg_wallet_ledger_simulated
ON CONFLICT (transaction_id,account_id) DO UPDATE SET
    entry_type=EXCLUDED.entry_type, amount=EXCLUDED.amount,
    balance_after=EXCLUDED.balance_after, reference_type=EXCLUDED.reference_type,
    reference_id=EXCLUDED.reference_id, narration=EXCLUDED.narration, created_at=EXCLUDED.created_at;

INSERT INTO veloop.withdrawals(withdrawal_id,user_id,tokens_debited,fiat_currency,fiat_amount,payout_rail,beneficiary_account_masked,status,requested_at,processed_at,payout_reference,failure_reason)
SELECT withdrawal_id,user_id,tokens_debited,fiat_currency,fiat_amount,payout_rail,beneficiary_account_masked,status,requested_at,processed_at,payout_reference,failure_reason
FROM veloop.stg_withdrawals_simulated
ON CONFLICT (withdrawal_id) DO UPDATE SET
    user_id=EXCLUDED.user_id, tokens_debited=EXCLUDED.tokens_debited,
    fiat_currency=EXCLUDED.fiat_currency, fiat_amount=EXCLUDED.fiat_amount,
    payout_rail=EXCLUDED.payout_rail, beneficiary_account_masked=EXCLUDED.beneficiary_account_masked,
    status=EXCLUDED.status, requested_at=EXCLUDED.requested_at,
    processed_at=EXCLUDED.processed_at, payout_reference=EXCLUDED.payout_reference,
    failure_reason=EXCLUDED.failure_reason;
