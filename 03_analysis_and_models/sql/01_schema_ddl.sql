-- =============================================================================
-- VELOOP REWARDS — PRODUCT ANALYTICS & LOGICAL DATA MODEL (DDL)
-- Work Package H & Deliverable 10
-- Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Dialect: PostgreSQL 15+
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS veloop;
SET search_path TO veloop, public;

-- -----------------------------------------------------------------------------
-- 1. USERS & ACCOUNT IDENTITY
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(64) PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    registration_datetime TIMESTAMPTZ NOT NULL,
    age INT CHECK (age >= 18 AND age <= 100),
    gender VARCHAR(20) CHECK (gender IN ('Male', 'Female', 'Other', 'Prefer Not to Say')),
    country CHAR(2) NOT NULL,
    platform VARCHAR(20) NOT NULL CHECK (platform IN ('Android', 'iOS', 'Web')),
    app_version VARCHAR(20) NOT NULL,
    account_status VARCHAR(20) NOT NULL DEFAULT 'Active' CHECK (account_status IN ('Active', 'Inactive', 'Suspended', 'Deleted')),
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    phone_verified BOOLEAN NOT NULL DEFAULT FALSE,
    xp_balance INT NOT NULL DEFAULT 0 CHECK (xp_balance >= 0),
    gems_balance INT NOT NULL DEFAULT 0 CHECK (gems_balance >= 0),
    tokens_balance NUMERIC(12, 2) NOT NULL DEFAULT 0.00 CHECK (tokens_balance >= 0),
    daily_streak INT NOT NULL DEFAULT 0 CHECK (daily_streak >= 0),
    active_days INT NOT NULL DEFAULT 1 CHECK (active_days >= 1),
    acquisition_source VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_account_status ON users(account_status);
CREATE INDEX IF NOT EXISTS idx_users_platform ON users(platform);
CREATE INDEX IF NOT EXISTS idx_users_registration_dt ON users(registration_datetime);

-- -----------------------------------------------------------------------------
-- 2. USER SESSIONS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    session_start TIMESTAMPTZ NOT NULL,
    session_end TIMESTAMPTZ,
    session_duration_minutes NUMERIC(8, 2) CHECK (session_duration_minutes >= 0),
    events_count INT NOT NULL DEFAULT 0 CHECK (events_count >= 0),
    device_model VARCHAR(100),
    os_version VARCHAR(50),
    ip_hash VARCHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_start ON sessions(session_start);

