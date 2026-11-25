# Wallet & Withdrawal Simulation Patch

## Purpose
This patch adds a clearly labelled synthetic wallet and withdrawal dataset for analytical testing. It does not represent actual VELOOP production financial activity. The original source datasets are not modified.

## Generated files
- `wallet_accounts_simulated.csv` — 2,001 wallet accounts, including one simulated platform token pool.
- `wallet_ledger_simulated.csv` — 2,680 double-entry ledger rows across 1,340 balanced transactions.
- `withdrawals_simulated.csv` — 180 simulated withdrawal requests.
- `wallet_withdrawal_analytics.sql` — additive migration notes and analytical/reconciliation queries.

## Simulation assumptions
- Currency code `TOKENS` represents simulated platform reward tokens, not fiat money.
- A platform token pool starts with a synthetic opening balance of 1,000,000 tokens.
- The illustrative conversion is 100 tokens = INR 1.00. This is a test assumption, not a VELOOP exchange rate or financial promise.
- `Settled` withdrawals debit the user's available token balance.
- `Processing` withdrawals move tokens from `USER_AVAILABLE` to `USER_LOCKED`.
- `Reversed` withdrawals include a settlement and a separate refund ledger transaction.
- `Requested` and `Rejected` withdrawals do not debit wallet balances.
- Beneficiary details are masked placeholders, not real payment destinations.

## Generated status distribution
- Processing: 20
- Rejected: 30
- Requested: 20
- Reversed: 10
- Settled: 100

## Important schema adjustment
The existing `wallet_accounts` table does not contain an opening-balance field. Run the `ALTER TABLE` statement in `wallet_withdrawal_analytics.sql` before importing account rows. Use the explicit column order shown in the import notes.

## Import order
1. Run the existing project schema DDL first.
2. Ensure the `veloop.users` table is populated with the 1,000 source users.
3. Run the `ALTER TABLE` migration to add `opening_balance`.
4. Import `wallet_accounts_simulated.csv` into `veloop.wallet_accounts` with explicit column mapping: `account_id,user_id,currency_code,account_type,current_balance,status,opening_balance`.
5. Import `wallet_ledger_simulated.csv` into `veloop.wallet_ledger` with explicit columns; omit `entry_id` so PostgreSQL generates it.
6. Import `withdrawals_simulated.csv` into `veloop.withdrawals` with explicit columns.
7. Execute the reconciliation and KPI queries.

## Validation built into the generated data
- Every ledger transaction has exactly two entries: one DEBIT and one CREDIT.
- Debits equal credits for every transaction.
- Each account's `current_balance` equals `opening_balance` plus signed ledger movements.
- Every user_id references one of the supplied 1,000 users.
- Every withdrawal has a corresponding user_id.

These are generator-level checks. PostgreSQL validation is only complete after importing and running the SQL queries in the user's database.
