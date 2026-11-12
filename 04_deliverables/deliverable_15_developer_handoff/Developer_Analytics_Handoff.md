# VELOOP REWARDS — DEVELOPER ANALYTICS HANDOFF SPECIFICATION
**Deliverable ID:** Deliverable 15  
**Work Package:** Work Package N — Developer Analytics Handoff  
**Author:** Data Analyst Intern  
**Organization:** VELOOP Rewards  
**Date:** 2026-11-11  
**Integrity Label:** `SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`  
**Classification:** Confirmed, Proposed, To Be Verified, Simulated  

---

## 1. Executive Summary & Purpose

The **Developer Analytics Handoff** establishes a strict, engineering-grade implementation contract between the Product Analytics team and Software Engineering (Frontend Mobile/Web and Backend Microservices).

In fast-paced product environments, analytics telemetry often fails because event names are informal, payload contracts are undocumented, timestamps lack timezone specifications, and duplicate client retries pollute analytical warehouses.

This document provides:
1. Strict **idempotency, deduplication, and retry standards** for streaming telemetry.
2. Comprehensive, field-level **engineering payload contracts** for all critical product events.
3. Realistic, automated **acceptance test scenarios** that QA and developers must execute prior to production release.

---

## 2. Universal Telemetry Standards & Idempotency Rules

Every event emitted by client applications or internal backend services must adhere to the following non-negotiable protocol:

### 2.1 Event Envelope Structure (Standard JSON Schema)
All events must be serialized into the universal wrapper envelope:
```json
{
  "event_id": "EVT00045812",
  "event_name": "task_completed",
  "timestamp": "2026-11-11T14:32:01.458Z",
  "user_id": "VLUSR000142",
  "session_id": "SESS0001842",
  "client_context": {
    "app_version": "2.4.1",
    "platform": "Android",
    "os_version": "14.0",
    "device_model": "Pixel 8",
    "network_type": "5G"
  },
  "payload": {
    "activity_id": "ACT0004812",
    "task_id": "TASK0042",
    "duration_seconds": 45,
    "reward_amount": 50.00,
    "reward_unit": "XP"
  }
}
```

### 2.2 Idempotency & Deduplication Protocol
* **Client-Side:** When a mobile network interruption causes an HTTP POST failure, the client SDK must retry using the **exact same `event_id`** and `sequence_number`.
* **Ingestion Layer:** The API Gateway / Redis Stream layer maintains an in-memory sliding window cache of all `event_id` keys with a **1-hour Time-to-Live (TTL)**.
* **Deduplication Rule:** If an incoming payload contains an `event_id` already present in the Redis cache, the gateway returns HTTP 200 OK to the client to stop retry loops, but **drops the duplicate record** from publishing to the Kafka / Event Broker topic.
* **Database Level:** Downstream analytical tables enforce a `PRIMARY KEY (event_id)` constraint to guarantee zero duplicate rows.

---

## 3. Engineering Event Specifications & Acceptance Contracts

### Event 1: `user_registered`
* **Requirement ID:** REQ-EVT-001
* **Event Name:** `user_registered`
* **Trigger:** User completes registration form and account record is successfully created in auth database.
* **Priority:** **Critical (P0)**
* **Source:** Authentication Microservice (Server-Side)
* **Timestamp Spec:** ISO-8601 UTC with millisecond precision (`YYYY-MM-DDTHH:MM:SS.sssZ`).
* **Why Needed:** Baseline denominator for all cohort retention, viral conversion, and acquisition CAC calculations.
* **KPI Dependency:** Total Registrations, Acquisition Channel Share, Registration Velocity.
* **Payload Fields:**
  * `user_id` (VARCHAR(16), Required): Valid user identifier (`^VLUSR[0-9]{6}$`).
  * `email_hash` (CHAR(64), Required): SHA-256 hash of email.
  * `registration_source` (VARCHAR(30), Required): Channel (`Organic`, `WhatsApp`, `YouTube`, etc.).
  * `referral_code_used` (VARCHAR(16), Optional): Referral code if referee registered via link.
  * `device` (VARCHAR(20), Required): `Android`, `iOS`, `Desktop Web`, `Mobile Web`.
  * `country` (VARCHAR(50), Required): ISO Country name (`India`).
* **Acceptance Test:**
  * *Given* a new user submitting registration on Android,
  * *When* the user record is committed,
  * *Then* exactly one `user_registered` event is published with non-null `user_id` matching database record, and `email_hash` must be a valid 64-character hexadecimal string without plaintext email exposure.

---

### Event 2: `task_completed`
* **Requirement ID:** REQ-EVT-002
* **Event Name:** `task_completed`
* **Trigger:** Client or third-party partner SDK signals that task activity criteria have been fully satisfied.
* **Priority:** **Critical (P0)**
* **Source:** Client Telemetry SDK / Partner Postback Gateway
* **Timestamp Spec:** ISO-8601 UTC.
* **Why Needed:** Core metric evaluating user engagement, offerwall fulfillment, and triggering reward disbursement.
* **KPI Dependency:** Task Completion Rate, Task Velocity, Revenue eCPM.
* **Payload Fields:**
  * `activity_id` (VARCHAR(16), Required): Unique execution key (`^ACT[0-9]{7}$`).
  * `user_id` (VARCHAR(16), Required): References account holder.
  * `task_id` (VARCHAR(16), Required): References `task_catalog`.
  * `task_category` (VARCHAR(30), Required): `Advertisement`, `App Task`, `Survey`, etc.
  * `duration_seconds` (INTEGER, Required): Elapsed execution time $\ge 1$.
  * `partner_verification_token` (VARCHAR(64), Optional): S2S HMAC signature token.
