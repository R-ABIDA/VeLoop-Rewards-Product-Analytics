"""
VELOOP REWARDS — COMPLETE 32-EVENT TRACKING PLAN GENERATOR
Deliverable 08 | Work Package F
Generates both Event_Tracking_Plan.md and Event_Tracking_Plan.xlsx
Includes all 16 required engineering attributes for every single event:
  1. Event name
  2. Business purpose
  3. Trigger condition
  4. Required properties
  5. Optional properties
  6. User identifier requirements
  7. Session identifier requirements
  8. Timestamp format
  9. JSON payload example
  10. JSON schema
  11. Field data types
  12. Allowed values
  13. Validation rules
  14. Negative test cases
  15. Acceptance criteria
  16. Acceptance test
"""

import os
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

event_definitions = [
    # ACCOUNT DOMAIN
    {
        "name": "user_registered",
        "domain": "Account",
        "status": "Observed in Clean Users",
        "purpose": "Capture new user account creation and attribution origin.",
        "trigger": "User successfully completes the registration flow.",
        "req_props": ["user_id", "email", "registration_datetime", "acquisition_source", "platform", "country"],
        "opt_props": ["referral_source_detail", "marketing_opt_in", "account_created_via"],
        "user_id_req": "Mandatory (e.g. VLUSR000001)",
        "session_id_req": "Optional on first signup",
        "ts_format": "ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)",
        "json_example": {
            "event_name": "user_registered",
            "user_id": "VLUSR000101",
            "email": "user101@example.com",
            "registration_datetime": "2026-03-15T10:14:00Z",
            "acquisition_source": "Organic Search",
            "platform": "Android",
            "country": "IN",
            "marketing_opt_in": True
        },
        "json_schema": {
            "type": "object",
            "required": ["event_name", "user_id", "email", "registration_datetime", "acquisition_source", "platform", "country"],
            "properties": {
                "event_name": {"type": "string", "enum": ["user_registered"]},
                "user_id": {"type": "string", "pattern": "^VLUSR[0-9]{6}$"},
                "email": {"type": "string", "format": "email"},
                "registration_datetime": {"type": "string", "format": "date-time"},
                "acquisition_source": {"type": "string"},
                "platform": {"type": "string", "enum": ["Android", "iOS", "Web", "Windows", "macOS"]},
                "country": {"type": "string", "minLength": 2, "maxLength": 2}
            }
        },
        "data_types": "user_id: string, email: string, registration_datetime: timestamptz, acquisition_source: string, platform: string, country: char(2)",
        "allowed_values": "platform in ('Android', 'iOS', 'Web', 'Windows', 'macOS'); country in ('IN', 'US', etc.)",
        "validation_rules": "Email must conform to RFC 5322; Age must be >= 18; user_id must be unique.",
        "negative_tests": "Null email; duplicate user_id; age < 18; malformed timestamp format.",
        "acceptance_criteria": "Event emitted within 500ms of user commitment to PostgreSQL users table.",
        "acceptance_test": "POST /api/v1/events/user_registered with valid payload returns HTTP 201."
    },
    {
        "name": "user_logged_in",
        "domain": "Account",
        "status": "Observed in Sessions",
        "purpose": "Track session initiation and user authentication frequency.",
        "trigger": "User submits valid credentials and JWT auth token is issued.",
        "req_props": ["user_id", "session_id", "timestamp", "device", "platform"],
        "opt_props": ["ip_hash", "app_version"],
        "user_id_req": "Mandatory",
        "session_id_req": "Mandatory (links session start)",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "user_logged_in",
            "user_id": "VLUSR000101",
            "session_id": "SESS000214",
            "timestamp": "2026-03-15T10:15:00Z",
            "device": "Android",
            "platform": "Mobile"
        },
        "json_schema": {
            "type": "object",
            "required": ["event_name", "user_id", "session_id", "timestamp", "device", "platform"],
            "properties": {
                "event_name": {"type": "string", "enum": ["user_logged_in"]},
                "user_id": {"type": "string"},
                "session_id": {"type": "string"},
                "timestamp": {"type": "string", "format": "date-time"}
            }
        },
        "data_types": "user_id: string, session_id: string, timestamp: timestamptz, device: string",
        "allowed_values": "device in ('Android', 'Windows', 'iOS', 'macOS')",
        "validation_rules": "session_id must match active session table; timestamp must be <= CURRENT_TIMESTAMP.",
        "negative_tests": "Expired session token; future login timestamp; unregistered user_id.",
        "acceptance_criteria": "Increments daily session_count for user in veloop.daily_activity.",
        "acceptance_test": "Successful auth endpoint triggers event log with valid session_id."
    },
    {
        "name": "user_logged_out",
        "domain": "Account",
        "status": "Proposed Future Spec",
        "purpose": "Track session closure and measure session duration accurately.",
        "trigger": "User taps logout button or inactivity timeout threshold triggers.",
        "req_props": ["user_id", "session_id", "timestamp", "logout_reason"],
        "opt_props": ["session_duration_seconds"],
        "user_id_req": "Mandatory",
        "session_id_req": "Mandatory",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "user_logged_out",
            "user_id": "VLUSR000101",
            "session_id": "SESS000214",
            "timestamp": "2026-03-15T10:35:00Z",
            "logout_reason": "User_Action"
        },
        "json_schema": {
            "type": "object",
            "required": ["event_name", "user_id", "session_id", "timestamp", "logout_reason"],
            "properties": {
                "logout_reason": {"type": "string", "enum": ["User_Action", "Timeout", "Revoked"]}
            }
        },
        "data_types": "user_id: string, session_id: string, timestamp: timestamptz, logout_reason: string",
        "allowed_values": "logout_reason in ('User_Action', 'Timeout', 'Revoked')",
        "validation_rules": "timestamp must be greater than session_start.",
        "negative_tests": "Logout timestamp earlier than session_start; non-existent session_id.",
        "acceptance_criteria": "Updates veloop.sessions session_end timestamp and calculates duration.",
        "acceptance_test": "POST logout endpoint commits session_end and emits user_logged_out."
    },
    {
        "name": "onboarding_started",
        "domain": "Account",
        "status": "Proposed Future Spec",
        "purpose": "Monitor the beginning of the interactive user onboarding tour.",
        "trigger": "First app launch after successful registration.",
        "req_props": ["user_id", "session_id", "timestamp", "step_number"],
        "opt_props": ["tour_version"],
        "user_id_req": "Mandatory",
        "session_id_req": "Mandatory",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "onboarding_started",
            "user_id": "VLUSR000101",
            "session_id": "SESS000214",
            "timestamp": "2026-03-15T10:15:30Z",
            "step_number": 1
        },
        "json_schema": {"type": "object", "required": ["event_name", "user_id", "session_id", "step_number"]},
        "data_types": "user_id: string, session_id: string, step_number: int",
        "allowed_values": "step_number >= 1",
        "validation_rules": "Emitted only once per user_id lifetime.",
        "negative_tests": "Emitting with step_number <= 0; emitting without active session.",
        "acceptance_criteria": "Flag onboarding_status set to 'Incomplete' in user table.",
        "acceptance_test": "New user tour load dispatches event."
    },
    {
        "name": "onboarding_completed",
        "domain": "Account",
        "status": "Proposed Future Spec",
        "purpose": "Measure onboarding funnel completion velocity and drop-off.",
        "trigger": "User completes final onboarding walkthrough step.",
        "req_props": ["user_id", "session_id", "timestamp", "total_steps_completed", "duration_seconds"],
        "opt_props": ["reward_granted"],
        "user_id_req": "Mandatory",
        "session_id_req": "Mandatory",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "onboarding_completed",
            "user_id": "VLUSR000101",
            "session_id": "SESS000214",
            "timestamp": "2026-03-15T10:18:00Z",
            "total_steps_completed": 5,
            "duration_seconds": 150
        },
        "json_schema": {"type": "object", "required": ["event_name", "user_id", "session_id", "total_steps_completed"]},
        "data_types": "user_id: string, total_steps_completed: int, duration_seconds: int",
        "allowed_values": "total_steps_completed >= 1; duration_seconds > 0",
        "validation_rules": "User must have existing onboarding_started event.",
        "negative_tests": "Duration negative; user already completed onboarding.",
        "acceptance_criteria": "Updates onboarding_status to 'Completed' in users table.",
        "acceptance_test": "Completing tour triggers status update and event emission."
    },

    # TASK DOMAIN
    {
        "name": "task_viewed",
        "domain": "Tasks",
        "status": "Observed in Task Activity",
        "purpose": "Track task catalog impressions and user offer discovery.",
        "trigger": "Task card becomes visible on user device viewport.",
        "req_props": ["activity_id", "user_id", "task_id", "task_category", "timestamp"],
        "opt_props": ["device", "session_id"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "task_viewed",
            "activity_id": "ACT000001",
            "user_id": "VLUSR000001",
            "task_id": "TSK0012",
            "task_category": "Watch Ads",
            "timestamp": "2026-03-15T11:00:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "activity_id", "user_id", "task_id", "task_category", "timestamp"]},
        "data_types": "activity_id: string, user_id: string, task_id: string, task_category: string",
        "allowed_values": "task_category in ('Watch Ads', 'Mining Rewards', 'Daily Check-in', 'Missions', 'Tap & Earn', 'Spin the Wheel')",
        "validation_rules": "activity_id must be unique.",
        "negative_tests": "Missing task_id; invalid category string.",
        "acceptance_criteria": "Logged in veloop.task_activity as Viewed.",
        "acceptance_test": "Viewport card intersection triggers event."
    },
    {
        "name": "task_opened",
        "domain": "Tasks",
        "status": "Proposed Future Spec",
        "purpose": "Track user click-through into detailed task instructions.",
        "trigger": "User taps task card to inspect details and requirements.",
        "req_props": ["activity_id", "user_id", "task_id", "timestamp"],
        "opt_props": ["session_id", "estimated_payout_xp"],
        "user_id_req": "Mandatory",
        "session_id_req": "Mandatory",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "task_opened",
            "activity_id": "ACT000001",
            "user_id": "VLUSR000001",
            "task_id": "TSK0012",
            "timestamp": "2026-03-15T11:00:15Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "activity_id", "user_id", "task_id"]},
        "data_types": "activity_id: string, user_id: string, task_id: string",
        "allowed_values": "task_id must exist in catalog",
        "validation_rules": "Requires preceding task_viewed event.",
        "negative_tests": "Opening inactive or expired task.",
        "acceptance_criteria": "Tracks intermediate engagement in micro-task funnel.",
        "acceptance_test": "Card tap emits event."
    },
    {
        "name": "task_started",
        "domain": "Tasks",
        "status": "Observed in Task Activity",
        "purpose": "Record task initiation and start time for duration tracking.",
        "trigger": "User taps 'Start Task' or enters execution screen.",
        "req_props": ["activity_id", "user_id", "task_id", "timestamp"],
        "opt_props": ["session_id"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "task_started",
            "activity_id": "ACT000001",
            "user_id": "VLUSR000001",
            "task_id": "TSK0012",
            "timestamp": "2026-03-15T11:00:30Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "activity_id", "user_id", "task_id", "timestamp"]},
        "data_types": "activity_id: string, user_id: string, task_id: string, timestamp: timestamptz",
        "allowed_values": "valid task_id",
        "validation_rules": "task_started_at must be >= task_viewed_at.",
        "negative_tests": "Starting task with task_started_at < task_viewed_at.",
        "acceptance_criteria": "Updates task_status in task_activity to Started.",
        "acceptance_test": "Action click dispatches event and updates DB."
    },
    {
        "name": "task_completed",
        "domain": "Tasks",
        "status": "Observed in Task Activity",
        "purpose": "Verify task completion and trigger reward eligibility.",
        "trigger": "User finishes all task requirements or verification callback confirms.",
        "req_props": ["activity_id", "user_id", "task_id", "timestamp", "duration_seconds"],
        "opt_props": ["partner_callback_status"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "task_completed",
            "activity_id": "ACT000001",
            "user_id": "VLUSR000001",
            "task_id": "TSK0012",
            "timestamp": "2026-03-15T11:02:00Z",
            "duration_seconds": 90
        },
        "json_schema": {"type": "object", "required": ["event_name", "activity_id", "user_id", "task_id", "duration_seconds"]},
        "data_types": "activity_id: string, user_id: string, task_id: string, duration_seconds: int",
        "allowed_values": "duration_seconds >= 1",
        "validation_rules": "task_completed_at must be >= task_started_at.",
        "negative_tests": "Duration negative; task not started.",
        "acceptance_criteria": "Updates task_status to 'Completed' in task_activity.",
        "acceptance_test": "Task completion callback commits record and emits event."
    },
    {
        "name": "task_failed",
        "domain": "Tasks",
        "status": "Observed in Task Activity",
        "purpose": "Record micro-task failures, partner rejection, or abandonment.",
        "trigger": "Timeout, user exit, or verification failure.",
        "req_props": ["activity_id", "user_id", "task_id", "failure_reason", "timestamp"],
        "opt_props": ["retry_allowed"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "task_failed",
            "activity_id": "ACT000002",
            "user_id": "VLUSR000002",
            "task_id": "TSK0015",
            "failure_reason": "Timeout_Expired",
            "timestamp": "2026-03-15T11:05:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "activity_id", "user_id", "task_id", "failure_reason"]},
        "data_types": "activity_id: string, user_id: string, failure_reason: string",
        "allowed_values": "failure_reason in ('Timeout_Expired', 'User_Abandoned', 'Partner_Rejected', 'Captcha_Failed')",
        "validation_rules": "Cannot mark task failed after successful reward crediting.",
        "negative_tests": "Empty failure reason; invalid activity ID.",
        "acceptance_criteria": "Updates task_status to Failed in task_activity.",
        "acceptance_test": "Abandonment trigger records failure."
    },

    # REWARDS DOMAIN
    {
        "name": "reward_credited",
        "domain": "Rewards",
        "status": "Observed in Task Activity",
        "purpose": "Record soft currency (XP) credit to user account balance.",
        "trigger": "PostgreSQL transaction successfully increments user xp_balance.",
        "req_props": ["reward_id", "user_id", "reward_type", "amount", "source_feature", "timestamp"],
        "opt_props": ["task_activity_id"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "reward_credited",
            "reward_id": "RWD000100",
            "user_id": "VLUSR000001",
            "reward_type": "XP",
            "amount": 50,
            "source_feature": "Watch Ads",
            "timestamp": "2026-03-15T11:02:01Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "reward_id", "user_id", "reward_type", "amount", "source_feature"]},
        "data_types": "reward_id: string, user_id: string, reward_type: string, amount: int",
        "allowed_values": "reward_type in ('XP', 'GEMS', 'TOKENS'); amount > 0",
        "validation_rules": "amount must be strictly positive; user_id must exist in users table.",
        "negative_tests": "amount <= 0; unknown user_id.",
        "acceptance_criteria": "Increments user xp_balance and records reward_status as 'Credited'.",
        "acceptance_test": "Reward credit commits atomic balance update."
    },
    {
        "name": "reward_pending",
        "domain": "Rewards",
        "status": "Observed in Task Activity",
        "purpose": "Log reward transactions requiring asynchronous partner verification.",
        "trigger": "Task completed awaiting partner server-to-server callback.",
        "req_props": ["activity_id", "user_id", "task_id", "timestamp"],
        "opt_props": ["callback_timeout_seconds"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "reward_pending",
            "activity_id": "ACT000005",
            "user_id": "VLUSR000005",
            "task_id": "TSK0020",
            "timestamp": "2026-03-15T11:10:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "activity_id", "user_id", "task_id"]},
        "data_types": "activity_id: string, user_id: string, task_id: string",
        "allowed_values": "valid task_id",
        "validation_rules": "reward_status set to Pending.",
        "negative_tests": "Missing activity_id.",
        "acceptance_criteria": "Queues task in audit verification pipeline.",
        "acceptance_test": "Pending callback status logs event."
    },
    {
        "name": "reward_reversed",
        "domain": "Rewards",
        "status": "Proposed Future Spec",
        "purpose": "Record revocation of fraudulently credited points or partner chargebacks.",
        "trigger": "Security audit or fraud detection flag confirms abuse.",
        "req_props": ["reward_id", "user_id", "amount", "reversal_reason", "timestamp"],
        "opt_props": ["audit_ticket_id"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "reward_reversed",
            "reward_id": "RWD000100",
            "user_id": "VLUSR000001",
            "amount": 50,
            "reversal_reason": "Bot_Activity_Detected",
            "timestamp": "2026-03-15T12:00:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "reward_id", "user_id", "amount", "reversal_reason"]},
        "data_types": "reward_id: string, user_id: string, amount: int, reversal_reason: string",
        "allowed_values": "reversal_reason in ('Bot_Activity_Detected', 'Duplicate_IP', 'Partner_Chargeback')",
        "validation_rules": "User balance must not drop below zero.",
        "negative_tests": "amount negative; reversing already reversed reward.",
        "acceptance_criteria": "Emits debit entry in ledger and adjusts user balance.",
        "acceptance_test": "Fraud revocation triggers reversal event."
    },
    {
        "name": "daily_reward_claimed",
        "domain": "Rewards",
        "status": "Observed in Feature Events",
        "purpose": "Track daily engagement check-in claims and retention cadence.",
        "trigger": "User taps 'Claim Daily Reward' on check-in screen.",
        "req_props": ["event_id", "user_id", "day_number", "xp_reward", "timestamp"],
        "opt_props": ["session_id", "streak_bonus"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "daily_reward_claimed",
            "event_id": "EVT000010",
            "user_id": "VLUSR000010",
            "day_number": 3,
            "xp_reward": 15,
            "timestamp": "2026-03-15T09:00:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "event_id", "user_id", "day_number", "xp_reward"]},
        "data_types": "event_id: string, user_id: string, day_number: int, xp_reward: int",
        "allowed_values": "day_number between 1 and 7; xp_reward > 0",
        "validation_rules": "Allowed only once per calendar day per user_id.",
        "negative_tests": "Claiming twice on same calendar date.",
        "acceptance_criteria": "Sets daily_reward_claimed = 'Yes' in daily_activity.",
        "acceptance_test": "Claim button triggers credit and daily lock."
    },
    {
        "name": "streak_updated",
        "domain": "Engagement",
        "status": "Observed in Feature Events",
        "purpose": "Track consecutive active day streak progression and breakage.",
        "trigger": "Automated daily midnight batch evaluation or check-in claim.",
        "req_props": ["user_id", "current_streak", "previous_streak", "status", "timestamp"],
        "opt_props": ["streak_broken_flag"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "streak_updated",
            "user_id": "VLUSR000010",
            "current_streak": 4,
            "previous_streak": 3,
            "status": "Maintained",
            "timestamp": "2026-03-15T09:00:01Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "user_id", "current_streak", "status"]},
        "data_types": "user_id: string, current_streak: int, status: string",
        "allowed_values": "status in ('Maintained', 'Broken', 'Reset'); current_streak >= 0",
        "validation_rules": "current_streak must equal previous_streak + 1 when Maintained.",
        "negative_tests": "Negative streak value; missing status.",
        "acceptance_criteria": "Updates daily_streak in veloop.users.",
        "acceptance_test": "Streak calculation commits to database."
    },

    # MISSIONS & GAMIFICATION
    {
        "name": "mission_started",
        "domain": "Missions",
        "status": "Observed in Feature Events",
        "purpose": "Track engagement with multi-step structured goals.",
        "trigger": "User accepts or initiates a daily or weekly mission.",
        "req_props": ["event_id", "user_id", "mission_id", "mission_type", "timestamp"],
        "opt_props": ["target_count", "session_id"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "mission_started",
            "event_id": "EVT000045",
            "user_id": "VLUSR000010",
            "mission_id": "MIS004",
            "mission_type": "Daily",
            "timestamp": "2026-03-15T09:05:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "event_id", "user_id", "mission_id"]},
        "data_types": "event_id: string, user_id: string, mission_id: string",
        "allowed_values": "mission_type in ('Daily', 'Weekly', 'Special')",
        "validation_rules": "mission_id must exist in active mission catalogue.",
        "negative_tests": "Starting expired mission.",
        "acceptance_criteria": "Sets mission_activity = 'Yes' in daily_activity.",
        "acceptance_test": "Mission accept button emits event."
    },
    {
        "name": "mission_completed",
        "domain": "Missions",
        "status": "Observed in Milestones",
        "purpose": "Verify mission requirement completion and disburse bonus.",
        "trigger": "All criteria of an active mission are satisfied.",
        "req_props": ["event_id", "user_id", "mission_id", "reward_xp", "timestamp"],
        "opt_props": ["badge_unlocked"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "mission_completed",
            "event_id": "EVT000088",
            "user_id": "VLUSR000010",
            "mission_id": "MIS004",
            "reward_xp": 100,
            "timestamp": "2026-03-15T09:30:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "event_id", "user_id", "mission_id", "reward_xp"]},
        "data_types": "event_id: string, user_id: string, mission_id: string, reward_xp: int",
        "allowed_values": "reward_xp >= 0",
        "validation_rules": "Must have prior mission_started record.",
        "negative_tests": "Completing without starting; duplicate completion.",
        "acceptance_criteria": "Logs milestone in veloop.milestones (first_mission).",
        "acceptance_test": "Fulfillment of target emits event and grants XP."
    },
    {
        "name": "badge_earned",
        "domain": "Gamification",
        "status": "Observed in Feature Events",
        "purpose": "Acknowledge user achievements and gamified milestones.",
        "trigger": "Achievement condition satisfied (e.g., 50 tasks completed).",
        "req_props": ["event_id", "user_id", "badge_id", "badge_tier", "timestamp"],
        "opt_props": ["xp_bonus"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "badge_earned",
            "event_id": "EVT000120",
            "user_id": "VLUSR000010",
            "badge_id": "BDG_TASK_MASTER",
            "badge_tier": "Bronze",
            "timestamp": "2026-03-15T10:00:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "event_id", "user_id", "badge_id"]},
        "data_types": "event_id: string, user_id: string, badge_id: string, badge_tier: string",
        "allowed_values": "badge_tier in ('Bronze', 'Silver', 'Gold', 'Platinum')",
        "validation_rules": "Cannot award same tier badge twice.",
        "negative_tests": "Duplicate badge grant; missing badge ID.",
        "acceptance_criteria": "Emits badge telemetry event in feature_events.",
        "acceptance_test": "Milestone condition triggers badge award."
    },
    {
        "name": "spin_started",
        "domain": "Gamification",
        "status": "Observed in Feature Events",
        "purpose": "Record spin wheel initiation and anti-cheat tracking.",
        "trigger": "User taps 'Spin Now' button on wheel screen.",
        "req_props": ["event_id", "user_id", "spin_cost_xp", "timestamp"],
        "opt_props": ["session_id", "free_spin_flag"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "spin_started",
            "event_id": "EVT000150",
            "user_id": "VLUSR000015",
            "spin_cost_xp": 0,
            "timestamp": "2026-03-15T10:10:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "event_id", "user_id", "spin_cost_xp"]},
        "data_types": "event_id: string, user_id: string, spin_cost_xp: int",
        "allowed_values": "spin_cost_xp >= 0",
        "validation_rules": "User must have adequate balance if cost > 0.",
        "negative_tests": "Spinning with insufficient balance.",
        "acceptance_criteria": "Sets spin_activity = 'Yes' in daily_activity.",
        "acceptance_test": "Wheel spin button emits event."
    },
    {
        "name": "spin_completed",
        "domain": "Gamification",
        "status": "Observed in Feature Events",
        "purpose": "Record spin wheel outcome and prize disbursement.",
        "trigger": "Wheel stops on winning wedge.",
        "req_props": ["event_id", "user_id", "prize_type", "prize_value", "timestamp"],
        "opt_props": ["multiplier"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "spin_completed",
            "event_id": "EVT000151",
            "user_id": "VLUSR000015",
            "prize_type": "XP",
            "prize_value": 25,
            "timestamp": "2026-03-15T10:10:15Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "event_id", "user_id", "prize_type", "prize_value"]},
        "data_types": "event_id: string, user_id: string, prize_type: string, prize_value: int",
        "allowed_values": "prize_type in ('XP', 'GEMS', 'TOKENS', 'BETTER_LUCK')",
        "validation_rules": "prize_value >= 0.",
        "negative_tests": "Disbursing negative prize.",
        "acceptance_criteria": "Credits winning prize to user balance.",
        "acceptance_test": "Wheel stop triggers credit."
    },

    # REFERRAL DOMAIN
    {
        "name": "referral_created",
        "domain": "Referral",
        "status": "Observed in Feature Events",
        "purpose": "Track unique referral link or invitation code generation.",
        "trigger": "User opens referral tab and generates unique sharing link.",
        "req_props": ["event_id", "user_id", "referral_code", "timestamp"],
        "opt_props": ["channel"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "referral_created",
            "event_id": "EVT000201",
            "user_id": "VLUSR000020",
            "referral_code": "VL850800",
            "timestamp": "2026-03-15T11:00:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "event_id", "user_id", "referral_code"]},
        "data_types": "event_id: string, user_id: string, referral_code: string",
        "allowed_values": "referral_code format '^VL[0-9]{6}$'",
        "validation_rules": "referral_code must match user's assigned code in users table.",
        "negative_tests": "Malformed referral code syntax.",
        "acceptance_criteria": "Logs referral creation in feature_events.",
        "acceptance_test": "Opening referral screen triggers event."
    },
    {
        "name": "referral_registered",
        "domain": "Referral",
        "status": "Proposed Future Spec",
        "purpose": "Attribute newly registered referee to referrer user ID.",
        "trigger": "Referee completes registration using referrer's invite code.",
        "req_props": ["referral_id", "referrer_user_id", "referee_user_id", "referral_code", "timestamp"],
        "opt_props": ["campaign"],
        "user_id_req": "Mandatory (both referrer and referee)",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "referral_registered",
            "referral_id": "REF000100",
            "referrer_user_id": "VLUSR000020",
            "referee_user_id": "VLUSR000150",
            "referral_code": "VL850800",
            "timestamp": "2026-03-15T12:00:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "referral_id", "referrer_user_id", "referee_user_id", "referral_code"]},
        "data_types": "referral_id: string, referrer_user_id: string, referee_user_id: string, referral_code: string",
        "allowed_values": "referrer_user_id != referee_user_id",
        "validation_rules": "Self-referral is strictly prohibited: referrer != referee.",
        "negative_tests": "Self-referral; referee already registered under another code.",
        "acceptance_criteria": "Creates entry in veloop.referrals with status 'Registered'.",
        "acceptance_test": "Signup with promo code logs referral pair."
    },
    {
        "name": "referral_activated",
        "domain": "Referral",
        "status": "Proposed Future Spec",
        "purpose": "Track when referred referee completes first qualifying action.",
        "trigger": "Referee completes first task, check-in, or session.",
        "req_props": ["referral_id", "referrer_user_id", "referee_user_id", "qualifying_action", "timestamp"],
        "opt_props": ["task_id"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "referral_activated",
            "referral_id": "REF000100",
            "referrer_user_id": "VLUSR000020",
            "referee_user_id": "VLUSR000150",
            "qualifying_action": "first_task_completion",
            "timestamp": "2026-03-15T12:30:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "referral_id", "referrer_user_id", "referee_user_id", "qualifying_action"]},
        "data_types": "referral_id: string, qualifying_action: string",
        "allowed_values": "qualifying_action in ('first_task_completion', 'first_login', 'onboarding_completed')",
        "validation_rules": "Must have preceding referral_registered status.",
        "negative_tests": "Activating before registration; duplicate activation.",
        "acceptance_criteria": "Updates referral status to 'Activated'.",
        "acceptance_test": "Task completion triggers activation check."
    },
    {
        "name": "referral_converted",
        "domain": "Referral",
        "status": "Proposed Future Spec",
        "purpose": "Disburse referral bonus points to both referrer and referee.",
        "trigger": "Activation verified and anti-fraud checks pass.",
        "req_props": ["referral_id", "referrer_user_id", "referee_user_id", "bonus_xp_credited", "timestamp"],
        "opt_props": ["fraud_score"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "referral_converted",
            "referral_id": "REF000100",
            "referrer_user_id": "VLUSR000020",
            "referee_user_id": "VLUSR000150",
            "bonus_xp_credited": 100,
            "timestamp": "2026-03-15T12:30:05Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "referral_id", "referrer_user_id", "bonus_xp_credited"]},
        "data_types": "referral_id: string, bonus_xp_credited: int",
        "allowed_values": "bonus_xp_credited > 0",
        "validation_rules": "Atomic double credit: awards bonus to referrer and referee.",
        "negative_tests": "Crediting zero bonus; crediting unactivated referral.",
        "acceptance_criteria": "Updates referral status to 'Reward_Disbursed' and commits ledger entries.",
        "acceptance_test": "Payout execution commits XP and logs event."
    },

    # WALLET DOMAIN
    {
        "name": "wallet_transaction_created",
        "domain": "Wallet",
        "status": "Proposed Future Spec",
        "purpose": "Initiate double-entry ledger balance transaction.",
        "trigger": "User or system queues balance adjustment (earning or payout).",
        "req_props": ["transaction_id", "user_id", "currency", "amount", "transaction_type", "reference_id", "timestamp"],
        "opt_props": ["narration"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "wallet_transaction_created",
            "transaction_id": "TXN98101",
            "user_id": "VLUSR000020",
            "currency": "XP",
            "amount": 100.0,
            "transaction_type": "Credit",
            "reference_id": "RWD000100",
            "timestamp": "2026-03-15T13:00:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "transaction_id", "user_id", "currency", "amount", "transaction_type"]},
        "data_types": "transaction_id: string, user_id: string, currency: string, amount: numeric(14,2)",
        "allowed_values": "currency in ('XP', 'GEMS', 'TOKENS', 'INR'); transaction_type in ('Credit', 'Debit', 'Hold')",
        "validation_rules": "amount must be > 0.00; transaction_id must be globally unique.",
        "negative_tests": "amount <= 0; invalid currency code; duplicate transaction_id.",
        "acceptance_criteria": "Creates pending transaction record in veloop.wallet_ledger.",
        "acceptance_test": "Queue transaction API returns HTTP 201."
    },
    {
        "name": "wallet_transaction_completed",
        "domain": "Wallet",
        "status": "Proposed Future Spec",
        "purpose": "Confirm double-entry ledger commitment and balance settlement.",
        "trigger": "PostgreSQL COMMIT executes with zero Net Debit/Credit imbalance.",
        "req_props": ["transaction_id", "user_id", "amount", "balance_after", "timestamp"],
        "opt_props": ["settlement_batch_id"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "wallet_transaction_completed",
            "transaction_id": "TXN98101",
            "user_id": "VLUSR000020",
            "amount": 100.0,
            "balance_after": 350.0,
            "timestamp": "2026-03-15T13:00:01Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "transaction_id", "user_id", "amount", "balance_after"]},
        "data_types": "transaction_id: string, user_id: string, amount: numeric, balance_after: numeric",
        "allowed_values": "balance_after >= 0.00",
        "validation_rules": "balance_after must equal balance_before +/- amount exactly.",
        "negative_tests": "balance_after mathematically inconsistent with amount.",
        "acceptance_criteria": "Status in wallet_transactions set to 'Settled'.",
        "acceptance_test": "Commit confirmation dispatches event."
    },
    {
        "name": "wallet_transaction_reversed",
        "domain": "Wallet",
        "status": "Proposed Future Spec",
        "purpose": "Log reversal of unsettled or disputed financial transactions.",
        "trigger": "Transaction rollback or manual administrative void.",
        "req_props": ["transaction_id", "original_transaction_id", "reversal_reason", "timestamp"],
        "opt_props": ["admin_user_id"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "wallet_transaction_reversed",
            "transaction_id": "REV98101",
            "original_transaction_id": "TXN98101",
            "reversal_reason": "Payment_Gateway_Timeout",
            "timestamp": "2026-03-15T13:10:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "transaction_id", "original_transaction_id", "reversal_reason"]},
        "data_types": "transaction_id: string, original_transaction_id: string, reversal_reason: string",
        "allowed_values": "valid original_transaction_id",
        "validation_rules": "Creates offsetting debit/credit entry in ledger.",
        "negative_tests": "Reversing non-existent transaction.",
        "acceptance_criteria": "Sets status to 'Reversed' in ledger.",
        "acceptance_test": "Rollback trigger logs reversal event."
    },

    # WITHDRAWAL DOMAIN
    {
        "name": "withdrawal_requested",
        "domain": "Withdrawals",
        "status": "Proposed Future Spec",
        "purpose": "Log user request to convert earned tokens to fiat currency.",
        "trigger": "User taps 'Confirm Withdrawal' after selecting payout rail.",
        "req_props": ["withdrawal_id", "user_id", "tokens_debited", "fiat_amount", "fiat_currency", "payout_rail", "timestamp"],
        "opt_props": ["beneficiary_mask"],
        "user_id_req": "Mandatory",
        "session_id_req": "Mandatory",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "withdrawal_requested",
            "withdrawal_id": "WDL000450",
            "user_id": "VLUSR000020",
            "tokens_debited": 100.0,
            "fiat_amount": 500.0,
            "fiat_currency": "INR",
            "payout_rail": "UPI",
            "timestamp": "2026-03-15T14:00:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "withdrawal_id", "user_id", "tokens_debited", "fiat_amount", "payout_rail"]},
        "data_types": "withdrawal_id: string, user_id: string, tokens_debited: numeric, fiat_amount: numeric, payout_rail: string",
        "allowed_values": "tokens_debited >= 50.00; payout_rail in ('UPI', 'Paytm', 'NEFT', 'IMPS'); fiat_currency = 'INR'",
        "validation_rules": "User token balance must be >= tokens_debited; minimum threshold 50.00 tokens.",
        "negative_tests": "Requesting below 50.00 threshold; requesting with insufficient balance.",
        "acceptance_criteria": "Creates record in veloop.withdrawals with status 'Requested'.",
        "acceptance_test": "POST /api/v1/withdrawals creates row and emits event."
    },
    {
        "name": "withdrawal_processing",
        "domain": "Withdrawals",
        "status": "Proposed Future Spec",
        "purpose": "Track when payout batch is handed off to payment gateway / banking rail.",
        "trigger": "Automated payout engine picks up requested withdrawal.",
        "req_props": ["withdrawal_id", "gateway_partner", "batch_id", "timestamp"],
        "opt_props": ["estimated_settlement_time"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "withdrawal_processing",
            "withdrawal_id": "WDL000450",
            "gateway_partner": "Razorpay_Payouts",
            "batch_id": "BATCH_20260315_01",
            "timestamp": "2026-03-15T14:05:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "withdrawal_id", "gateway_partner", "batch_id"]},
        "data_types": "withdrawal_id: string, gateway_partner: string, batch_id: string",
        "allowed_values": "valid gateway_partner string",
        "validation_rules": "Previous status must be 'Requested'.",
        "negative_tests": "Processing already completed withdrawal.",
        "acceptance_criteria": "Updates status to 'Processing' in veloop.withdrawals.",
        "acceptance_test": "Batch engine transitions status and emits event."
    },
    {
        "name": "withdrawal_completed",
        "domain": "Withdrawals",
        "status": "Proposed Future Spec",
        "purpose": "Confirm fiat bank credit and close withdrawal SLA tracking.",
        "trigger": "Bank / UPI webhook confirms successful beneficiary settlement.",
        "req_props": ["withdrawal_id", "user_id", "fiat_amount", "payout_reference", "sla_duration_hours", "timestamp"],
        "opt_props": ["utr_number"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "withdrawal_completed",
            "withdrawal_id": "WDL000450",
            "user_id": "VLUSR000020",
            "fiat_amount": 500.0,
            "payout_reference": "UTR9948210381",
            "sla_duration_hours": 1.25,
            "timestamp": "2026-03-15T15:15:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "withdrawal_id", "user_id", "fiat_amount", "payout_reference"]},
        "data_types": "withdrawal_id: string, user_id: string, fiat_amount: numeric, payout_reference: string, sla_duration_hours: numeric",
        "allowed_values": "fiat_amount > 0.00; payout_reference must be non-empty",
        "validation_rules": "payout_reference must be unique.",
        "negative_tests": "Duplicate payout reference; completing unrequested withdrawal.",
        "acceptance_criteria": "Updates status to 'Settled' and records processed_at timestamp.",
        "acceptance_test": "Gateway webhook triggers completion event."
    },
    {
        "name": "withdrawal_rejected",
        "domain": "Withdrawals",
        "status": "Proposed Future Spec",
        "purpose": "Log rejected payouts and release held user token balance.",
        "trigger": "Beneficiary bank rejects transfer (e.g., invalid UPI ID / Account closed).",
        "req_props": ["withdrawal_id", "user_id", "rejection_reason", "timestamp"],
        "opt_props": ["tokens_refunded"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "withdrawal_rejected",
            "withdrawal_id": "WDL000455",
            "user_id": "VLUSR000030",
            "rejection_reason": "Invalid_VPA_Address",
            "timestamp": "2026-03-15T14:15:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "withdrawal_id", "user_id", "rejection_reason"]},
        "data_types": "withdrawal_id: string, user_id: string, rejection_reason: string",
        "allowed_values": "rejection_reason in ('Invalid_VPA_Address', 'Account_Frozen', 'Beneficiary_Name_Mismatch')",
        "validation_rules": "Must automatically trigger token refund credit back to user balance.",
        "negative_tests": "Rejecting without refunding tokens.",
        "acceptance_criteria": "Updates status to 'Rejected' and credits tokens back to user.",
        "acceptance_test": "Bank rejection webhook triggers refund and logs event."
    },
    {
        "name": "withdrawal_reversed",
        "domain": "Withdrawals",
        "status": "Proposed Future Spec",
        "purpose": "Log post-settlement clawbacks or banking reversal callbacks.",
        "trigger": "Payment rail issues chargeback or reversal notice post-settlement.",
        "req_props": ["withdrawal_id", "user_id", "reversal_reference", "timestamp"],
        "opt_props": ["admin_case_id"],
        "user_id_req": "Mandatory",
        "session_id_req": "Optional",
        "ts_format": "ISO 8601 UTC",
        "json_example": {
            "event_name": "withdrawal_reversed",
            "withdrawal_id": "WDL000450",
            "user_id": "VLUSR000020",
            "reversal_reference": "REV_UTR_88319",
            "timestamp": "2026-03-16T10:00:00Z"
        },
        "json_schema": {"type": "object", "required": ["event_name", "withdrawal_id", "user_id", "reversal_reference"]},
        "data_types": "withdrawal_id: string, user_id: string, reversal_reference: string",
        "allowed_values": "valid reversal_reference",
        "validation_rules": "Updates status to 'Reversed' in veloop.withdrawals.",
        "negative_tests": "Reversing non-settled withdrawal.",
        "acceptance_criteria": "Creates reversal audit trail in financial ledger.",
        "acceptance_test": "Reversal webhook triggers ledger adjustment."
    }
]

print(f"Total events configured: {len(event_definitions)}")

# Generate Event_Tracking_Plan.md
md_path = "04_deliverables/deliverable_08_event_tracking_plan/Event_Tracking_Plan.md"
os.makedirs(os.path.dirname(md_path), exist_ok=True)

md_content = """# VELOOP REWARDS — PRODUCTION EVENT TRACKING PLAN
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
"""

for i, ev in enumerate(event_definitions, 1):
    md_content += f"| {i} | `{ev['name']}` | {ev['domain']} | **{ev['status']}** | {ev['user_id_req']} | {ev['trigger']} |\n"

md_content += "\n---\n\n## 3. Detailed Engineering Event Specifications\n\n"

for i, ev in enumerate(event_definitions, 1):
    md_content += f"""### Event {i:02d}: `{ev['name']}`
* **Functional Domain:** {ev['domain']}
* **Implementation Status:** `{ev['status']}`
* **Business Purpose:** {ev['purpose']}
* **Trigger Condition:** {ev['trigger']}
* **Required Properties:** `{', '.join(ev['req_props'])}`
* **Optional Properties:** `{', '.join(ev['opt_props'])}`
* **User Identifier Requirement:** {ev['user_id_req']}
* **Session Identifier Requirement:** {ev['session_id_req']}
* **Timestamp Format:** `{ev['ts_format']}`
* **Field Data Types:** `{ev['data_types']}`
* **Allowed Values & Constraints:** `{ev['allowed_values']}`
* **Validation Rules:** {ev['validation_rules']}
* **Negative Test Cases:** {ev['negative_tests']}
* **Acceptance Criteria:** {ev['acceptance_criteria']}
* **Acceptance Test Method:** `{ev['acceptance_test']}`

#### JSON Payload Example
```json
{json.dumps(ev['json_example'], indent=2)}
```

#### JSON Schema
```json
{json.dumps(ev['json_schema'], indent=2)}
```

---
"""

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"Generated {md_path} ({len(md_content)} bytes)")

# Generate Event_Tracking_Plan.xlsx
xlsx_path = "04_deliverables/deliverable_08_event_tracking_plan/Event_Tracking_Plan.xlsx"
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Event_Tracking_Plan"

# Title Header
ws.merge_cells("A1:P1")
ws["A1"] = "VELOOP REWARDS — PRODUCTION EVENT TRACKING PLAN (32 EVENTS)"
ws["A1"].font = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
ws["A1"].fill = PatternFill(start_color="111B2E", end_color="111B2E", fill_type="solid")
ws["A1"].alignment = Alignment(horizontal="center", vertical="center")

ws.merge_cells("A2:P2")
ws["A2"] = "Deliverable 08 | Complete 16-Attribute Engineering Schemas (Work Package F)"
ws["A2"].font = Font(name="Calibri", size=11, bold=True, color="22D3EE")
ws["A2"].fill = PatternFill(start_color="0B1220", end_color="0B1220", fill_type="solid")
ws["A2"].alignment = Alignment(horizontal="center", vertical="center")

ws.merge_cells("A3:P3")
ws["A3"] = "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING | VELOOP REWARDS DATA ANALYST INTERNSHIP"
ws["A3"].font = Font(name="Calibri", size=10, italic=True, color="F59E0B")
ws["A3"].fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
ws["A3"].alignment = Alignment(horizontal="center", vertical="center")

headers = [
    "Req ID", "Event Name", "Domain", "Status", "Business Purpose", "Trigger Condition",
    "Required Properties", "Optional Properties", "User ID Requirement", "Session ID Requirement",
    "Timestamp Format", "Field Data Types", "Allowed Values", "Validation Rules", "Negative Test Cases", "Acceptance Criteria"
]

ws.row_dimensions[5].height = 25
for col_num, h in enumerate(headers, 1):
    c = ws.cell(row=5, column=col_num, value=h)
    c.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    c.fill = PatternFill(start_color="1F2937", end_color="1F2937", fill_type="solid")
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

thin_border = Border(
    left=Side(style='thin', color='E5E7EB'),
    right=Side(style='thin', color='E5E7EB'),
    top=Side(style='thin', color='E5E7EB'),
    bottom=Side(style='thin', color='E5E7EB')
)

for row_idx, ev in enumerate(event_definitions, 6):
    ws.row_dimensions[row_idx].height = 22
    row_vals = [
        f"EVT-{ev['domain'][:3].upper()}-{row_idx-5:02d}",
        ev["name"],
        ev["domain"],
        ev["status"],
        ev["purpose"],
        ev["trigger"],
        ", ".join(ev["req_props"]),
        ", ".join(ev["opt_props"]),
        ev["user_id_req"],
        ev["session_id_req"],
        ev["ts_format"],
        ev["data_types"],
        ev["allowed_values"],
        ev["validation_rules"],
        ev["negative_tests"],
        ev["acceptance_criteria"]
    ]
    fill_color = "F9FAFB" if row_idx % 2 == 0 else "FFFFFF"
    for col_idx, val in enumerate(row_vals, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.font = Font(name="Calibri", size=9)
        cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
        cell.border = thin_border
        cell.alignment = Alignment(vertical="center", wrap_text=True)

# Auto-adjust column widths
for col in ws.columns:
    col_letter = get_column_letter(col[0].column)
    if col[0].column in [1, 3, 4, 9, 10]:
        ws.column_dimensions[col_letter].width = 16
    elif col[0].column == 2:
        ws.column_dimensions[col_letter].width = 24
    else:
        ws.column_dimensions[col_letter].width = 30

wb.save(xlsx_path)
print(f"Generated {xlsx_path} with all 32 events and 16 attributes!")
