# VELOOP REWARDS — LOGICAL DATA MODEL & ER DIAGRAM SPECIFICATION
**Deliverable ID:** Deliverable 10  
**Work Package:** Work Package H — Logical Data Model & ER Diagram  
**Author:** Data Analyst Intern  
**Organization:** VELOOP Rewards  
**Date:** 2026-11-11  
**Integrity Label:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
**Classification:** Confirmed, Proposed, To Be Verified, Simulated  

---

## 1. Executive Summary & Architectural Overview

The VELOOP Rewards platform requires a high-performance, normalized relational data model capable of supporting both high-throughput write operations (telemetry event ingestion, reward crediting) and analytical reporting (cohort retention, financial reconciliation, multi-touch attribution).

To prevent data silos and inconsistencies, the model is architected across four functional clusters:
1. **User Identity & Lifecycle Cluster:** `users`, `sessions`, `daily_activity`.
2. **Behavioral Telemetry Cluster:** `feature_events`, `task_catalog`, `task_activity`.
3. **Financial Accounting Cluster:** `wallet_transactions`, `rewards_ledger`, `withdrawals`.
4. **Growth & Virality Cluster:** `referrals`.

The complete schema is written in PostgreSQL 15+ compatible DDL and saved at [`04_deliverables/deliverable_10_logical_data_model/schema.sql`](file:///d:/Veloop%20data%20Analysis/04_deliverables/deliverable_10_logical_data_model/schema.sql).

---

## 2. Professional Entity-Relationship (ER) Diagram

```mermaid
erDiagram
    users ||--o{ sessions : "initiates (1:N)"
    users ||--o{ feature_events : "emits (1:N)"
    users ||--o{ task_activity : "executes (1:N)"
    users ||--o{ rewards_ledger : "earns (1:N)"
    users ||--o{ wallet_transactions : "owns (1:N)"
    users ||--o{ withdrawals : "requests (1:N)"
    users ||--o{ referrals : "refers (1:N as referrer)"
    users ||--o| referrals : "acquired_by (1:1 as referee)"
    users ||--o{ daily_activity : "aggregates (1:N)"

    sessions ||--o{ feature_events : "contains (1:N)"
    sessions ||--o{ task_activity : "frames (1:N)"

    task_catalog ||--o{ task_activity : "instantiates (1:N)"
    task_activity ||--o| rewards_ledger : "triggers (1:1)"

    rewards_ledger ||--|| wallet_transactions : "posts_to (1:1)"
    wallet_transactions ||--o| wallet_transactions : "reverses (1:1 self-ref)"
    withdrawals ||--|| wallet_transactions : "holds_or_settles (1:1)"

    users {
        VARCHAR_16 user_id PK
        CHAR_64 email_hash
        VARCHAR_20 account_status
        TIMESTAMP account_created_at
        VARCHAR_16 referral_code
        INTEGER xp_balance
        DECIMAL token_balance
    }

    sessions {
        VARCHAR_16 session_id PK
        VARCHAR_16 user_id FK
        TIMESTAMP session_start
        TIMESTAMP session_end
        INTEGER session_duration_seconds
        VARCHAR_20 device
        VARCHAR_50 entry_point
    }

    feature_events {
        VARCHAR_16 event_id PK
        VARCHAR_16 session_id FK
        VARCHAR_16 user_id FK
        TIMESTAMP event_datetime
        VARCHAR_50 feature_name
        VARCHAR_50 event_name
        VARCHAR_20 event_status
        JSONB payload_json
    }

    task_catalog {
        VARCHAR_16 task_id PK
        VARCHAR_100 task_name
        VARCHAR_30 task_category
        DECIMAL base_reward_amount
        VARCHAR_10 reward_unit
        BOOLEAN is_active
    }

    task_activity {
        VARCHAR_16 activity_id PK
        VARCHAR_16 user_id FK
        VARCHAR_16 task_id FK
        VARCHAR_16 session_id FK
        TIMESTAMP task_started_at
        TIMESTAMP task_completed_at
        VARCHAR_20 task_status
        VARCHAR_50 failure_reason
        VARCHAR_20 reward_status
    }

    rewards_ledger {
        VARCHAR_16 reward_id PK
        VARCHAR_16 activity_id FK
        VARCHAR_16 user_id FK
        DECIMAL reward_amount
        VARCHAR_10 reward_unit
        VARCHAR_20 disbursement_status
        VARCHAR_16 transaction_id FK
        TIMESTAMP credited_at
    }

    wallet_transactions {
        VARCHAR_16 transaction_id PK
        VARCHAR_16 user_id FK
        TIMESTAMP timestamp
        VARCHAR_25 transaction_type
        DECIMAL amount
        VARCHAR_10 unit
        VARCHAR_15 status
        VARCHAR_32 reference_id
        VARCHAR_16 reversal_transaction_id FK
    }

    withdrawals {
        VARCHAR_16 withdrawal_id PK
        VARCHAR_16 user_id FK
        DECIMAL requested_amount
        VARCHAR_20 payout_method
        CHAR_64 destination_hash
        TIMESTAMP requested_timestamp
        TIMESTAMP final_timestamp
        VARCHAR_20 status
        VARCHAR_50 rejection_reason
    }

    referrals {
        VARCHAR_16 referral_id PK
        VARCHAR_16 referring_user_id FK
        VARCHAR_16 referred_user_id FK "UNIQUE"
        TIMESTAMP registration_timestamp
        TIMESTAMP activation_timestamp
        VARCHAR_20 referral_status
        DECIMAL commission_amount
    }

    daily_activity {
        VARCHAR_16 user_id PK_FK
        DATE activity_date PK
        INTEGER session_count
        INTEGER completed_task_count
        VARCHAR_3 active_flag
    }
```

---

## 3. Primary Key & Relational Integrity Specifications (H1 & H2)

### 3.1 Primary Keys Summary
* `users.user_id`: Immutable alphanumeric identifier format `^VLUSR[0-9]{6}$`.
* `sessions.session_id`: Alphanumeric format `^SESS[0-9]{7}$`.
* `feature_events.event_id`: High-volume format `^EVT[0-9]{8}$`.
* `task_catalog.task_id`: Catalog identifier format `^TASK[0-9]{4}$`.
* `task_activity.activity_id`: Execution instance format `^ACT[0-9]{7}$`.
* `rewards_ledger.reward_id`: Disbursement key format `^RWD[0-9]{7}$`.
* `wallet_transactions.transaction_id`: Ledger key format `^TXN[0-9]{8}$`.
* `withdrawals.withdrawal_id`: Payout key format `^WDL[0-9]{7}$`.
* `referrals.referral_id`: Attribution key format `^REF[0-9]{8}$`.
* `daily_activity.(user_id, activity_date)`: Composite primary key.

### 3.2 Foreign Key Cascading & Deletion Policies
1. **User Cascades:** Deleting a user (`ON DELETE CASCADE`) cascades to `sessions`, `feature_events`, `task_activity`, and `daily_activity`.
2. **Financial Protection (`ON DELETE RESTRICT`):** The entities `wallet_transactions`, `withdrawals`, and `task_catalog` strictly enforce `ON DELETE RESTRICT`. A user record cannot be hard-deleted if financial transactions or payout records exist in the ledger. This guarantees audit compliance with financial accounting standards.
3. **Nullable Activity Links (`ON DELETE SET NULL`):** If a `task_activity` record is pruned in operational maintenance, the `rewards_ledger.activity_id` is set to NULL, preserving the immutable financial ledger entry intact.

---

## 4. Cardinality & Relationship Documentation (H3)

### 4.1 One-to-Many Relationships (1:N)
* **`users` $\rightarrow$ `sessions` (1:N):** One registered user initiates multiple contiguous application visits across different devices and dates.
* **`users` $\rightarrow$ `task_activity` (1:N):** A user executes multiple earning tasks over their tenure.
* **`users` $\rightarrow$ `wallet_transactions` (1:N):** A user balance is mutated across numerous distinct earning credits, redemptions, and fee adjustments.
* **`users` $\rightarrow$ `withdrawals` (1:N):** A user submits multiple payout requests as they accumulate redeemable balances.
* **`sessions` $\rightarrow$ `feature_events` (1:N):** A single 5-minute user session emits dozens of discrete interaction events (views, clicks, taps, claims).

### 4.2 One-to-One Relationships (1:1)
* **`users` $\rightarrow$ `referrals` (as referee) (1:1):** A user can only be referred into the platform **once**. Enforced by a unique constraint on `referrals.referred_user_id`.
* **`task_activity` $\rightarrow$ `rewards_ledger` (1:1):** Each completed task activity record can generate at most one disbursement credit record in `rewards_ledger`.
* **`rewards_ledger` $\rightarrow$ `wallet_transactions` (1:1):** Every individual reward disbursement record corresponds to exactly one committed double-entry credit record in the financial transaction ledger.

### 4.3 Many-to-Many Relationships (N:M)
* **`users` $\longleftrightarrow$ `task_catalog` (N:M):** Users engage with many tasks, and tasks are executed by thousands of users. This relationship is fully resolved by the associative junction table `task_activity`.

### 4.4 Self-Referencing Recursive Relationships
* **`wallet_transactions.reversal_transaction_id` $\rightarrow$ `wallet_transactions.transaction_id`:** When a prior credit is clawed back for fraud, a new offsetting transaction record is created that directly points to the historical transaction being reversed. This provides a clean, tamper-evident audit trail without overwriting historical database records.
* **`users.referring_user_id` $\rightarrow$ `users.user_id`:** Self-referencing foreign key on the `users` table allowing direct recursive traversal of multi-tier referral trees.

