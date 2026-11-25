# VELOOP REWARDS — PRODUCTION EVENT TRACKING PLAN
**Deliverable 08 | Work Package F**  
**Engineering Specification: 32 Standardized Production Telemetry Events**  
**Integrity Policy:** SIMULATED DATA — CREATED FOR ANALYTICAL TESTING  

---

## 1. Executive Overview & Tracking Governance

This Event Tracking Plan defines the enterprise telemetry taxonomy for **VELOOP Rewards**. It covers 32 standardized events across six core functional domains:
1. **Account & Identity:** User lifecycle, onboarding, and authentication.
2. **Task Execution:** Micro-task funnel (viewed, started, completed, failed).
3. **Rewards & Incentives:** XP soft currency disbursement and verification lifecycle.
4. **Engagement & Gamification:** Streaks, daily check-ins, missions, spin wheel, badges.
5. **Referral & Virality:** Link creation, invite dispatch, referee attribution, and activation.
6. **Wallet & Financial Withdrawals:** Double-entry ledger balance movements and fiat payout pipeline.

Every event specification provides the complete **16 required engineering attributes**:
1. Event Name
2. Business Purpose
3. Trigger Condition
4. Required Properties
5. Optional Properties
6. User Identifier Requirements
7. Session Identifier Requirements
8. Timestamp Format
9. JSON Payload Example
10. JSON Schema Definition
11. Field Data Types
12. Allowed Values
13. Validation Rules
14. Negative Test Cases
15. Acceptance Criteria
16. Acceptance Test Method

---

## 2. Event Taxonomy Summary Matrix

| # | Event Name | Functional Domain | Implementation Status | User ID Req | Trigger Summary |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | `user_registered` | Account | **Observed in Clean Users** | Mandatory (e.g. VLUSR000001) | User successfully completes the registration flow. |
| 2 | `user_logged_in` | Account | **Observed in Sessions** | Mandatory | User submits valid credentials and JWT auth token is issued. |
| 3 | `user_logged_out` | Account | **Proposed Future Spec** | Mandatory | User taps logout button or inactivity timeout threshold triggers. |
| 4 | `onboarding_started` | Account | **Proposed Future Spec** | Mandatory | First app launch after successful registration. |
| 5 | `onboarding_completed` | Account | **Proposed Future Spec** | Mandatory | User completes final onboarding walkthrough step. |
| 6 | `task_viewed` | Tasks | **Observed in Task Activity** | Mandatory | Task card becomes visible on user device viewport. |
| 7 | `task_opened` | Tasks | **Proposed Future Spec** | Mandatory | User taps task card to inspect details and requirements. |
| 8 | `task_started` | Tasks | **Observed in Task Activity** | Mandatory | User taps 'Start Task' or enters execution screen. |
| 9 | `task_completed` | Tasks | **Observed in Task Activity** | Mandatory | User finishes all task requirements or verification callback confirms. |
| 10 | `task_failed` | Tasks | **Observed in Task Activity** | Mandatory | Timeout, user exit, or verification failure. |
| 11 | `reward_credited` | Rewards | **Observed in Task Activity** | Mandatory | PostgreSQL transaction successfully increments user xp_balance. |
| 12 | `reward_pending` | Rewards | **Observed in Task Activity** | Mandatory | Task completed awaiting partner server-to-server callback. |
| 13 | `reward_reversed` | Rewards | **Proposed Future Spec** | Mandatory | Security audit or fraud detection flag confirms abuse. |
| 14 | `daily_reward_claimed` | Rewards | **Observed in Feature Events** | Mandatory | User taps 'Claim Daily Reward' on check-in screen. |
| 15 | `streak_updated` | Engagement | **Observed in Feature Events** | Mandatory | Automated daily midnight batch evaluation or check-in claim. |
| 16 | `mission_started` | Missions | **Observed in Feature Events** | Mandatory | User accepts or initiates a daily or weekly mission. |
| 17 | `mission_completed` | Missions | **Observed in Milestones** | Mandatory | All criteria of an active mission are satisfied. |
| 18 | `badge_earned` | Gamification | **Observed in Feature Events** | Mandatory | Achievement condition satisfied (e.g., 50 tasks completed). |
| 19 | `spin_started` | Gamification | **Observed in Feature Events** | Mandatory | User taps 'Spin Now' button on wheel screen. |
| 20 | `spin_completed` | Gamification | **Observed in Feature Events** | Mandatory | Wheel stops on winning wedge. |
| 21 | `referral_created` | Referral | **Observed in Feature Events** | Mandatory | User opens referral tab and generates unique sharing link. |
| 22 | `referral_registered` | Referral | **Proposed Future Spec** | Mandatory (both referrer and referee) | Referee completes registration using referrer's invite code. |
| 23 | `referral_activated` | Referral | **Proposed Future Spec** | Mandatory | Referee completes first task, check-in, or session. |
| 24 | `referral_converted` | Referral | **Proposed Future Spec** | Mandatory | Activation verified and anti-fraud checks pass. |
| 25 | `wallet_transaction_created` | Wallet | **Proposed Future Spec** | Mandatory | User or system queues balance adjustment (earning or payout). |
| 26 | `wallet_transaction_completed` | Wallet | **Proposed Future Spec** | Mandatory | PostgreSQL COMMIT executes with zero Net Debit/Credit imbalance. |
| 27 | `wallet_transaction_reversed` | Wallet | **Proposed Future Spec** | Mandatory | Transaction rollback or manual administrative void. |
| 28 | `withdrawal_requested` | Withdrawals | **Proposed Future Spec** | Mandatory | User taps 'Confirm Withdrawal' after selecting payout rail. |
| 29 | `withdrawal_processing` | Withdrawals | **Proposed Future Spec** | Mandatory | Automated payout engine picks up requested withdrawal. |
| 30 | `withdrawal_completed` | Withdrawals | **Proposed Future Spec** | Mandatory | Bank / UPI webhook confirms successful beneficiary settlement. |
| 31 | `withdrawal_rejected` | Withdrawals | **Proposed Future Spec** | Mandatory | Beneficiary bank rejects transfer (e.g., invalid UPI ID / Account closed). |
| 32 | `withdrawal_reversed` | Withdrawals | **Proposed Future Spec** | Mandatory | Payment rail issues chargeback or reversal notice post-settlement. |