-- -----------------------------------------------------------------------------
-- 3. BEHAVIORAL FEATURE EVENTS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS feature_events (
    event_id VARCHAR(64) PRIMARY KEY,
    session_id VARCHAR(64) REFERENCES sessions(session_id) ON DELETE SET NULL,
    user_id VARCHAR(64) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    event_name VARCHAR(100) NOT NULL,
    feature_name VARCHAR(100) NOT NULL,
    event_datetime TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Started', 'Completed', 'Failed', 'Cancelled')),
    properties JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_events_user_feature ON feature_events(user_id, feature_name);
CREATE INDEX IF NOT EXISTS idx_events_datetime ON feature_events(event_datetime);
CREATE INDEX IF NOT EXISTS idx_events_name ON feature_events(event_name);

-- -----------------------------------------------------------------------------
-- 4. TASK CATALOG & TASK EXECUTION
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS task_catalog (
    task_id VARCHAR(64) PRIMARY KEY,
    task_name VARCHAR(150) NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    partner_id VARCHAR(64) NOT NULL,
    payout_xp INT NOT NULL CHECK (payout_xp >= 0),
    payout_gems INT NOT NULL DEFAULT 0,
    estimated_duration_seconds INT CHECK (estimated_duration_seconds > 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS task_activity (
    task_activity_id VARCHAR(64) PRIMARY KEY,
    task_id VARCHAR(64) NOT NULL REFERENCES task_catalog(task_id) ON DELETE RESTRICT,
    user_id VARCHAR(64) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    status VARCHAR(30) NOT NULL CHECK (status IN ('Viewed', 'Started', 'Completed', 'Failed', 'Abandoned')),
    task_viewed_at TIMESTAMPTZ NOT NULL,
    task_started_at TIMESTAMPTZ,
    task_completed_at TIMESTAMPTZ,
    duration_seconds INT CHECK (duration_seconds >= 0),
    partner_callback_status VARCHAR(30) CHECK (partner_callback_status IN ('Pending', 'Verified', 'Rejected')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_task_activity_user ON task_activity(user_id);
CREATE INDEX IF NOT EXISTS idx_task_activity_status ON task_activity(status);

-- -----------------------------------------------------------------------------
-- 5. REWARDS LEDGER
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS rewards_ledger (
    reward_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    task_activity_id VARCHAR(64) REFERENCES task_activity(task_activity_id) ON DELETE SET NULL,
    reward_type VARCHAR(30) NOT NULL CHECK (reward_type IN ('XP', 'GEMS', 'TOKENS')),
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    source_feature VARCHAR(50) NOT NULL,
    verification_status VARCHAR(30) NOT NULL CHECK (verification_status IN ('Credited', 'Pending', 'Under_Review', 'Reversed')),
    credited_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_rewards_user ON rewards_ledger(user_id);
CREATE INDEX IF NOT EXISTS idx_rewards_status ON rewards_ledger(verification_status);

-- -----------------------------------------------------------------------------
-- 6. WALLET TRANSACTIONS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS wallet_transactions (
    transaction_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    currency VARCHAR(20) NOT NULL CHECK (currency IN ('XP', 'GEMS', 'TOKENS')),
    transaction_type VARCHAR(30) NOT NULL CHECK (transaction_type IN ('Credit', 'Debit', 'Escrow_Hold', 'Reversal')),
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    balance_after NUMERIC(12, 2) NOT NULL CHECK (balance_after >= 0),
    reference_entity VARCHAR(50) NOT NULL,
    reference_id VARCHAR(64) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Settled', 'Pending', 'Failed', 'Cancelled')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_wallet_user_currency ON wallet_transactions(user_id, currency);

-- -----------------------------------------------------------------------------
-- 7. WITHDRAWALS PIPELINE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS withdrawals (
    withdrawal_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    tokens_amount NUMERIC(12, 2) NOT NULL CHECK (tokens_amount >= 50.00),
    fiat_currency CHAR(3) NOT NULL DEFAULT 'INR',
    fiat_amount NUMERIC(12, 2) NOT NULL CHECK (fiat_amount > 0),
    payout_method VARCHAR(30) NOT NULL CHECK (payout_method IN ('UPI', 'Paytm', 'Bank_Transfer', 'PayPal')),
    payout_destination_mask VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL CHECK (status IN ('Requested', 'Processing', 'Completed', 'Rejected', 'Reversed')),
    requested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMPTZ,
    settlement_reference VARCHAR(100),
    rejection_reason VARCHAR(255)
);

CREATE INDEX IF NOT EXISTS idx_withdrawals_status ON withdrawals(status);
CREATE INDEX IF NOT EXISTS idx_withdrawals_user ON withdrawals(user_id);

-- -----------------------------------------------------------------------------
-- 8. REFERRAL ATTRIBUTION
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS referrals (
    referral_id VARCHAR(64) PRIMARY KEY,
    referrer_user_id VARCHAR(64) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    referee_user_id VARCHAR(64) UNIQUE REFERENCES users(user_id) ON DELETE SET NULL,
    referral_code VARCHAR(32) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    status VARCHAR(30) NOT NULL CHECK (status IN ('Link_Created', 'Invite_Shared', 'User_Registered', 'User_Activated', 'Bonus_Credited')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    registered_at TIMESTAMPTZ,
    activated_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_referrals_referrer ON referrals(referrer_user_id);
CREATE INDEX IF NOT EXISTS idx_referrals_status ON referrals(status);

-- -----------------------------------------------------------------------------
-- 9. PRE-AGGREGATED DAILY ROLLUPS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS daily_activity (
    daily_activity_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    activity_date DATE NOT NULL,
    session_count INT NOT NULL DEFAULT 0,
    total_duration_minutes NUMERIC(8, 2) NOT NULL DEFAULT 0.00,
    events_triggered INT NOT NULL DEFAULT 0,
    tasks_completed INT NOT NULL DEFAULT 0,
    xp_earned INT NOT NULL DEFAULT 0,
    qualifying_event BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_user_date UNIQUE (user_id, activity_date)
);

CREATE INDEX IF NOT EXISTS idx_daily_activity_date ON daily_activity(activity_date);

