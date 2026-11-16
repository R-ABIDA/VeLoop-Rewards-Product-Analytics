-- =============================================================================
-- VELOOP REWARDS — PRODUCT ANALYTICS & RELATIONAL SCHEMA DDL
-- Dialect: PostgreSQL 15+
-- Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Document: Deliverable 10 | Logical Data Model & Physical DDL
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS veloop;
SET search_path TO veloop, public;

-- -----------------------------------------------------------------------------
-- 1. CORE IDENTITY: USERS
-- Mapped from original worksheet Users_1000_Clean (1,000 records)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(32) PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    age INT CHECK (age >= 18 AND age <= 100),
    gender VARCHAR(20) CHECK (gender IN ('Male', 'Female', 'Other', 'Prefer not to say')),
    state VARCHAR(100),
    city VARCHAR(100),
    registration_datetime TIMESTAMPTZ NOT NULL,
    acquisition_source VARCHAR(50) NOT NULL,
    referral_source_detail VARCHAR(100),
    primary_device VARCHAR(30) NOT NULL,
    platform VARCHAR(20) NOT NULL,
    account_status VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK (account_status IN ('Active', 'Inactive', 'Suspended', 'Deleted')),
    email_verification_status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (email_verification_status IN ('Verified', 'Pending', 'Unverified')),
    onboarding_status VARCHAR(20) NOT NULL DEFAULT 'Incomplete' CHECK (onboarding_status IN ('Completed', 'Incomplete', 'Skipped')),
    last_login_datetime TIMESTAMPTZ,
    lifetime_sessions INT NOT NULL DEFAULT 0 CHECK (lifetime_sessions >= 0),
    active_days INT NOT NULL DEFAULT 1 CHECK (active_days >= 0),
    xp_balance INT NOT NULL DEFAULT 0 CHECK (xp_balance >= 0),
    referral_code VARCHAR(32) NOT NULL UNIQUE,
    days_since_registration INT NOT NULL DEFAULT 0 CHECK (days_since_registration >= 0),
    is_active_7d BOOLEAN NOT NULL DEFAULT FALSE,
    is_active_30d BOOLEAN NOT NULL DEFAULT FALSE,
    consent_status VARCHAR(20) NOT NULL DEFAULT 'Granted',
    marketing_opt_in BOOLEAN NOT NULL DEFAULT FALSE,
    account_created_via VARCHAR(50),
    country CHAR(2) NOT NULL DEFAULT 'IN',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_status ON users(account_status);
CREATE INDEX IF NOT EXISTS idx_users_platform ON users(platform);
CREATE INDEX IF NOT EXISTS idx_users_device ON users(primary_device);
CREATE INDEX IF NOT EXISTS idx_users_reg_dt ON users(registration_datetime);
CREATE INDEX IF NOT EXISTS idx_users_acq_source ON users(acquisition_source);