---

## 3. Detailed Engineering Event Specifications

### Event 01: `user_registered`
* **Functional Domain:** Account
* **Implementation Status:** `Observed in Clean Users`
* **Business Purpose:** Capture new user account creation and attribution origin.
* **Trigger Condition:** User successfully completes the registration flow.
* **Required Properties:** `user_id, email, registration_datetime, acquisition_source, platform, country`
* **Optional Properties:** `referral_source_detail, marketing_opt_in, account_created_via`
* **User Identifier Requirement:** Mandatory (e.g. VLUSR000001)
* **Session Identifier Requirement:** Optional on first signup
* **Timestamp Format:** `ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)`
* **Field Data Types:** `user_id: string, email: string, registration_datetime: timestamptz, acquisition_source: string, platform: string, country: char(2)`
* **Allowed Values & Constraints:** `platform in ('Android', 'iOS', 'Web', 'Windows', 'macOS'); country in ('IN', 'US', etc.)`
* **Validation Rules:** Email must conform to RFC 5322; Age must be >= 18; user_id must be unique.
* **Negative Test Cases:** Null email; duplicate user_id; age < 18; malformed timestamp format.
* **Acceptance Criteria:** Event emitted within 500ms of user commitment to PostgreSQL users table.
* **Acceptance Test Method:** `POST /api/v1/events/user_registered with valid payload returns HTTP 201.`

#### JSON Payload Example
```json
{
  "event_name": "user_registered",
  "user_id": "VLUSR000101",
  "email": "user101@example.com",
  "registration_datetime": "2026-03-15T10:14:00Z",
  "acquisition_source": "Organic Search",
  "platform": "Android",
  "country": "IN",
  "marketing_opt_in": true
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "user_id",
    "email",
    "registration_datetime",
    "acquisition_source",
    "platform",
    "country"
  ],
  "properties": {
    "event_name": {
      "type": "string",
      "enum": [
        "user_registered"
      ]
    },
    "user_id": {
      "type": "string",
      "pattern": "^VLUSR[0-9]{6}$"
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "registration_datetime": {
      "type": "string",
      "format": "date-time"
    },
    "acquisition_source": {
      "type": "string"
    },
    "platform": {
      "type": "string",
      "enum": [
        "Android",
        "iOS",
        "Web",
        "Windows",
        "macOS"
      ]
    },
    "country": {
      "type": "string",
      "minLength": 2,
      "maxLength": 2
    }
  }
}
```

---
### Event 02: `user_logged_in`
* **Functional Domain:** Account
* **Implementation Status:** `Observed in Sessions`
* **Business Purpose:** Track session initiation and user authentication frequency.
* **Trigger Condition:** User submits valid credentials and JWT auth token is issued.
* **Required Properties:** `user_id, session_id, timestamp, device, platform`
* **Optional Properties:** `ip_hash, app_version`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Mandatory (links session start)
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `user_id: string, session_id: string, timestamp: timestamptz, device: string`
* **Allowed Values & Constraints:** `device in ('Android', 'Windows', 'iOS', 'macOS')`
* **Validation Rules:** session_id must match active session table; timestamp must be <= CURRENT_TIMESTAMP.
* **Negative Test Cases:** Expired session token; future login timestamp; unregistered user_id.
* **Acceptance Criteria:** Increments daily session_count for user in veloop.daily_activity.
* **Acceptance Test Method:** `Successful auth endpoint triggers event log with valid session_id.`

