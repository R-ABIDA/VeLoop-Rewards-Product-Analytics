-- =============================================================================
-- VELOOP REWARDS — ENTERPRISE LOGICAL DATA MODEL (DDL)
-- Deliverable ID: Deliverable 10
-- Work Package: Work Package H — Logical Data Model & ER Diagram
-- Database Engine: PostgreSQL 15+ Compatible
-- Integrity Label: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Evidentiary Tier: Proposed Production Architecture
-- =============================================================================

-- Enable UUID extension if UUIDv4/UUIDv7 is preferred in production
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -----------------------------------------------------------------------------
-- 1. USERS ENTITY
-- Stores master user identity, demographic attributes, and account statuses.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id                     VARCHAR(16) PRIMARY KEY,
    email_hash                  CHAR(64) NOT NULL UNIQUE,
    full_name_masked            VARCHAR(100),
    age                         SMALLINT CHECK (age >= 13 AND age <= 100),
    gender                      VARCHAR(25) CHECK (gender IN ('Male', 'Female', 'Non-binary', 'Prefer not to say')),
    state                       VARCHAR(50),
    city                        VARCHAR(50),
    country                     VARCHAR(50) DEFAULT 'India',
    account_created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    account_status              VARCHAR(20) NOT NULL DEFAULT 'Active' 
                                CHECK (account_status IN ('Active', 'Inactive', 'Pending', 'Suspended', 'Dormant', 'Banned', 'Deleted')),
    email_verification_status   VARCHAR(15) NOT NULL DEFAULT 'Pending' 
                                CHECK (email_verification_status IN ('Verified', 'Pending', 'Failed')),
    email_verified_at           TIMESTAMP WITH TIME ZONE,
    onboarding_status           VARCHAR(20) NOT NULL DEFAULT 'Not_Started' 
                                CHECK (onboarding_status IN ('Not_Started', 'In_Progress', 'Completed', 'Skipped')),
    onboarding_completed_at     TIMESTAMP WITH TIME ZONE,
    account_created_via         VARCHAR(30) NOT NULL,
    acquisition_source          VARCHAR(50) NOT NULL,
    referral_code               VARCHAR(16) NOT NULL UNIQUE,
    referring_user_id           VARCHAR(16),
    primary_device              VARCHAR(20) CHECK (primary_device IN ('Android', 'iOS', 'Desktop Web', 'Mobile Web')),
    platform                    VARCHAR(20) CHECK (platform IN ('Web', 'Mobile App')),
    last_login_datetime         TIMESTAMP WITH TIME ZONE,
    last_activity_datetime      TIMESTAMP WITH TIME ZONE,
    lifetime_sessions           INTEGER DEFAULT 0 CHECK (lifetime_sessions >= 0),
    active_days                 INTEGER DEFAULT 0 CHECK (active_days >= 0),
    xp_balance                  INTEGER DEFAULT 0 CHECK (xp_balance >= 0),
    gem_balance                 INTEGER DEFAULT 0 CHECK (gem_balance >= 0),
    token_balance               DECIMAL(12, 4) DEFAULT 0.0000 CHECK (token_balance >= 0.0000),
    is_active_7d                VARCHAR(3) DEFAULT 'No' CHECK (is_active_7d IN ('Yes', 'No')),
    is_active_30d               VARCHAR(3) DEFAULT 'No' CHECK (is_active_30d IN ('Yes', 'No')),
    consent_status              VARCHAR(15) DEFAULT 'Accepted' CHECK (consent_status IN ('Accepted', 'Declined', 'Pending')),
    marketing_opt_in            VARCHAR(3) DEFAULT 'No' CHECK (marketing_opt_in IN ('Yes', 'No')),
    created_at                  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at                  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_users_referring_user FOREIGN KEY (referring_user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE INDEX idx_users_account_status ON users(account_status);
CREATE INDEX idx_users_acquisition_source ON users(acquisition_source);
CREATE INDEX idx_users_last_login ON users(last_login_datetime);

-- -----------------------------------------------------------------------------
-- 2. SESSIONS ENTITY
-- Captures contiguous user visits with duration, entry points, and exit screens.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sessions (
    session_id                  VARCHAR(16) PRIMARY KEY,
    user_id                     VARCHAR(16) NOT NULL,
    session_start               TIMESTAMP WITH TIME ZONE NOT NULL,
    session_end                 TIMESTAMP WITH TIME ZONE,
    session_duration_seconds    INTEGER CHECK (session_duration_seconds >= 0),
    device                      VARCHAR(20) NOT NULL CHECK (device IN ('Android', 'iOS', 'Desktop Web', 'Mobile Web')),
    platform                    VARCHAR(20) NOT NULL CHECK (platform IN ('Web', 'Mobile App')),
    entry_point                 VARCHAR(50) NOT NULL,
    exit_feature                VARCHAR(50),
    events_in_session           INTEGER DEFAULT 0 CHECK (events_in_session >= 0),
    features_used_count         INTEGER DEFAULT 0 CHECK (features_used_count >= 0),
    session_status              VARCHAR(20) DEFAULT 'Completed' CHECK (session_status IN ('Active', 'Completed', 'Timed_Out', 'Crashed')),
    created_at                  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sessions_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_start ON sessions(session_start);

-- -----------------------------------------------------------------------------
-- 3. FEATURE_EVENTS ENTITY
-- High-throughput append-only event stream logging every atomic user interaction.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS feature_events (
    event_id                    VARCHAR(16) PRIMARY KEY,
    session_id                  VARCHAR(16) NOT NULL,
    user_id                     VARCHAR(16) NOT NULL,
    event_datetime              TIMESTAMP WITH TIME ZONE NOT NULL,
    feature_name                VARCHAR(50) NOT NULL,
    event_name                  VARCHAR(50) NOT NULL,
    event_status                VARCHAR(20) NOT NULL CHECK (event_status IN ('Started', 'Completed', 'Failed', 'Viewed', 'Cancelled', 'Claimed', 'Shared')),
    device                      VARCHAR(20) NOT NULL,
    platform                    VARCHAR(20) NOT NULL,
    acquisition_source          VARCHAR(50),
    sequence_number             INTEGER NOT NULL CHECK (sequence_number >= 1),
    reward_related_flag         VARCHAR(3) DEFAULT 'No' CHECK (reward_related_flag IN ('Yes', 'No')),
    xp_related_flag             VARCHAR(3) DEFAULT 'No' CHECK (xp_related_flag IN ('Yes', 'No')),
    payload_json                JSONB,
    created_at                  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_events_session FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    CONSTRAINT fk_events_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_feature_events_user_time ON feature_events(user_id, event_datetime);
CREATE INDEX idx_feature_events_feature ON feature_events(feature_name);
CREATE INDEX idx_feature_events_name ON feature_events(event_name);

-- -----------------------------------------------------------------------------
-- 4. TASK_CATALOG ENTITY
-- Master registry of tasks, partner providers, durations, and reward terms.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS task_catalog (
    task_id                     VARCHAR(16) PRIMARY KEY,
    task_name                   VARCHAR(100) NOT NULL,
    task_category               VARCHAR(30) NOT NULL CHECK (task_category IN ('Advertisement', 'App Task', 'Survey', 'CAPTCHA', 'Social Activity', 'Game', 'Mission', 'Promotional Task')),
    partner_provider            VARCHAR(50) NOT NULL DEFAULT 'Internal',
    base_reward_amount          DECIMAL(10, 2) NOT NULL CHECK (base_reward_amount > 0),
    reward_unit                 VARCHAR(10) NOT NULL CHECK (reward_unit IN ('XP', 'GEMS', 'TOKENS', 'INR')),
    estimated_duration_seconds  INTEGER CHECK (estimated_duration_seconds >= 0),
    daily_cap_per_user          SMALLINT DEFAULT 10,
    is_active                   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at                  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 5. TASK_ACTIVITY ENTITY
-- Execution records for user task attempts, tracking funnel from view to reward.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS task_activity (
    activity_id                 VARCHAR(16) PRIMARY KEY,
    user_id                     VARCHAR(16) NOT NULL,
    task_id                     VARCHAR(16) NOT NULL,
    session_id                  VARCHAR(16),
    task_category               VARCHAR(30) NOT NULL,
    task_viewed_at              TIMESTAMP WITH TIME ZONE NOT NULL,
    task_started_at             TIMESTAMP WITH TIME ZONE NOT NULL,
    task_completed_at           TIMESTAMP WITH TIME ZONE,
    task_status                 VARCHAR(20) NOT NULL CHECK (task_status IN ('Completed', 'Abandoned', 'Failed', 'Pending')),
    failure_reason              VARCHAR(50) CHECK (failure_reason IN ('Validation failed', 'Task unavailable', 'Timeout', 'Incomplete action', 'User exited', 'Partner error')),
    reward_status               VARCHAR(20) NOT NULL DEFAULT 'Not Credited' CHECK (reward_status IN ('Credited', 'Not Credited', 'Pending')),
    device                      VARCHAR(20) NOT NULL,
    created_at                  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_task_activity_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_task_activity_task FOREIGN KEY (task_id) REFERENCES task_catalog(task_id) ON DELETE RESTRICT,
    CONSTRAINT fk_task_activity_session FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE SET NULL,
    CONSTRAINT chk_task_timing CHECK (task_completed_at IS NULL OR task_completed_at >= task_started_at)
);

CREATE INDEX idx_task_activity_user_id ON task_activity(user_id);
CREATE INDEX idx_task_activity_status ON task_activity(task_status);

-- -----------------------------------------------------------------------------
-- 6. WALLET_TRANSACTIONS ENTITY
-- Immutable double-entry financial ledger recording all balance credits and debits.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS wallet_transactions (
    transaction_id              VARCHAR(16) PRIMARY KEY,
    user_id                     VARCHAR(16) NOT NULL,
    timestamp                   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_type            VARCHAR(25) NOT NULL CHECK (transaction_type IN ('Reward Credit', 'Redemption', 'Reversal', 'Adjustment', 'Withdrawal Hold', 'Withdrawal Release')),
    amount                      DECIMAL(12, 2) NOT NULL,
    unit                        VARCHAR(10) NOT NULL CHECK (unit IN ('XP', 'GEMS', 'TOKENS', 'INR', 'USD')),
    status                      VARCHAR(15) NOT NULL DEFAULT 'Committed' CHECK (status IN ('Committed', 'Pending', 'Failed', 'Reversed')),
    source                      VARCHAR(30) NOT NULL,
    reference_id                VARCHAR(32) NOT NULL,
    reversal_transaction_id     VARCHAR(16),
    created_at                  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_wallet_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    CONSTRAINT fk_wallet_reversal FOREIGN KEY (reversal_transaction_id) REFERENCES wallet_transactions(transaction_id) ON DELETE SET NULL
);

CREATE INDEX idx_wallet_user_id ON wallet_transactions(user_id);
CREATE INDEX idx_wallet_timestamp ON wallet_transactions(timestamp);
CREATE INDEX idx_wallet_reference ON wallet_transactions(reference_id);

-- -----------------------------------------------------------------------------
-- 7. REWARDS_LEDGER ENTITY
-- Financial disbursement records linking earning events to wallet transactions.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS rewards_ledger (
    reward_id                   VARCHAR(16) PRIMARY KEY,
    activity_id                 VARCHAR(16),
    user_id                     VARCHAR(16) NOT NULL,
    reward_source               VARCHAR(30) NOT NULL,
    reward_amount               DECIMAL(12, 2) NOT NULL CHECK (reward_amount > 0),
    reward_unit                 VARCHAR(10) NOT NULL CHECK (reward_unit IN ('XP', 'GEMS', 'TOKENS', 'INR')),
    disbursement_status         VARCHAR(20) NOT NULL DEFAULT 'Credited' CHECK (disbursement_status IN ('Credited', 'Pending_Escrow', 'Reversed', 'Corrected')),
    transaction_id              VARCHAR(16) NOT NULL,
    credited_at                 TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at                  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_rewards_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_rewards_activity FOREIGN KEY (activity_id) REFERENCES task_activity(activity_id) ON DELETE SET NULL,
    CONSTRAINT fk_rewards_txn FOREIGN KEY (transaction_id) REFERENCES wallet_transactions(transaction_id) ON DELETE RESTRICT
);

CREATE INDEX idx_rewards_user_id ON rewards_ledger(user_id);
CREATE INDEX idx_rewards_credited_at ON rewards_ledger(credited_at);

-- -----------------------------------------------------------------------------
-- 8. WITHDRAWALS ENTITY
-- Cash payout requests, payment gateway fulfillment tracking, and status audit.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS withdrawals (
    withdrawal_id               VARCHAR(16) PRIMARY KEY,
    user_id                     VARCHAR(16) NOT NULL,
    requested_amount            DECIMAL(10, 2) NOT NULL CHECK (requested_amount >= 10.00),
    fee_amount                  DECIMAL(10, 2) DEFAULT 0.00 CHECK (fee_amount >= 0.00),
    payout_method               VARCHAR(20) NOT NULL CHECK (payout_method IN ('UPI', 'Paytm', 'Bank Transfer', 'PayPal', 'Crypto Voucher')),
    destination_hash            CHAR(64) NOT NULL,
    requested_timestamp         TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processing_timestamp        TIMESTAMP WITH TIME ZONE,
    final_timestamp             TIMESTAMP WITH TIME ZONE,
    status                      VARCHAR(20) NOT NULL DEFAULT 'Requested' CHECK (status IN ('Requested', 'Under_Review', 'Processing', 'Completed', 'Rejected', 'Reversed')),
    gateway_name                VARCHAR(50),
    gateway_txn_id              VARCHAR(64),
    rejection_reason            VARCHAR(50) CHECK (rejection_reason IN ('Invalid Payment Address', 'Failed Minimum Balance', 'Suspected Bot Activity', 'Multiple Accounts on Payment Address', 'Gateway Timeout', 'KYC Pending')),
    created_at                  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_withdrawals_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    CONSTRAINT chk_withdrawal_dates CHECK (final_timestamp IS NULL OR final_timestamp >= requested_timestamp)
);

CREATE INDEX idx_withdrawals_user_id ON withdrawals(user_id);
CREATE INDEX idx_withdrawals_status ON withdrawals(status);
CREATE INDEX idx_withdrawals_requested ON withdrawals(requested_timestamp);

-- -----------------------------------------------------------------------------
-- 9. REFERRALS ENTITY
-- Relational attribution tree mapping referrers to referees and tracking conversion.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS referrals (
    referral_id                 VARCHAR(16) PRIMARY KEY,
    referring_user_id           VARCHAR(16) NOT NULL,
    referred_user_id            VARCHAR(16) NOT NULL UNIQUE,
    creation_timestamp          TIMESTAMP WITH TIME ZONE NOT NULL,
    registration_timestamp      TIMESTAMP WITH TIME ZONE NOT NULL,
    activation_timestamp        TIMESTAMP WITH TIME ZONE,
    conversion_timestamp        TIMESTAMP WITH TIME ZONE,
    referral_status             VARCHAR(20) NOT NULL DEFAULT 'Registered' CHECK (referral_status IN ('Created', 'Registered', 'Activated', 'Converted', 'Rejected')),
    referral_source             VARCHAR(30) NOT NULL,
    commission_amount           DECIMAL(10, 2) CHECK (commission_amount >= 0),
    commission_unit             VARCHAR(10) DEFAULT 'XP',
    rejection_reason            VARCHAR(50),
    created_at                  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_referrals_referrer FOREIGN KEY (referring_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_referrals_referee FOREIGN KEY (referred_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT chk_no_self_referral CHECK (referring_user_id != referred_user_id)
);

CREATE INDEX idx_referrals_referrer ON referrals(referring_user_id);
CREATE INDEX idx_referrals_status ON referrals(referral_status);

-- -----------------------------------------------------------------------------
-- 10. DAILY_ACTIVITY ENTITY
-- Pre-aggregated rollups per user per calendar date for fast executive BI queries.
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS daily_activity (
    user_id                     VARCHAR(16) NOT NULL,
    activity_date               DATE NOT NULL,
    session_count               INTEGER DEFAULT 0 CHECK (session_count >= 0),
    session_duration_minutes    DECIMAL(8, 2) DEFAULT 0.0 CHECK (session_duration_minutes >= 0.0),
    event_count                 INTEGER DEFAULT 0 CHECK (event_count >= 0),
    feature_count               INTEGER DEFAULT 0 CHECK (feature_count >= 0),
    task_count                  INTEGER DEFAULT 0 CHECK (task_count >= 0),
    completed_task_count        INTEGER DEFAULT 0 CHECK (completed_task_count >= 0),
    reward_activity_count       INTEGER DEFAULT 0 CHECK (reward_activity_count >= 0),
    xp_activity_count           INTEGER DEFAULT 0 CHECK (xp_activity_count >= 0),
    streak_activity             VARCHAR(3) DEFAULT 'No' CHECK (streak_activity IN ('Yes', 'No')),
    daily_reward_claimed        VARCHAR(3) DEFAULT 'No' CHECK (daily_reward_claimed IN ('Yes', 'No')),
    mission_activity            VARCHAR(3) DEFAULT 'No' CHECK (mission_activity IN ('Yes', 'No')),
    spin_activity               VARCHAR(3) DEFAULT 'No' CHECK (spin_activity IN ('Yes', 'No')),
    referral_activity           VARCHAR(3) DEFAULT 'No' CHECK (referral_activity IN ('Yes', 'No')),
    wallet_activity             VARCHAR(3) DEFAULT 'No' CHECK (wallet_activity IN ('Yes', 'No')),
    active_flag                 VARCHAR(3) DEFAULT 'No' CHECK (active_flag IN ('Yes', 'No')),
    created_at                  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, activity_date),
    CONSTRAINT fk_daily_activity_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_daily_activity_date ON daily_activity(activity_date);
CREATE INDEX idx_daily_activity_active ON daily_activity(active_flag);