-- -----------------------------------------------------------------------------
-- 2. ENGAGEMENT: SESSIONS
-- Mapped from original worksheet 02_Sessions (7,913 records)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    session_start TIMESTAMPTZ NOT NULL,
    session_end TIMESTAMPTZ,
    session_duration_seconds INT CHECK (session_duration_seconds >= 0),
    device VARCHAR(30) NOT NULL,
    platform VARCHAR(20) NOT NULL,
    entry_point VARCHAR(50),
    exit_feature VARCHAR(50),
    events_in_session INT NOT NULL DEFAULT 0 CHECK (events_in_session >= 0),
    features_used_count INT NOT NULL DEFAULT 0 CHECK (features_used_count >= 0),
    session_status VARCHAR(20) NOT NULL DEFAULT 'Completed' CHECK (session_status IN ('Completed', 'Abandoned', 'Timeout', 'Active')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sessions_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_start ON sessions(session_start);

-- -----------------------------------------------------------------------------
-- 3. BEHAVIORAL TELEMETRY: FEATURE_EVENTS
-- Mapped from original worksheet 03_Feature_Events (35,704 records)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS feature_events (
    event_id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    session_id VARCHAR(32) NOT NULL,
    event_datetime TIMESTAMPTZ NOT NULL,
    feature_name VARCHAR(50) NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    event_status VARCHAR(20) NOT NULL CHECK (event_status IN ('Success', 'Failed', 'Cancelled', 'Incomplete')),
    xp_earned INT NOT NULL DEFAULT 0 CHECK (xp_earned >= 0),
    event_duration_seconds INT CHECK (event_duration_seconds >= 0),
    device VARCHAR(30) NOT NULL,
    platform VARCHAR(20) NOT NULL,
    network_type VARCHAR(20),
    sequence_number INT NOT NULL DEFAULT 1 CHECK (sequence_number >= 1),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_events_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_events_session FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_events_user_id ON feature_events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_session_id ON feature_events(session_id);
CREATE INDEX IF NOT EXISTS idx_events_feature ON feature_events(feature_name);
CREATE INDEX IF NOT EXISTS idx_events_datetime ON feature_events(event_datetime);
CREATE INDEX IF NOT EXISTS idx_events_action ON feature_events(action_type);

-- -----------------------------------------------------------------------------
-- 4. DAILY USER ACTIVITY ROLLUPS: DAILY_ACTIVITY
-- Mapped from original worksheet 04_Daily_Activity (6,667 records)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS daily_activity (
    activity_id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    activity_date DATE NOT NULL,
    active_flag VARCHAR(5) NOT NULL DEFAULT 'Yes' CHECK (active_flag IN ('Yes', 'No')),
    sessions_count INT NOT NULL DEFAULT 0 CHECK (sessions_count >= 0),
    events_count INT NOT NULL DEFAULT 0 CHECK (events_count >= 0),
    features_accessed_count INT NOT NULL DEFAULT 0 CHECK (features_accessed_count >= 0),
    total_duration_minutes NUMERIC(8, 2) NOT NULL DEFAULT 0.0 CHECK (total_duration_minutes >= 0.0),
    daily_reward_claimed VARCHAR(5) NOT NULL DEFAULT 'No' CHECK (daily_reward_claimed IN ('Yes', 'No')),
    streak_activity VARCHAR(5) NOT NULL DEFAULT 'No' CHECK (streak_activity IN ('Yes', 'No')),
    tasks_started INT NOT NULL DEFAULT 0 CHECK (tasks_started >= 0),
    tasks_completed INT NOT NULL DEFAULT 0 CHECK (tasks_completed >= 0),
    spin_activity VARCHAR(5) NOT NULL DEFAULT 'No' CHECK (spin_activity IN ('Yes', 'No')),
    mining_activity VARCHAR(5) NOT NULL DEFAULT 'No' CHECK (mining_activity IN ('Yes', 'No')),
    referral_activity VARCHAR(5) NOT NULL DEFAULT 'No' CHECK (referral_activity IN ('Yes', 'No')),
    wallet_activity VARCHAR(5) NOT NULL DEFAULT 'No' CHECK (wallet_activity IN ('Yes', 'No')),
    daily_xp_earned INT NOT NULL DEFAULT 0 CHECK (daily_xp_earned >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_user_activity_date UNIQUE (user_id, activity_date),
    CONSTRAINT fk_daily_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_daily_user_id ON daily_activity(user_id);
CREATE INDEX IF NOT EXISTS idx_daily_date ON daily_activity(activity_date);
CREATE INDEX IF NOT EXISTS idx_daily_active_flag ON daily_activity(active_flag);

-- -----------------------------------------------------------------------------
-- 5. EARNINGS & TASKS: TASK_ACTIVITY
-- Mapped from original worksheet 05_Task_Activity (9,846 records)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS task_activity (
    activity_id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    task_id VARCHAR(32) NOT NULL,
    task_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    started_datetime TIMESTAMPTZ NOT NULL,
    completed_datetime TIMESTAMPTZ,
    task_status VARCHAR(20) NOT NULL CHECK (task_status IN ('Completed', 'Abandoned', 'Failed', 'Pending')),
    reward_points_allocated INT NOT NULL DEFAULT 0 CHECK (reward_points_allocated >= 0),
    reward_status VARCHAR(20) NOT NULL CHECK (reward_status IN ('Credited', 'Not Credited', 'Pending')),
    duration_seconds INT CHECK (duration_seconds >= 0),
    device VARCHAR(30) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tasks_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON task_activity(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_category ON task_activity(category);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON task_activity(task_status);
CREATE INDEX IF NOT EXISTS idx_tasks_reward_status ON task_activity(reward_status);

-- -----------------------------------------------------------------------------
-- 6. PROGRESSION & GAMIFICATION: MILESTONES
-- Mapped from original worksheet 06_Milestones (4,799 records)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS milestones (
    milestone_id VARCHAR(32) PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    milestone_type VARCHAR(50) NOT NULL,
    milestone_name VARCHAR(100) NOT NULL,
    achieved_datetime TIMESTAMPTZ NOT NULL,
    bonus_xp INT NOT NULL DEFAULT 0 CHECK (bonus_xp >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_milestones_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_milestones_user ON milestones(user_id);
CREATE INDEX IF NOT EXISTS idx_milestones_type ON milestones(milestone_type);

-- -----------------------------------------------------------------------------
-- 7. WALLET ACCOUNTS (FUTURE DOUBLE-ENTRY LEDGER DESIGN)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS wallet_accounts (
    account_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    currency_code VARCHAR(10) NOT NULL CHECK (currency_code IN ('XP', 'GEMS', 'TOKENS', 'INR')),
    account_type VARCHAR(20) NOT NULL CHECK (account_type IN ('USER_AVAILABLE', 'USER_LOCKED', 'SYSTEM_LIABILITY', 'RESERVE_CASH')),
    current_balance NUMERIC(14, 2) NOT NULL DEFAULT 0.00 CHECK (current_balance >= 0.00),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'FROZEN', 'CLOSED')),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_user_currency_acctype UNIQUE (user_id, currency_code, account_type),
    CONSTRAINT fk_wallet_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_wallet_user_id ON wallet_accounts(user_id);

-- -----------------------------------------------------------------------------
-- 8. IMMUTABLE WALLET LEDGER (DOUBLE-ENTRY ACCOUNTING)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS wallet_ledger (
    entry_id BIGSERIAL PRIMARY KEY,
    transaction_id VARCHAR(64) NOT NULL,
    account_id VARCHAR(64) NOT NULL,
    entry_type VARCHAR(10) NOT NULL CHECK (entry_type IN ('DEBIT', 'CREDIT')),
    amount NUMERIC(14, 2) NOT NULL CHECK (amount > 0.00),
    balance_after NUMERIC(14, 2) NOT NULL CHECK (balance_after >= 0.00),
    reference_type VARCHAR(50) NOT NULL CHECK (reference_type IN ('TASK_REWARD', 'DAILY_CHECKIN', 'WITHDRAWAL', 'REFERRAL_BONUS', 'ADMIN_ADJUSTMENT')),
    reference_id VARCHAR(64) NOT NULL,
    narration TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ledger_account FOREIGN KEY (account_id) REFERENCES wallet_accounts(account_id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_ledger_tx ON wallet_ledger(transaction_id);
CREATE INDEX IF NOT EXISTS idx_ledger_acc ON wallet_ledger(account_id);

-- -----------------------------------------------------------------------------
-- 9. WITHDRAWALS PIPELINE (FUTURE MONETARY PAYOUT DESIGN)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS withdrawals (
    withdrawal_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(32) NOT NULL,
    tokens_debited NUMERIC(14, 2) NOT NULL CHECK (tokens_debited >= 50.00),
    fiat_currency CHAR(3) NOT NULL DEFAULT 'INR',
    fiat_amount NUMERIC(12, 2) NOT NULL CHECK (fiat_amount > 0.00),
    payout_rail VARCHAR(30) NOT NULL CHECK (payout_rail IN ('UPI', 'Paytm', 'NEFT', 'IMPS')),
    beneficiary_account_masked VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Requested' CHECK (status IN ('Requested', 'Processing', 'Settled', 'Rejected', 'Reversed')),
    requested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMPTZ,
    payout_reference VARCHAR(100) UNIQUE,
    failure_reason VARCHAR(255),
    CONSTRAINT fk_withdrawals_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_withdrawals_status ON withdrawals(status);
CREATE INDEX IF NOT EXISTS idx_withdrawals_user ON withdrawals(user_id);

-- -----------------------------------------------------------------------------
-- 10. REFERRAL RELATIONSHIPS (FUTURE ATTRIBUTION DESIGN)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS referrals (
    referral_id VARCHAR(64) PRIMARY KEY,
    referrer_user_id VARCHAR(32) NOT NULL,
    referee_user_id VARCHAR(32) UNIQUE,
    referral_code VARCHAR(32) NOT NULL,
    channel VARCHAR(50) NOT NULL DEFAULT 'In-App Share',
    status VARCHAR(30) NOT NULL DEFAULT 'Link_Created' CHECK (status IN ('Link_Created', 'Invite_Sent', 'Registered', 'Activated', 'Reward_Disbursed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    registered_at TIMESTAMPTZ,
    activated_at TIMESTAMPTZ,
    reward_xp_credited INT DEFAULT 0 CHECK (reward_xp_credited >= 0),
    CONSTRAINT chk_referrer_referee_distinct CHECK (referrer_user_id != referee_user_id),
    CONSTRAINT fk_referrals_referrer FOREIGN KEY (referrer_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_referrals_referee FOREIGN KEY (referee_user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_user_id);
CREATE INDEX IF NOT EXISTS idx_referrals_referee ON referrals(referee_user_id);

-- -----------------------------------------------------------------------------
-- 11. DATA QUALITY & RECONCILIATION AUDIT LOG
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS data_quality_audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    audit_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dataset_name VARCHAR(100) NOT NULL,
    check_name VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO')),
    record_identifier VARCHAR(64),
    issue_description TEXT NOT NULL,
    remediation_status VARCHAR(30) NOT NULL DEFAULT 'DETECTED' CHECK (remediation_status IN ('DETECTED', 'QUARANTINED', 'CLEANED', 'RESOLVED'))
);

CREATE INDEX IF NOT EXISTS idx_dq_check ON data_quality_audit_log(check_name);
CREATE INDEX IF NOT EXISTS idx_dq_severity ON data_quality_audit_log(severity);

-- -----------------------------------------------------------------------------
-- 12. ACCOUNTING INTEGRITY: STATE MACHINE & LEDGER BALANCE ENFORCEMENT
-- -----------------------------------------------------------------------------

-- Trigger Function 1: Enforce valid state transitions for withdrawals
CREATE OR REPLACE FUNCTION fn_enforce_withdrawal_status_transition()
RETURNS TRIGGER AS $$
BEGIN
    -- Only validate when status actually changes
    IF OLD.status IS NOT DISTINCT FROM NEW.status THEN
        RETURN NEW;
    END IF;

    -- State transition rules:
    -- Requested -> Processing, Rejected
    -- Processing -> Settled, Rejected
    -- Settled -> Reversed
    -- Terminal states: Rejected, Reversed cannot transition
    IF OLD.status = 'Requested' AND NEW.status NOT IN ('Processing', 'Rejected') THEN
        RAISE EXCEPTION 'Invalid withdrawal transition from % to % for ID %', OLD.status, NEW.status, OLD.withdrawal_id;
    ELSIF OLD.status = 'Processing' AND NEW.status NOT IN ('Settled', 'Rejected') THEN
        RAISE EXCEPTION 'Invalid withdrawal transition from % to % for ID %', OLD.status, NEW.status, OLD.withdrawal_id;
    ELSIF OLD.status = 'Settled' AND NEW.status NOT IN ('Reversed') THEN
        RAISE EXCEPTION 'Invalid withdrawal transition from % to % for ID %', OLD.status, NEW.status, OLD.withdrawal_id;
    ELSIF OLD.status IN ('Rejected', 'Reversed') THEN
        RAISE EXCEPTION 'Cannot update terminal withdrawal status % for ID %', OLD.status, OLD.withdrawal_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_withdrawal_status_transition ON withdrawals;
CREATE TRIGGER trg_withdrawal_status_transition
BEFORE UPDATE ON withdrawals
FOR EACH ROW
EXECUTE FUNCTION fn_enforce_withdrawal_status_transition();

-- Trigger Function 2: Enforce Double-Entry Transaction Balance
-- Evaluates transaction integrity after commit/statement: debits must equal credits.
CREATE OR REPLACE FUNCTION fn_check_ledger_transaction_balance()
RETURNS TRIGGER AS $$
DECLARE
    v_net_imbalance NUMERIC(14, 2);
    v_tx_id VARCHAR(64);
BEGIN
    v_tx_id := NEW.transaction_id;

    SELECT COALESCE(SUM(CASE WHEN entry_type = 'DEBIT' THEN amount ELSE -amount END), 0.00)
    INTO v_net_imbalance
    FROM veloop.wallet_ledger
    WHERE transaction_id = v_tx_id;

    IF v_net_imbalance != 0.00 THEN
        RAISE EXCEPTION 'Accounting Integrity Violation: Transaction % is unbalanced! Net imbalance: %', v_tx_id, v_net_imbalance;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Constraint Trigger: evaluated at end of statement/transaction to allow paired inserts
DROP TRIGGER IF EXISTS trg_ledger_balance_check ON wallet_ledger;
CREATE CONSTRAINT TRIGGER trg_ledger_balance_check
AFTER INSERT OR UPDATE ON wallet_ledger
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION fn_check_ledger_transaction_balance();

-- Stored Procedure: Transaction-safe posting of balanced double-entry mutations
CREATE OR REPLACE PROCEDURE sp_record_balanced_transaction(
    p_tx_id VARCHAR(64),
    p_debit_account_id VARCHAR(64),
    p_credit_account_id VARCHAR(64),
    p_amount NUMERIC(14, 2),
    p_ref_type VARCHAR(50),
    p_ref_id VARCHAR(64),
    p_narration TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_debit_new_bal NUMERIC(14, 2);
    v_credit_new_bal NUMERIC(14, 2);
BEGIN
    IF p_amount <= 0.00 THEN
        RAISE EXCEPTION 'Transaction amount must be strictly positive: %', p_amount;
    END IF;

    -- Update debit account balance
    UPDATE veloop.wallet_accounts
    SET current_balance = current_balance - p_amount,
        updated_at = CURRENT_TIMESTAMP
    WHERE account_id = p_debit_account_id
    RETURNING current_balance INTO v_debit_new_bal;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Debit account % not found', p_debit_account_id;
    END IF;

    -- Update credit account balance
    UPDATE veloop.wallet_accounts
    SET current_balance = current_balance + p_amount,
        updated_at = CURRENT_TIMESTAMP
    WHERE account_id = p_credit_account_id
    RETURNING current_balance INTO v_credit_new_bal;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Credit account % not found', p_credit_account_id;
    END IF;

    -- Insert DEBIT entry
    INSERT INTO veloop.wallet_ledger (
        transaction_id, account_id, entry_type, amount, balance_after, reference_type, reference_id, narration
    ) VALUES (
        p_tx_id, p_debit_account_id, 'DEBIT', p_amount, v_debit_new_bal, p_ref_type, p_ref_id, p_narration
    );

    -- Insert CREDIT entry
    INSERT INTO veloop.wallet_ledger (
        transaction_id, account_id, entry_type, amount, balance_after, reference_type, reference_id, narration
    ) VALUES (
        p_tx_id, p_credit_account_id, 'CREDIT', p_amount, v_credit_new_bal, p_ref_type, p_ref_id, p_narration
    );
END;
$$;