#### JSON Payload Example
```json
{
  "event_name": "user_logged_in",
  "user_id": "VLUSR000101",
  "session_id": "SESS000214",
  "timestamp": "2026-03-15T10:15:00Z",
  "device": "Android",
  "platform": "Mobile"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "user_id",
    "session_id",
    "timestamp",
    "device",
    "platform"
  ],
  "properties": {
    "event_name": {
      "type": "string",
      "enum": [
        "user_logged_in"
      ]
    },
    "user_id": {
      "type": "string"
    },
    "session_id": {
      "type": "string"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

---
### Event 03: `user_logged_out`
* **Functional Domain:** Account
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Track session closure and measure session duration accurately.
* **Trigger Condition:** User taps logout button or inactivity timeout threshold triggers.
* **Required Properties:** `user_id, session_id, timestamp, logout_reason`
* **Optional Properties:** `session_duration_seconds`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Mandatory
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `user_id: string, session_id: string, timestamp: timestamptz, logout_reason: string`
* **Allowed Values & Constraints:** `logout_reason in ('User_Action', 'Timeout', 'Revoked')`
* **Validation Rules:** timestamp must be greater than session_start.
* **Negative Test Cases:** Logout timestamp earlier than session_start; non-existent session_id.
* **Acceptance Criteria:** Updates veloop.sessions session_end timestamp and calculates duration.
* **Acceptance Test Method:** `POST logout endpoint commits session_end and emits user_logged_out.`

#### JSON Payload Example
```json
{
  "event_name": "user_logged_out",
  "user_id": "VLUSR000101",
  "session_id": "SESS000214",
  "timestamp": "2026-03-15T10:35:00Z",
  "logout_reason": "User_Action"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "user_id",
    "session_id",
    "timestamp",
    "logout_reason"
  ],
  "properties": {
    "logout_reason": {
      "type": "string",
      "enum": [
        "User_Action",
        "Timeout",
        "Revoked"
      ]
    }
  }
}
```

---
### Event 04: `onboarding_started`
* **Functional Domain:** Account
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Monitor the beginning of the interactive user onboarding tour.
* **Trigger Condition:** First app launch after successful registration.
* **Required Properties:** `user_id, session_id, timestamp, step_number`
* **Optional Properties:** `tour_version`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Mandatory
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `user_id: string, session_id: string, step_number: int`
* **Allowed Values & Constraints:** `step_number >= 1`
* **Validation Rules:** Emitted only once per user_id lifetime.
* **Negative Test Cases:** Emitting with step_number <= 0; emitting without active session.
* **Acceptance Criteria:** Flag onboarding_status set to 'Incomplete' in user table.
* **Acceptance Test Method:** `New user tour load dispatches event.`

#### JSON Payload Example
```json
{
  "event_name": "onboarding_started",
  "user_id": "VLUSR000101",
  "session_id": "SESS000214",
  "timestamp": "2026-03-15T10:15:30Z",
  "step_number": 1
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "user_id",
    "session_id",
    "step_number"
  ]
}
```

---
### Event 05: `onboarding_completed`
* **Functional Domain:** Account
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Measure onboarding funnel completion velocity and drop-off.
* **Trigger Condition:** User completes final onboarding walkthrough step.
* **Required Properties:** `user_id, session_id, timestamp, total_steps_completed, duration_seconds`
* **Optional Properties:** `reward_granted`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Mandatory
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `user_id: string, total_steps_completed: int, duration_seconds: int`
* **Allowed Values & Constraints:** `total_steps_completed >= 1; duration_seconds > 0`
* **Validation Rules:** User must have existing onboarding_started event.
* **Negative Test Cases:** Duration negative; user already completed onboarding.
* **Acceptance Criteria:** Updates onboarding_status to 'Completed' in users table.
* **Acceptance Test Method:** `Completing tour triggers status update and event emission.`

#### JSON Payload Example
```json
{
  "event_name": "onboarding_completed",
  "user_id": "VLUSR000101",
  "session_id": "SESS000214",
  "timestamp": "2026-03-15T10:18:00Z",
  "total_steps_completed": 5,
  "duration_seconds": 150
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "user_id",
    "session_id",
    "total_steps_completed"
  ]
}
```

---
### Event 06: `task_viewed`
* **Functional Domain:** Tasks
* **Implementation Status:** `Observed in Task Activity`
* **Business Purpose:** Track task catalog impressions and user offer discovery.
* **Trigger Condition:** Task card becomes visible on user device viewport.
* **Required Properties:** `activity_id, user_id, task_id, task_category, timestamp`
* **Optional Properties:** `device, session_id`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `activity_id: string, user_id: string, task_id: string, task_category: string`
* **Allowed Values & Constraints:** `task_category in ('Watch Ads', 'Mining Rewards', 'Daily Check-in', 'Missions', 'Tap & Earn', 'Spin the Wheel')`
* **Validation Rules:** activity_id must be unique.
* **Negative Test Cases:** Missing task_id; invalid category string.
* **Acceptance Criteria:** Logged in veloop.task_activity as Viewed.
* **Acceptance Test Method:** `Viewport card intersection triggers event.`

#### JSON Payload Example
```json
{
  "event_name": "task_viewed",
  "activity_id": "ACT000001",
  "user_id": "VLUSR000001",
  "task_id": "TSK0012",
  "task_category": "Watch Ads",
  "timestamp": "2026-03-15T11:00:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "activity_id",
    "user_id",
    "task_id",
    "task_category",
    "timestamp"
  ]
}
```

---
### Event 07: `task_opened`
* **Functional Domain:** Tasks
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Track user click-through into detailed task instructions.
* **Trigger Condition:** User taps task card to inspect details and requirements.
* **Required Properties:** `activity_id, user_id, task_id, timestamp`
* **Optional Properties:** `session_id, estimated_payout_xp`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Mandatory
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `activity_id: string, user_id: string, task_id: string`
* **Allowed Values & Constraints:** `task_id must exist in catalog`
* **Validation Rules:** Requires preceding task_viewed event.
* **Negative Test Cases:** Opening inactive or expired task.
* **Acceptance Criteria:** Tracks intermediate engagement in micro-task funnel.
* **Acceptance Test Method:** `Card tap emits event.`

#### JSON Payload Example
```json
{
  "event_name": "task_opened",
  "activity_id": "ACT000001",
  "user_id": "VLUSR000001",
  "task_id": "TSK0012",
  "timestamp": "2026-03-15T11:00:15Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "activity_id",
    "user_id",
    "task_id"
  ]
}
```

---
### Event 08: `task_started`
* **Functional Domain:** Tasks
* **Implementation Status:** `Observed in Task Activity`
* **Business Purpose:** Record task initiation and start time for duration tracking.
* **Trigger Condition:** User taps 'Start Task' or enters execution screen.
* **Required Properties:** `activity_id, user_id, task_id, timestamp`
* **Optional Properties:** `session_id`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `activity_id: string, user_id: string, task_id: string, timestamp: timestamptz`
* **Allowed Values & Constraints:** `valid task_id`
* **Validation Rules:** task_started_at must be >= task_viewed_at.
* **Negative Test Cases:** Starting task with task_started_at < task_viewed_at.
* **Acceptance Criteria:** Updates task_status in task_activity to Started.
* **Acceptance Test Method:** `Action click dispatches event and updates DB.`

#### JSON Payload Example
```json
{
  "event_name": "task_started",
  "activity_id": "ACT000001",
  "user_id": "VLUSR000001",
  "task_id": "TSK0012",
  "timestamp": "2026-03-15T11:00:30Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "activity_id",
    "user_id",
    "task_id",
    "timestamp"
  ]
}
```

---
### Event 09: `task_completed`
* **Functional Domain:** Tasks
* **Implementation Status:** `Observed in Task Activity`
* **Business Purpose:** Verify task completion and trigger reward eligibility.
* **Trigger Condition:** User finishes all task requirements or verification callback confirms.
* **Required Properties:** `activity_id, user_id, task_id, timestamp, duration_seconds`
* **Optional Properties:** `partner_callback_status`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `activity_id: string, user_id: string, task_id: string, duration_seconds: int`
* **Allowed Values & Constraints:** `duration_seconds >= 1`
* **Validation Rules:** task_completed_at must be >= task_started_at.
* **Negative Test Cases:** Duration negative; task not started.
* **Acceptance Criteria:** Updates task_status to 'Completed' in task_activity.
* **Acceptance Test Method:** `Task completion callback commits record and emits event.`

#### JSON Payload Example
```json
{
  "event_name": "task_completed",
  "activity_id": "ACT000001",
  "user_id": "VLUSR000001",
  "task_id": "TSK0012",
  "timestamp": "2026-03-15T11:02:00Z",
  "duration_seconds": 90
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "activity_id",
    "user_id",
    "task_id",
    "duration_seconds"
  ]
}
```

---
### Event 10: `task_failed`
* **Functional Domain:** Tasks
* **Implementation Status:** `Observed in Task Activity`
* **Business Purpose:** Record micro-task failures, partner rejection, or abandonment.
* **Trigger Condition:** Timeout, user exit, or verification failure.
* **Required Properties:** `activity_id, user_id, task_id, failure_reason, timestamp`
* **Optional Properties:** `retry_allowed`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `activity_id: string, user_id: string, failure_reason: string`
* **Allowed Values & Constraints:** `failure_reason in ('Timeout_Expired', 'User_Abandoned', 'Partner_Rejected', 'Captcha_Failed')`
* **Validation Rules:** Cannot mark task failed after successful reward crediting.
* **Negative Test Cases:** Empty failure reason; invalid activity ID.
* **Acceptance Criteria:** Updates task_status to Failed in task_activity.
* **Acceptance Test Method:** `Abandonment trigger records failure.`

#### JSON Payload Example
```json
{
  "event_name": "task_failed",
  "activity_id": "ACT000002",
  "user_id": "VLUSR000002",
  "task_id": "TSK0015",
  "failure_reason": "Timeout_Expired",
  "timestamp": "2026-03-15T11:05:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "activity_id",
    "user_id",
    "task_id",
    "failure_reason"
  ]
}
```

---
### Event 11: `reward_credited`
* **Functional Domain:** Rewards
* **Implementation Status:** `Observed in Task Activity`
* **Business Purpose:** Record soft currency (XP) credit to user account balance.
* **Trigger Condition:** PostgreSQL transaction successfully increments user xp_balance.
* **Required Properties:** `reward_id, user_id, reward_type, amount, source_feature, timestamp`
* **Optional Properties:** `task_activity_id`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `reward_id: string, user_id: string, reward_type: string, amount: int`
* **Allowed Values & Constraints:** `reward_type in ('XP', 'GEMS', 'TOKENS'); amount > 0`
* **Validation Rules:** amount must be strictly positive; user_id must exist in users table.
* **Negative Test Cases:** amount <= 0; unknown user_id.
* **Acceptance Criteria:** Increments user xp_balance and records reward_status as 'Credited'.
* **Acceptance Test Method:** `Reward credit commits atomic balance update.`

#### JSON Payload Example
```json
{
  "event_name": "reward_credited",
  "reward_id": "RWD000100",
  "user_id": "VLUSR000001",
  "reward_type": "XP",
  "amount": 50,
  "source_feature": "Watch Ads",
  "timestamp": "2026-03-15T11:02:01Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "reward_id",
    "user_id",
    "reward_type",
    "amount",
    "source_feature"
  ]
}
```

---
### Event 12: `reward_pending`
* **Functional Domain:** Rewards
* **Implementation Status:** `Observed in Task Activity`
* **Business Purpose:** Log reward transactions requiring asynchronous partner verification.
* **Trigger Condition:** Task completed awaiting partner server-to-server callback.
* **Required Properties:** `activity_id, user_id, task_id, timestamp`
* **Optional Properties:** `callback_timeout_seconds`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `activity_id: string, user_id: string, task_id: string`
* **Allowed Values & Constraints:** `valid task_id`
* **Validation Rules:** reward_status set to Pending.
* **Negative Test Cases:** Missing activity_id.
* **Acceptance Criteria:** Queues task in audit verification pipeline.
* **Acceptance Test Method:** `Pending callback status logs event.`

#### JSON Payload Example
```json
{
  "event_name": "reward_pending",
  "activity_id": "ACT000005",
  "user_id": "VLUSR000005",
  "task_id": "TSK0020",
  "timestamp": "2026-03-15T11:10:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "activity_id",
    "user_id",
    "task_id"
  ]
}
```

---
### Event 13: `reward_reversed`
* **Functional Domain:** Rewards
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Record revocation of fraudulently credited points or partner chargebacks.
* **Trigger Condition:** Security audit or fraud detection flag confirms abuse.
* **Required Properties:** `reward_id, user_id, amount, reversal_reason, timestamp`
* **Optional Properties:** `audit_ticket_id`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `reward_id: string, user_id: string, amount: int, reversal_reason: string`
* **Allowed Values & Constraints:** `reversal_reason in ('Bot_Activity_Detected', 'Duplicate_IP', 'Partner_Chargeback')`
* **Validation Rules:** User balance must not drop below zero.
* **Negative Test Cases:** amount negative; reversing already reversed reward.
* **Acceptance Criteria:** Emits debit entry in ledger and adjusts user balance.
* **Acceptance Test Method:** `Fraud revocation triggers reversal event.`

#### JSON Payload Example
```json
{
  "event_name": "reward_reversed",
  "reward_id": "RWD000100",
  "user_id": "VLUSR000001",
  "amount": 50,
  "reversal_reason": "Bot_Activity_Detected",
  "timestamp": "2026-03-15T12:00:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "reward_id",
    "user_id",
    "amount",
    "reversal_reason"
  ]
}
```

---
### Event 14: `daily_reward_claimed`
* **Functional Domain:** Rewards
* **Implementation Status:** `Observed in Feature Events`
* **Business Purpose:** Track daily engagement check-in claims and retention cadence.
* **Trigger Condition:** User taps 'Claim Daily Reward' on check-in screen.
* **Required Properties:** `event_id, user_id, day_number, xp_reward, timestamp`
* **Optional Properties:** `session_id, streak_bonus`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `event_id: string, user_id: string, day_number: int, xp_reward: int`
* **Allowed Values & Constraints:** `day_number between 1 and 7; xp_reward > 0`
* **Validation Rules:** Allowed only once per calendar day per user_id.
* **Negative Test Cases:** Claiming twice on same calendar date.
* **Acceptance Criteria:** Sets daily_reward_claimed = 'Yes' in daily_activity.
* **Acceptance Test Method:** `Claim button triggers credit and daily lock.`

#### JSON Payload Example
```json
{
  "event_name": "daily_reward_claimed",
  "event_id": "EVT000010",
  "user_id": "VLUSR000010",
  "day_number": 3,
  "xp_reward": 15,
  "timestamp": "2026-03-15T09:00:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "event_id",
    "user_id",
    "day_number",
    "xp_reward"
  ]
}
```

---
### Event 15: `streak_updated`
* **Functional Domain:** Engagement
* **Implementation Status:** `Observed in Feature Events`
* **Business Purpose:** Track consecutive active day streak progression and breakage.
* **Trigger Condition:** Automated daily midnight batch evaluation or check-in claim.
* **Required Properties:** `user_id, current_streak, previous_streak, status, timestamp`
* **Optional Properties:** `streak_broken_flag`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `user_id: string, current_streak: int, status: string`
* **Allowed Values & Constraints:** `status in ('Maintained', 'Broken', 'Reset'); current_streak >= 0`
* **Validation Rules:** current_streak must equal previous_streak + 1 when Maintained.
* **Negative Test Cases:** Negative streak value; missing status.
* **Acceptance Criteria:** Updates daily_streak in veloop.users.
* **Acceptance Test Method:** `Streak calculation commits to database.`

#### JSON Payload Example
```json
{
  "event_name": "streak_updated",
  "user_id": "VLUSR000010",
  "current_streak": 4,
  "previous_streak": 3,
  "status": "Maintained",
  "timestamp": "2026-03-15T09:00:01Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "user_id",
    "current_streak",
    "status"
  ]
}
```

---
### Event 16: `mission_started`
* **Functional Domain:** Missions
* **Implementation Status:** `Observed in Feature Events`
* **Business Purpose:** Track engagement with multi-step structured goals.
* **Trigger Condition:** User accepts or initiates a daily or weekly mission.
* **Required Properties:** `event_id, user_id, mission_id, mission_type, timestamp`
* **Optional Properties:** `target_count, session_id`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `event_id: string, user_id: string, mission_id: string`
* **Allowed Values & Constraints:** `mission_type in ('Daily', 'Weekly', 'Special')`
* **Validation Rules:** mission_id must exist in active mission catalogue.
* **Negative Test Cases:** Starting expired mission.
* **Acceptance Criteria:** Sets mission_activity = 'Yes' in daily_activity.
* **Acceptance Test Method:** `Mission accept button emits event.`

#### JSON Payload Example
```json
{
  "event_name": "mission_started",
  "event_id": "EVT000045",
  "user_id": "VLUSR000010",
  "mission_id": "MIS004",
  "mission_type": "Daily",
  "timestamp": "2026-03-15T09:05:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "event_id",
    "user_id",
    "mission_id"
  ]
}
```

---
### Event 17: `mission_completed`
* **Functional Domain:** Missions
* **Implementation Status:** `Observed in Milestones`
* **Business Purpose:** Verify mission requirement completion and disburse bonus.
* **Trigger Condition:** All criteria of an active mission are satisfied.
* **Required Properties:** `event_id, user_id, mission_id, reward_xp, timestamp`
* **Optional Properties:** `badge_unlocked`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `event_id: string, user_id: string, mission_id: string, reward_xp: int`
* **Allowed Values & Constraints:** `reward_xp >= 0`
* **Validation Rules:** Must have prior mission_started record.
* **Negative Test Cases:** Completing without starting; duplicate completion.
* **Acceptance Criteria:** Logs milestone in veloop.milestones (first_mission).
* **Acceptance Test Method:** `Fulfillment of target emits event and grants XP.`

#### JSON Payload Example
```json
{
  "event_name": "mission_completed",
  "event_id": "EVT000088",
  "user_id": "VLUSR000010",
  "mission_id": "MIS004",
  "reward_xp": 100,
  "timestamp": "2026-03-15T09:30:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "event_id",
    "user_id",
    "mission_id",
    "reward_xp"
  ]
}
```

---
### Event 18: `badge_earned`
* **Functional Domain:** Gamification
* **Implementation Status:** `Observed in Feature Events`
* **Business Purpose:** Acknowledge user achievements and gamified milestones.
* **Trigger Condition:** Achievement condition satisfied (e.g., 50 tasks completed).
* **Required Properties:** `event_id, user_id, badge_id, badge_tier, timestamp`
* **Optional Properties:** `xp_bonus`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `event_id: string, user_id: string, badge_id: string, badge_tier: string`
* **Allowed Values & Constraints:** `badge_tier in ('Bronze', 'Silver', 'Gold', 'Platinum')`
* **Validation Rules:** Cannot award same tier badge twice.
* **Negative Test Cases:** Duplicate badge grant; missing badge ID.
* **Acceptance Criteria:** Emits badge telemetry event in feature_events.
* **Acceptance Test Method:** `Milestone condition triggers badge award.`

#### JSON Payload Example
```json
{
  "event_name": "badge_earned",
  "event_id": "EVT000120",
  "user_id": "VLUSR000010",
  "badge_id": "BDG_TASK_MASTER",
  "badge_tier": "Bronze",
  "timestamp": "2026-03-15T10:00:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "event_id",
    "user_id",
    "badge_id"
  ]
}
```

---
### Event 19: `spin_started`
* **Functional Domain:** Gamification
* **Implementation Status:** `Observed in Feature Events`
* **Business Purpose:** Record spin wheel initiation and anti-cheat tracking.
* **Trigger Condition:** User taps 'Spin Now' button on wheel screen.
* **Required Properties:** `event_id, user_id, spin_cost_xp, timestamp`
* **Optional Properties:** `session_id, free_spin_flag`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `event_id: string, user_id: string, spin_cost_xp: int`
* **Allowed Values & Constraints:** `spin_cost_xp >= 0`
* **Validation Rules:** User must have adequate balance if cost > 0.
* **Negative Test Cases:** Spinning with insufficient balance.
* **Acceptance Criteria:** Sets spin_activity = 'Yes' in daily_activity.
* **Acceptance Test Method:** `Wheel spin button emits event.`

#### JSON Payload Example
```json
{
  "event_name": "spin_started",
  "event_id": "EVT000150",
  "user_id": "VLUSR000015",
  "spin_cost_xp": 0,
  "timestamp": "2026-03-15T10:10:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "event_id",
    "user_id",
    "spin_cost_xp"
  ]
}
```

---
### Event 20: `spin_completed`
* **Functional Domain:** Gamification
* **Implementation Status:** `Observed in Feature Events`
* **Business Purpose:** Record spin wheel outcome and prize disbursement.
* **Trigger Condition:** Wheel stops on winning wedge.
* **Required Properties:** `event_id, user_id, prize_type, prize_value, timestamp`
* **Optional Properties:** `multiplier`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `event_id: string, user_id: string, prize_type: string, prize_value: int`
* **Allowed Values & Constraints:** `prize_type in ('XP', 'GEMS', 'TOKENS', 'BETTER_LUCK')`
* **Validation Rules:** prize_value >= 0.
* **Negative Test Cases:** Disbursing negative prize.
* **Acceptance Criteria:** Credits winning prize to user balance.
* **Acceptance Test Method:** `Wheel stop triggers credit.`

#### JSON Payload Example
```json
{
  "event_name": "spin_completed",
  "event_id": "EVT000151",
  "user_id": "VLUSR000015",
  "prize_type": "XP",
  "prize_value": 25,
  "timestamp": "2026-03-15T10:10:15Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "event_id",
    "user_id",
    "prize_type",
    "prize_value"
  ]
}
```

---
### Event 21: `referral_created`
* **Functional Domain:** Referral
* **Implementation Status:** `Observed in Feature Events`
* **Business Purpose:** Track unique referral link or invitation code generation.
* **Trigger Condition:** User opens referral tab and generates unique sharing link.
* **Required Properties:** `event_id, user_id, referral_code, timestamp`
* **Optional Properties:** `channel`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `event_id: string, user_id: string, referral_code: string`
* **Allowed Values & Constraints:** `referral_code format '^VL[0-9]{6}$'`
* **Validation Rules:** referral_code must match user's assigned code in users table.
* **Negative Test Cases:** Malformed referral code syntax.
* **Acceptance Criteria:** Logs referral creation in feature_events.
* **Acceptance Test Method:** `Opening referral screen triggers event.`

#### JSON Payload Example
```json
{
  "event_name": "referral_created",
  "event_id": "EVT000201",
  "user_id": "VLUSR000020",
  "referral_code": "VL850800",
  "timestamp": "2026-03-15T11:00:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "event_id",
    "user_id",
    "referral_code"
  ]
}
```

---
### Event 22: `referral_registered`
* **Functional Domain:** Referral
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Attribute newly registered referee to referrer user ID.
* **Trigger Condition:** Referee completes registration using referrer's invite code.
* **Required Properties:** `referral_id, referrer_user_id, referee_user_id, referral_code, timestamp`
* **Optional Properties:** `campaign`
* **User Identifier Requirement:** Mandatory (both referrer and referee)
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `referral_id: string, referrer_user_id: string, referee_user_id: string, referral_code: string`
* **Allowed Values & Constraints:** `referrer_user_id != referee_user_id`
* **Validation Rules:** Self-referral is strictly prohibited: referrer != referee.
* **Negative Test Cases:** Self-referral; referee already registered under another code.
* **Acceptance Criteria:** Creates entry in veloop.referrals with status 'Registered'.
* **Acceptance Test Method:** `Signup with promo code logs referral pair.`

#### JSON Payload Example
```json
{
  "event_name": "referral_registered",
  "referral_id": "REF000100",
  "referrer_user_id": "VLUSR000020",
  "referee_user_id": "VLUSR000150",
  "referral_code": "VL850800",
  "timestamp": "2026-03-15T12:00:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "referral_id",
    "referrer_user_id",
    "referee_user_id",
    "referral_code"
  ]
}
```

---
### Event 23: `referral_activated`
* **Functional Domain:** Referral
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Track when referred referee completes first qualifying action.
* **Trigger Condition:** Referee completes first task, check-in, or session.
* **Required Properties:** `referral_id, referrer_user_id, referee_user_id, qualifying_action, timestamp`
* **Optional Properties:** `task_id`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `referral_id: string, qualifying_action: string`
* **Allowed Values & Constraints:** `qualifying_action in ('first_task_completion', 'first_login', 'onboarding_completed')`
* **Validation Rules:** Must have preceding referral_registered status.
* **Negative Test Cases:** Activating before registration; duplicate activation.
* **Acceptance Criteria:** Updates referral status to 'Activated'.
* **Acceptance Test Method:** `Task completion triggers activation check.`

#### JSON Payload Example
```json
{
  "event_name": "referral_activated",
  "referral_id": "REF000100",
  "referrer_user_id": "VLUSR000020",
  "referee_user_id": "VLUSR000150",
  "qualifying_action": "first_task_completion",
  "timestamp": "2026-03-15T12:30:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "referral_id",
    "referrer_user_id",
    "referee_user_id",
    "qualifying_action"
  ]
}
```

---
### Event 24: `referral_converted`
* **Functional Domain:** Referral
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Disburse referral bonus points to both referrer and referee.
* **Trigger Condition:** Activation verified and anti-fraud checks pass.
* **Required Properties:** `referral_id, referrer_user_id, referee_user_id, bonus_xp_credited, timestamp`
* **Optional Properties:** `fraud_score`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `referral_id: string, bonus_xp_credited: int`
* **Allowed Values & Constraints:** `bonus_xp_credited > 0`
* **Validation Rules:** Atomic double credit: awards bonus to referrer and referee.
* **Negative Test Cases:** Crediting zero bonus; crediting unactivated referral.
* **Acceptance Criteria:** Updates referral status to 'Reward_Disbursed' and commits ledger entries.
* **Acceptance Test Method:** `Payout execution commits XP and logs event.`

#### JSON Payload Example
```json
{
  "event_name": "referral_converted",
  "referral_id": "REF000100",
  "referrer_user_id": "VLUSR000020",
  "referee_user_id": "VLUSR000150",
  "bonus_xp_credited": 100,
  "timestamp": "2026-03-15T12:30:05Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "referral_id",
    "referrer_user_id",
    "bonus_xp_credited"
  ]
}
```

---
### Event 25: `wallet_transaction_created`
* **Functional Domain:** Wallet
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Initiate double-entry ledger balance transaction.
* **Trigger Condition:** User or system queues balance adjustment (earning or payout).
* **Required Properties:** `transaction_id, user_id, currency, amount, transaction_type, reference_id, timestamp`
* **Optional Properties:** `narration`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `transaction_id: string, user_id: string, currency: string, amount: numeric(14,2)`
* **Allowed Values & Constraints:** `currency in ('XP', 'GEMS', 'TOKENS', 'INR'); transaction_type in ('Credit', 'Debit', 'Hold')`
* **Validation Rules:** amount must be > 0.00; transaction_id must be globally unique.
* **Negative Test Cases:** amount <= 0; invalid currency code; duplicate transaction_id.
* **Acceptance Criteria:** Creates pending transaction record in veloop.wallet_ledger.
* **Acceptance Test Method:** `Queue transaction API returns HTTP 201.`

#### JSON Payload Example
```json
{
  "event_name": "wallet_transaction_created",
  "transaction_id": "TXN98101",
  "user_id": "VLUSR000020",
  "currency": "XP",
  "amount": 100.0,
  "transaction_type": "Credit",
  "reference_id": "RWD000100",
  "timestamp": "2026-03-15T13:00:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "transaction_id",
    "user_id",
    "currency",
    "amount",
    "transaction_type"
  ]
}
```

---
### Event 26: `wallet_transaction_completed`
* **Functional Domain:** Wallet
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Confirm double-entry ledger commitment and balance settlement.
* **Trigger Condition:** PostgreSQL COMMIT executes with zero Net Debit/Credit imbalance.
* **Required Properties:** `transaction_id, user_id, amount, balance_after, timestamp`
* **Optional Properties:** `settlement_batch_id`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `transaction_id: string, user_id: string, amount: numeric, balance_after: numeric`
* **Allowed Values & Constraints:** `balance_after >= 0.00`
* **Validation Rules:** balance_after must equal balance_before +/- amount exactly.
* **Negative Test Cases:** balance_after mathematically inconsistent with amount.
* **Acceptance Criteria:** Status in wallet_transactions set to 'Settled'.
* **Acceptance Test Method:** `Commit confirmation dispatches event.`

#### JSON Payload Example
```json
{
  "event_name": "wallet_transaction_completed",
  "transaction_id": "TXN98101",
  "user_id": "VLUSR000020",
  "amount": 100.0,
  "balance_after": 350.0,
  "timestamp": "2026-03-15T13:00:01Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "transaction_id",
    "user_id",
    "amount",
    "balance_after"
  ]
}
```

---
### Event 27: `wallet_transaction_reversed`
* **Functional Domain:** Wallet
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Log reversal of unsettled or disputed financial transactions.
* **Trigger Condition:** Transaction rollback or manual administrative void.
* **Required Properties:** `transaction_id, original_transaction_id, reversal_reason, timestamp`
* **Optional Properties:** `admin_user_id`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `transaction_id: string, original_transaction_id: string, reversal_reason: string`
* **Allowed Values & Constraints:** `valid original_transaction_id`
* **Validation Rules:** Creates offsetting debit/credit entry in ledger.
* **Negative Test Cases:** Reversing non-existent transaction.
* **Acceptance Criteria:** Sets status to 'Reversed' in ledger.
* **Acceptance Test Method:** `Rollback trigger logs reversal event.`

#### JSON Payload Example
```json
{
  "event_name": "wallet_transaction_reversed",
  "transaction_id": "REV98101",
  "original_transaction_id": "TXN98101",
  "reversal_reason": "Payment_Gateway_Timeout",
  "timestamp": "2026-03-15T13:10:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "transaction_id",
    "original_transaction_id",
    "reversal_reason"
  ]
}
```

---
### Event 28: `withdrawal_requested`
* **Functional Domain:** Withdrawals
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Log user request to convert earned tokens to fiat currency.
* **Trigger Condition:** User taps 'Confirm Withdrawal' after selecting payout rail.
* **Required Properties:** `withdrawal_id, user_id, tokens_debited, fiat_amount, fiat_currency, payout_rail, timestamp`
* **Optional Properties:** `beneficiary_mask`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Mandatory
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `withdrawal_id: string, user_id: string, tokens_debited: numeric, fiat_amount: numeric, payout_rail: string`
* **Allowed Values & Constraints:** `tokens_debited >= 50.00; payout_rail in ('UPI', 'Paytm', 'NEFT', 'IMPS'); fiat_currency = 'INR'`
* **Validation Rules:** User token balance must be >= tokens_debited; minimum threshold 50.00 tokens.
* **Negative Test Cases:** Requesting below 50.00 threshold; requesting with insufficient balance.
* **Acceptance Criteria:** Creates record in veloop.withdrawals with status 'Requested'.
* **Acceptance Test Method:** `POST /api/v1/withdrawals creates row and emits event.`

#### JSON Payload Example
```json
{
  "event_name": "withdrawal_requested",
  "withdrawal_id": "WDL000450",
  "user_id": "VLUSR000020",
  "tokens_debited": 100.0,
  "fiat_amount": 500.0,
  "fiat_currency": "INR",
  "payout_rail": "UPI",
  "timestamp": "2026-03-15T14:00:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "withdrawal_id",
    "user_id",
    "tokens_debited",
    "fiat_amount",
    "payout_rail"
  ]
}
```

---
### Event 29: `withdrawal_processing`
* **Functional Domain:** Withdrawals
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Track when payout batch is handed off to payment gateway / banking rail.
* **Trigger Condition:** Automated payout engine picks up requested withdrawal.
* **Required Properties:** `withdrawal_id, gateway_partner, batch_id, timestamp`
* **Optional Properties:** `estimated_settlement_time`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `withdrawal_id: string, gateway_partner: string, batch_id: string`
* **Allowed Values & Constraints:** `valid gateway_partner string`
* **Validation Rules:** Previous status must be 'Requested'.
* **Negative Test Cases:** Processing already completed withdrawal.
* **Acceptance Criteria:** Updates status to 'Processing' in veloop.withdrawals.
* **Acceptance Test Method:** `Batch engine transitions status and emits event.`

#### JSON Payload Example
```json
{
  "event_name": "withdrawal_processing",
  "withdrawal_id": "WDL000450",
  "gateway_partner": "Razorpay_Payouts",
  "batch_id": "BATCH_20260315_01",
  "timestamp": "2026-03-15T14:05:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "withdrawal_id",
    "gateway_partner",
    "batch_id"
  ]
}
```

---
### Event 30: `withdrawal_completed`
* **Functional Domain:** Withdrawals
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Confirm fiat bank credit and close withdrawal SLA tracking.
* **Trigger Condition:** Bank / UPI webhook confirms successful beneficiary settlement.
* **Required Properties:** `withdrawal_id, user_id, fiat_amount, payout_reference, sla_duration_hours, timestamp`
* **Optional Properties:** `utr_number`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `withdrawal_id: string, user_id: string, fiat_amount: numeric, payout_reference: string, sla_duration_hours: numeric`
* **Allowed Values & Constraints:** `fiat_amount > 0.00; payout_reference must be non-empty`
* **Validation Rules:** payout_reference must be unique.
* **Negative Test Cases:** Duplicate payout reference; completing unrequested withdrawal.
* **Acceptance Criteria:** Updates status to 'Settled' and records processed_at timestamp.
* **Acceptance Test Method:** `Gateway webhook triggers completion event.`

#### JSON Payload Example
```json
{
  "event_name": "withdrawal_completed",
  "withdrawal_id": "WDL000450",
  "user_id": "VLUSR000020",
  "fiat_amount": 500.0,
  "payout_reference": "UTR9948210381",
  "sla_duration_hours": 1.25,
  "timestamp": "2026-03-15T15:15:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "withdrawal_id",
    "user_id",
    "fiat_amount",
    "payout_reference"
  ]
}
```

---
### Event 31: `withdrawal_rejected`
* **Functional Domain:** Withdrawals
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Log rejected payouts and release held user token balance.
* **Trigger Condition:** Beneficiary bank rejects transfer (e.g., invalid UPI ID / Account closed).
* **Required Properties:** `withdrawal_id, user_id, rejection_reason, timestamp`
* **Optional Properties:** `tokens_refunded`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `withdrawal_id: string, user_id: string, rejection_reason: string`
* **Allowed Values & Constraints:** `rejection_reason in ('Invalid_VPA_Address', 'Account_Frozen', 'Beneficiary_Name_Mismatch')`
* **Validation Rules:** Must automatically trigger token refund credit back to user balance.
* **Negative Test Cases:** Rejecting without refunding tokens.
* **Acceptance Criteria:** Updates status to 'Rejected' and credits tokens back to user.
* **Acceptance Test Method:** `Bank rejection webhook triggers refund and logs event.`

#### JSON Payload Example
```json
{
  "event_name": "withdrawal_rejected",
  "withdrawal_id": "WDL000455",
  "user_id": "VLUSR000030",
  "rejection_reason": "Invalid_VPA_Address",
  "timestamp": "2026-03-15T14:15:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "withdrawal_id",
    "user_id",
    "rejection_reason"
  ]
}
```

---
### Event 32: `withdrawal_reversed`
* **Functional Domain:** Withdrawals
* **Implementation Status:** `Proposed Future Spec`
* **Business Purpose:** Log post-settlement clawbacks or banking reversal callbacks.
* **Trigger Condition:** Payment rail issues chargeback or reversal notice post-settlement.
* **Required Properties:** `withdrawal_id, user_id, reversal_reference, timestamp`
* **Optional Properties:** `admin_case_id`
* **User Identifier Requirement:** Mandatory
* **Session Identifier Requirement:** Optional
* **Timestamp Format:** `ISO 8601 UTC`
* **Field Data Types:** `withdrawal_id: string, user_id: string, reversal_reference: string`
* **Allowed Values & Constraints:** `valid reversal_reference`
* **Validation Rules:** Updates status to 'Reversed' in veloop.withdrawals.
* **Negative Test Cases:** Reversing non-settled withdrawal.
* **Acceptance Criteria:** Creates reversal audit trail in financial ledger.
* **Acceptance Test Method:** `Reversal webhook triggers ledger adjustment.`

#### JSON Payload Example
```json
{
  "event_name": "withdrawal_reversed",
  "withdrawal_id": "WDL000450",
  "user_id": "VLUSR000020",
  "reversal_reference": "REV_UTR_88319",
  "timestamp": "2026-03-16T10:00:00Z"
}
```

#### JSON Schema
```json
{
  "type": "object",
  "required": [
    "event_name",
    "withdrawal_id",
    "user_id",
    "reversal_reference"
  ]
}
```

---

## Current implementation status — 25 November 2026

This deliverable is an analytical specification/report and must be read separately from runtime verification. The current Streamlit source contains seven navigation sections: Overview, User Analytics, Earning & Rewards, Wallet & Withdrawal, Referral & Virality, Feature & Engagement, and Data Quality & Audit. Workbook-level simulated records are not interchangeable with PostgreSQL-loaded records.

The supplied PostgreSQL execution evidence is marked `AUTH_REQUIRED_NOT_VERIFIED`; successful live database execution is therefore not established by that evidence. The automated project test suite was rerun for this archive and passed 40/40 tests. This does not verify live PostgreSQL, production payment settlement, or public dashboard deployment.

Wallet, withdrawal, user, session, event, task, and milestone examples are simulated/test data. Referral event activity must not be described as verified referral conversion without validated referrer/referee relationship records. A proposed schema or KPI definition is not evidence that the corresponding production workflow is deployed.