* **Acceptance Test:**
  * *Given* an active task session initiated at `10:00:00`,
  * *When* the user completes a 30-second rewarded video at `10:00:32`,
  * *Then* emit `task_completed` with `duration_seconds = 32`. If the client submits multiple completion signals for the same `activity_id`, the ingestion engine must deduplicate and commit only the initial event.

---

### Event 3: `reward_credited`
* **Requirement ID:** REQ-EVT-003
* **Event Name:** `reward_credited`
* **Trigger:** Backend Wallet Ledger successfully commits an ACID double-entry balance increment.
* **Priority:** **Critical (P0)**
* **Source:** Wallet Microservice (Server-Side)
* **Timestamp Spec:** ISO-8601 UTC.
* **Why Needed:** Financial audit record of currency issuance; reconciles user wallet balance with platform liabilities.
* **KPI Dependency:** Reward Credit Volume, Average Reward per DAU, Currency Inflation Rate.
* **Payload Fields:**
  * `reward_id` (VARCHAR(16), Required): Unique disbursement key (`^RWD[0-9]{7}$`).
  * `transaction_id` (VARCHAR(16), Required): References committed `wallet_transactions` row.
  * `activity_id` (VARCHAR(16), Optional): Nullable for daily check-in / spin rewards.
  * `user_id` (VARCHAR(16), Required): Recipient user ID.
  * `reward_amount` (DECIMAL(12,2), Required): Non-zero positive amount.
  * `reward_unit` (VARCHAR(10), Required): Enum (`XP`, `GEMS`, `TOKENS`, `INR`).
  * `reward_source` (VARCHAR(30), Required): `Task`, `Daily Check-In`, `Spin Wheel`, `Mining`.
* **Acceptance Test:**
  * *Given* a validated task completion event,
  * *When* the Wallet service processes payout,
  * *Then* emit `reward_credited` only after the database transaction successfully commits. `reward_amount` must match `task_catalog.base_reward_amount`.

---

### Event 4: `withdrawal_requested`
* **Requirement ID:** REQ-EVT-004
* **Event Name:** `withdrawal_requested`
* **Trigger:** User submits payout request form and balance is placed in escrow freeze.
* **Priority:** **Critical (P0)**
* **Source:** Withdrawal Microservice (Server-Side)
* **Timestamp Spec:** ISO-8601 UTC.
* **Why Needed:** Initiates payout pipeline SLA tracking; locks funds to prevent double-spending.
* **KPI Dependency:** Withdrawal Requests Volume, Pending Queue Depth, Requested Payout Volume.
* **Payload Fields:**
  * `withdrawal_id` (VARCHAR(16), Required): Payout identifier (`^WDL[0-9]{7}$`).
  * `user_id` (VARCHAR(16), Required): Account holder.
  * `requested_amount` (DECIMAL(10,2), Required): Fiat value $\ge 10.00$.
  * `payout_method` (VARCHAR(20), Required): `UPI`, `Paytm`, `Bank Transfer`, `PayPal`.
  * `destination_hash` (CHAR(64), Required): Cryptographic hash of payment address.
* **Acceptance Test:**
  * *Given* a user with available balance of 500 XP,
  * *When* user submits withdrawal of 200 INR (redeeming 400 XP),
  * *Then* emit `withdrawal_requested` and immediately decrement available balance by 400 XP while moving it to frozen escrow balance.

---

### Event 5: `withdrawal_completed`
* **Requirement ID:** REQ-EVT-005
* **Event Name:** `withdrawal_completed`
* **Trigger:** Payment gateway webhook confirms successful bank settlement.
* **Priority:** **Critical (P0)**
* **Source:** Payment Gateway Webhook Worker (Server-Side)
* **Timestamp Spec:** ISO-8601 UTC.
* **Why Needed:** Confirms cash delivery; terminates payout SLA timer; finalizes platform cash outflow.
* **KPI Dependency:** Completed Withdrawals, Payout Latency (Hours), Disbursed Cash Volume.
* **Payload Fields:**
  * `withdrawal_id` (VARCHAR(16), Required): References pending payout record.
  * `gateway_name` (VARCHAR(50), Required): Gateway provider (`Cashfree`, `Razorpay`, `PayPal`).
  * `gateway_txn_id` (VARCHAR(64), Required): External bank clearing reference.
  * `latency_hours` (DECIMAL(6,2), Required): Elapsed hours from request.
* **Acceptance Test:**
  * *Given* an active payout batch in `Processing` state,
  * *When* gateway returns HTTP 200 settlement webhook,
  * *Then* update withdrawal status to `Completed` and emit `withdrawal_completed` with non-null `gateway_txn_id`.

