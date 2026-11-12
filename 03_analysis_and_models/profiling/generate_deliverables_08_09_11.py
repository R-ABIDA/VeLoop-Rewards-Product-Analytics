"""
VELOOP REWARDS — WORK PACKAGES F, G, I GENERATOR
Generates:
1. Deliverable 08: Event Tracking Plan (Excel) - 30+ production events with all 15 required fields
2. Deliverable 09: Enterprise Data Dictionary (Excel) - 80+ fields across 10 entities with all 12 required fields
3. Deliverable 11: KPI Catalogue (Excel) - 35+ KPIs across 7 domains with mathematical formulas
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Design Palette - VELOOP Professional Navy & Teal
NAVY_HEADER = "1B365D"
TEAL_ACCENT = "008080"
LIGHT_GRAY_FILL = "F8F9FA"
ZEBRA_FILL = "F0F4F8"
WHITE = "FFFFFF"
BORDER_COLOR = "D3D3D3"

STATUS_GREEN = "D4EDDA"
STATUS_YELLOW = "FFF3CD"
STATUS_RED = "F8D7DA"
STATUS_BLUE = "CCE5FF"

def apply_header_style(cell, text, fill_color=NAVY_HEADER, font_size=10, font_color=WHITE, bold=True):
    cell.value = text
    cell.font = Font(name="Calibri", size=font_size, bold=bold, color=font_color)
    cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

def apply_data_cell(cell, value, is_zebra=False, align="left", bold=False, font_size=9, fill_override=None):
    cell.value = value
    cell.font = Font(name="Calibri", size=font_size, bold=bold, color="333333")
    if fill_override:
        cell.fill = PatternFill(start_color=fill_override, end_color=fill_override, fill_type="solid")
    elif is_zebra:
        cell.fill = PatternFill(start_color=ZEBRA_FILL, end_color=ZEBRA_FILL, fill_type="solid")
    else:
        cell.fill = PatternFill(start_color=WHITE, end_color=WHITE, fill_type="solid")
    
    cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=True)
    thin_border = Border(
        left=Side(style='thin', color=BORDER_COLOR),
        right=Side(style='thin', color=BORDER_COLOR),
        top=Side(style='thin', color=BORDER_COLOR),
        bottom=Side(style='thin', color=BORDER_COLOR)
    )
    cell.border = thin_border

def create_banner(ws, title, subtitle, max_col=12):
    end_col = get_column_letter(max_col)
    ws.merge_cells(f"A1:{end_col}1")
    c1 = ws["A1"]
    c1.value = title
    c1.font = Font(name="Calibri", size=13, bold=True, color=WHITE)
    c1.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    c1.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28

    ws.merge_cells(f"A2:{end_col}2")
    c2 = ws["A2"]
    c2.value = subtitle
    c2.font = Font(name="Calibri", size=10, italic=True, color="CCCCCC")
    c2.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    c2.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 20

    ws.merge_cells(f"A3:{end_col}3")
    c3 = ws["A3"]
    c3.value = "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING | VELOOP REWARDS DATA ANALYST INTERNSHIP"
    c3.font = Font(name="Calibri", size=9, bold=True, color="856404")
    c3.fill = PatternFill(start_color=STATUS_YELLOW, end_color=STATUS_YELLOW, fill_type="solid")
    c3.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[3].height = 18

def autofit_columns(ws, min_col=1, max_col=None, padding=3):
    if max_col is None:
        max_col = ws.max_column
    for col in range(min_col, max_col + 1):
        max_len = 0
        col_letter = get_column_letter(col)
        for row in range(5, ws.max_row + 1):
            val = ws.cell(row=row, column=col).value
            if val is not None:
                lines = str(val).split("\n")
                line_max = max(len(l) for l in lines)
                max_len = max(max_len, line_max)
        ws.column_dimensions[col_letter].width = max(min(max_len + padding, 50), 12)

# ==============================================================================
# 1. DELIVERABLE 08: PRODUCTION EVENT TRACKING PLAN (EXCEL)
# ==============================================================================
def generate_event_tracking_plan():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Event_Tracking_Plan"
    ws.views.sheetView[0].showGridLines = True

    create_banner(
        ws,
        "VELOOP REWARDS — PRODUCTION EVENT TRACKING PLAN",
        "Deliverable 08 | 30 Standardized Production Events with Full Engineering Schemas (Work Package F)",
        max_col=16
    )

    headers = [
        "Req ID", "Event Name", "Domain", "Trigger Condition", "Event Definition", 
        "User ID Requirement", "Event ID Format", "Timestamp Spec", "Status", 
        "Required Properties (Payload)", "Optional Properties", "Data Types", 
        "Validation Rule", "Source System", "KPI Dependency", "Status"
    ]
    ws.row_dimensions[5].height = 28
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=5, column=col_idx)
        apply_header_style(cell, h, fill_color=NAVY_HEADER, font_size=10)

    # 30 Comprehensive Production Events across 7 Core Domains
    events = [
        # Account Events (5)
        ("EVT-ACC-01", "user_registered", "Account", "User submits registration form successfully", "Emitted when a new user record is committed to database", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, registration_source, device, platform, auth_method", "country, state, referral_code", 
         "string, string, string, string, string", "Non-null user_id; unique email check", "Auth Microservice", "Total Registrations, Acquisition Share", "Proposed"),
        
        ("EVT-ACC-02", "user_logged_in", "Account", "User successfully authenticates session", "Emitted on JWT token generation or OAuth callback verification", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, session_id, login_method, platform, device", "ip_hash, client_version", 
         "string, string, string, string, string", "Valid active session_id; user_id must exist", "Auth Microservice", "DAU, WAU, MAU, Login Frequency", "Proposed"),
        
        ("EVT-ACC-03", "user_logged_out", "Account", "User clicks logout or session timeout expires", "Emitted on session termination and token invalidation", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, session_id, session_duration_seconds", "logout_reason", 
         "string, string, integer", "duration >= 0; session_id must match active session", "Client App / Auth API", "Average Session Length, Bounce Rate", "Proposed"),

        ("EVT-ACC-04", "onboarding_started", "Account", "User enters first step of onboarding walkthrough", "Tracks initiation of new user product tour", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, session_id, onboarding_version", "entry_point", 
         "string, string, string", "user_id must have account_created_at <= 24h", "Client App", "Onboarding Start Rate", "Proposed"),

        ("EVT-ACC-05", "onboarding_completed", "Account", "User completes final step of onboarding tutorial", "Emitted when user finishes initial product walkthrough", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, session_id, duration_seconds, steps_completed", "reward_claimed_flag", 
         "string, string, integer, integer", "steps_completed == total_onboarding_steps", "Client App", "Onboarding Completion Rate", "Proposed"),

        # Tasks Events (5)
        ("EVT-TSK-01", "task_viewed", "Tasks", "Task card rendered in feed for >= 1.0s", "Measures top-of-funnel task discovery impression", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, task_id, task_category, position_index", "feed_section", 
         "string, string, string, integer", "task_id must exist in task_catalog", "Client App", "Task Impression Volume, CTR", "Confirmed"),

        ("EVT-TSK-02", "task_opened", "Tasks", "User clicks task card to view details", "Tracks intent to evaluate task requirements and reward terms", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, task_id, task_category, reward_offered", "session_id", 
         "string, string, string, decimal", "reward_offered > 0", "Client App", "Task Click-Through Rate", "Confirmed"),

        ("EVT-TSK-03", "task_started", "Tasks", "User clicks 'Start Task' and enters task flow", "Tracks initiation of task execution attempt", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "activity_id, user_id, task_id, task_category, device", "partner_sdk_name", 
         "string, string, string, string, string", "activity_id unique; user_id not suspended", "Client App / Partner SDK", "Task Start Volume, Start Rate", "Confirmed"),

        ("EVT-TSK-04", "task_completed", "Tasks", "User satisfies task completion criteria", "Emitted when client/partner SDK signals task completion", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "activity_id, user_id, task_id, duration_seconds", "completion_proof_hash", 
         "string, string, string, integer", "duration_seconds > 0; activity_id must match started", "Client App / Ingestion API", "Task Completion Rate, Completion Volume", "Confirmed"),

        ("EVT-TSK-05", "task_failed", "Tasks", "Task terminates abnormally or is abandoned", "Captures task drop-off, partner crashes, or timeout", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "activity_id, user_id, task_id, failure_reason", "elapsed_seconds", 
         "string, string, string, string", "failure_reason in allowed enum categories", "Client App / Ingestion API", "Task Failure Rate, Abandonment Rate", "Confirmed"),

        # Rewards Events (3)
        ("EVT-RWD-01", "reward_credited", "Rewards", "Points/cash successfully committed to wallet", "Emitted upon backend double-entry ledger credit execution", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "reward_id, user_id, amount, unit, transaction_id, source", "activity_id", 
         "string, string, decimal, string, string, string", "amount > 0; transaction_id committed in DB", "Wallet Microservice", "Reward Credits, Net Point Volume", "Confirmed"),

        ("EVT-RWD-02", "reward_pending", "Rewards", "Reward placed in escrow hold for verification", "Emitted when high-tier reward requires holding period", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "reward_id, user_id, amount, unit, hold_reason, release_date", "activity_id", 
         "string, string, decimal, string, string, string", "release_date > current_timestamp", "Escrow Service", "Pending Reward Queue, Escrow Volume", "Confirmed"),

        ("EVT-RWD-03", "reward_reversed", "Rewards", "Previously credited reward revoked for fraud", "Emitted upon partner chargeback or anti-cheat clawback", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "reward_id, user_id, clawback_amount, unit, reversal_txn_id, reason", "original_txn_id", 
         "string, string, decimal, string, string, string", "reversal_txn_id != original_txn_id; amount > 0", "Audit / Finance Engine", "Reward Reversal Rate, Fraud Clawbacks", "Proposed"),

        # Daily / Engagement Events (7)
        ("EVT-ENG-01", "daily_reward_claimed", "Daily Engagement", "User claims consecutive daily check-in", "Emitted upon calendar check-in reward disbursement", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, streak_day_number, reward_amount, unit", "multiplier", 
         "string, integer, decimal, string", "streak_day_number between 1 and 7; 24h cooldown enforced", "Engagement Service", "Daily Claim Rate, D7 Retention", "Confirmed"),

        ("EVT-ENG-02", "streak_updated", "Daily Engagement", "User streak incremented or reset to zero", "Emitted when streak engine processes midnight activity cutoff", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, old_streak, new_streak, streak_status", "bonus_xp_credited", 
         "string, integer, integer, string", "streak_status in ('Active', 'Claimed', 'Broken')", "Streak Service", "Streak Retention, Broken Streak Churn", "Confirmed"),

        ("EVT-ENG-03", "mission_started", "Daily Engagement", "User begins multi-step daily/weekly mission", "Tracks mission progress container initialization", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, mission_id, mission_category, target_steps", "deadline_timestamp", 
         "string, string, string, integer", "mission_id must exist; user not previously completed", "Mission Engine", "Mission Start Rate", "Confirmed"),

        ("EVT-ENG-04", "mission_completed", "Daily Engagement", "User finishes all criteria for mission", "Emitted upon mission reward validation and payout", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, mission_id, duration_minutes, reward_amount", "unit", 
         "string, string, decimal, decimal", "all mission step criteria satisfied", "Mission Engine", "Mission Completion Rate", "Confirmed"),

        ("EVT-ENG-05", "badge_earned", "Daily Engagement", "User crosses milestone achievement threshold", "Emitted when trophy / badge is awarded to profile", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, badge_id, badge_tier, bonus_xp", "triggering_metric", 
         "string, string, string, integer", "badge_id valid; cannot award same badge tier twice", "Achievement Service", "Badges Earned, Achievement Velocity", "Confirmed"),

        ("EVT-ENG-06", "spin_started", "Daily Engagement", "User clicks spin button on lucky wheel", "Emitted upon RNG ticket deduction and wheel animation start", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, spin_id, spin_type, ticket_cost", "session_id", 
         "string, string, string, integer", "ticket_cost >= 0; user balance >= cost", "Wheel Service", "Spin Volume, Wheel Participation Rate", "Confirmed"),

        ("EVT-ENG-07", "spin_completed", "Daily Engagement", "Wheel lands on wedge; outcome finalized", "Emitted when prize outcome is verified and committed", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "user_id, spin_id, prize_type, prize_value, rng_hash", "reward_unit", 
         "string, string, string, decimal, string", "prize_value >= 0; rng_hash verifiable", "Wheel Service", "Prize Distribution Variance, Spin ROI", "Confirmed"),

        # Referral Events (4)
        ("EVT-REF-01", "referral_created", "Referrals", "User generates unique invite code or link", "Tracks intent of existing user to share app", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "referral_id, referring_user_id, referral_code", "created_at", 
         "string, string, string", "referral_code matches user unique format", "Referral Service", "Referrals Created, Invites Sent per DAU", "Confirmed"),

        ("EVT-REF-02", "referral_registered", "Referrals", "Referee creates account using invite code", "Attribution event binding referee to referrer", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "referral_id, referring_user_id, referred_user_id, channel", "registration_ts", 
         "string, string, string, string", "referring_user_id != referred_user_id (no self-ref)", "Referral Service", "Referral Registration Conversion Rate", "Proposed"),

        ("EVT-REF-03", "referral_activated", "Referrals", "Referee reaches required activity threshold", "Referee completes qualification milestone (e.g. 50 XP)", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "referral_id, referring_user_id, referred_user_id, activation_ts", "points_earned", 
         "string, string, string, string", "activation_ts >= registration_ts", "Referral Service", "Referee Activation Rate", "Proposed"),

        ("EVT-REF-04", "referral_converted", "Referrals", "Commission credited to referrer after fraud check", "Final economic conversion of referral relationship", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "referral_id, referring_user_id, commission_amount, transaction_id", "unit", 
         "string, string, decimal, string", "commission_amount > 0; referee passed fraud check", "Wallet / Referral Service", "Referral Conversion Rate, Viral Coefficient (K)", "Proposed"),

        # Wallet Events (3)
        ("EVT-WAL-01", "wallet_transaction_created", "Wallet", "Balance mutation instruction queued in ledger", "Emitted at start of ACID double-entry transaction block", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "transaction_id, user_id, amount, unit, transaction_type, source", "reference_id", 
         "string, string, decimal, string, string, string", "transaction_id unique; unit in allowed currencies", "Wallet Microservice", "Wallet Transactions Initiated", "Proposed"),

        ("EVT-WAL-02", "wallet_transaction_completed", "Wallet", "ACID ledger transaction committed successfully", "Emitted when user balance ledger is updated", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "transaction_id, user_id, new_balance, amount, unit", "committed_at", 
         "string, string, decimal, decimal, string", "new_balance >= 0 (no unauthorized overdraft)", "Wallet Microservice", "Completed Wallet Transactions, Net Points Flow", "Proposed"),

        ("EVT-WAL-03", "wallet_transaction_reversed", "Wallet", "Ledger transaction reversed via offsetting entry", "Emitted when prior credit/debit is cancelled", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "transaction_id, original_txn_id, user_id, reversal_amount, reason", "authorized_by", 
         "string, string, string, decimal, string", "original_txn_id must exist in committed state", "Wallet Microservice", "Transaction Reversal Ratio", "Proposed"),

        # Withdrawal Events (5)
        ("EVT-WDL-01", "withdrawal_requested", "Withdrawals", "User submits payout form with payment address", "Funds frozen in wallet; payout record created in queue", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "withdrawal_id, user_id, requested_amount, payout_method, destination_hash", "fee_amount", 
         "string, string, decimal, string, string", "amount >= minimum_threshold; user balance >= amount", "Withdrawal Service", "Withdrawal Requests, Requested Volume", "Proposed"),

        ("EVT-WDL-02", "withdrawal_processing", "Withdrawals", "Payout batch transmitted to payment gateway partner", "Status transitions to processing; webhook listener active", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "withdrawal_id, gateway_name, gateway_batch_id, dispatched_ts", "destination_type", 
         "string, string, string, string", "gateway_batch_id not null; status was Requested", "Gateway Integration API", "Withdrawal Processing Queue", "Proposed"),

        ("EVT-WDL-03", "withdrawal_completed", "Withdrawals", "Gateway webhook confirms funds reached user account", "Permanent cash outflow finalized; escrow hold cleared", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "withdrawal_id, user_id, amount, payout_method, gateway_txn_id, latency_hours", "bank_ref", 
         "string, string, decimal, string, string, decimal", "gateway_txn_id present; latency_hours >= 0", "Payment Webhook Worker", "Completed Withdrawals, Disbursed Volume, Latency", "Proposed"),

        ("EVT-WDL-04", "withdrawal_rejected", "Withdrawals", "Payout request declined for fraud or bad details", "Funds unfrozen and returned to user balance", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "withdrawal_id, user_id, amount, rejection_reason, rejected_at", "rejection_code", 
         "string, string, decimal, string, string", "rejection_reason in allowed categories", "Risk Engine / Admin Tool", "Rejected Withdrawals, Rejection Rate", "Proposed"),

        ("EVT-WDL-05", "withdrawal_reversed", "Withdrawals", "Bank returns funds post-settlement or chargeback", "Offsetting ledger debit applied to user account", 
         "Required (user_id)", "UUIDv4 / EVT########", "ISO-8601 UTC", "Active", "withdrawal_id, user_id, amount, reversal_reason, banking_error_code", "cleared_ts", 
         "string, string, decimal, string, string", "must reference previously completed withdrawal", "Finance Reconciliation", "Reversed Withdrawals, Settlement Leakage", "Proposed")
    ]

    for row_idx, r in enumerate(events, 6):
        ws.row_dimensions[row_idx].height = 24
        is_zebra = (row_idx % 2 == 1)
        for col_idx, val in enumerate(r, 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            fill_override = None
            if col_idx == 16:  # Status
                if val == "Confirmed":
                    fill_override = STATUS_GREEN
                elif val == "Proposed":
                    fill_override = STATUS_BLUE
            apply_data_cell(cell, val, is_zebra=is_zebra, align="left" if col_idx in [2,4,5,10,11,14,15] else "center", fill_override=fill_override)

    autofit_columns(ws, 1, 16)
    os.makedirs("04_deliverables/deliverable_08_event_tracking_plan", exist_ok=True)
    out_path = "04_deliverables/deliverable_08_event_tracking_plan/Event_Tracking_Plan.xlsx"
    wb.save(out_path)
    print(f"[SUCCESS] Generated Deliverable 08 Excel: {out_path} ({len(events)} events)")

# ==============================================================================
# 2. DELIVERABLE 09: ENTERPRISE DATA DICTIONARY (EXCEL)
# ==============================================================================
def generate_data_dictionary():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data_Dictionary"
    ws.views.sheetView[0].showGridLines = True

    create_banner(
        ws,
        "VELOOP REWARDS — ENTERPRISE DATA DICTIONARY",
        "Deliverable 09 | 80+ Standardized Fields Across All Entities with Governance Rules (Work Package G)",
        max_col=12
    )

    headers = [
        "Entity", "Field Name", "Data Type", "Definition", "Example Value", 
        "Required?", "Allowed Values", "Validation Rule", "Source System", 
        "Sensitivity Tier", "Analytical Use", "Status"
    ]
    ws.row_dimensions[5].height = 28
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=5, column=col_idx)
        apply_header_style(cell, h, fill_color=NAVY_HEADER, font_size=10)

    # 80+ Meaningful Fields across 10 Core Entities
    fields = [
        # Entity: Users (16 fields)
        ("Users", "user_id", "VARCHAR(16)", "Unique immutable simulated user identifier", "VLUSR000001", "Yes", "VLUSR + 6 digits", "^VLUSR[0-9]{6}$; PK, Not Null", "Auth Microservice", "Internal", "Primary entity key; joins across all tables", "Confirmed"),
        ("Users", "email_hash", "CHAR(64)", "SHA-256 cryptographic hash of user email address", "e3b0c44298fc1c149afbf4c8996fb924...", "Yes", "64-char hex", "Valid SHA-256 string; Not Null", "Auth API / Ingestion", "Restricted", "Unique account deduplication without exposing PII", "Proposed"),
        ("Users", "account_created_at", "TIMESTAMP", "Exact UTC timestamp of user account registration", "2026-06-10 07:14:00", "Yes", "ISO-8601 UTC", "Cannot be in future; Not Null", "Auth Microservice", "Internal", "Cohort segmentation; user tenure calculations", "Confirmed"),
        ("Users", "account_status", "VARCHAR(20)", "Current operational state of user account", "Active", "Yes", "Active, Inactive, Suspended, Dormant, Banned", "Must match allowed enum", "Auth Service / Risk", "Internal", "Active user filtering; churn and fraud reporting", "Confirmed"),
        ("Users", "email_verification_status", "VARCHAR(15)", "State of user email ownership verification", "Verified", "Yes", "Verified, Pending, Failed", "Must match allowed enum", "Auth Microservice", "Internal", "Trust scoring; fraud risk filtering", "Confirmed"),
        ("Users", "onboarding_status", "VARCHAR(20)", "Completion status of new user onboarding flow", "Completed", "Yes", "Not_Started, In_Progress, Completed", "Must match allowed enum", "Client App / Auth", "Internal", "Onboarding funnel conversion analysis", "Confirmed"),
        ("Users", "account_created_via", "VARCHAR(30)", "Registration UX flow channel used by user", "Web Registration", "Yes", "Web, Android App, iOS App, Google OAuth", "Must match allowed enum", "Client App", "Internal", "Registration channel conversion efficiency", "Confirmed"),
        ("Users", "acquisition_source", "VARCHAR(50)", "Marketing attribution channel bringing user to app", "Organic Search", "Yes", "Organic, Direct, WhatsApp, Telegram, YouTube", "Must match allowed enum", "Attribution Service", "Internal", "Customer acquisition cost (CAC) and LTV by source", "Confirmed"),
        ("Users", "referral_code", "VARCHAR(16)", "User unique alphanumeric outbound invite code", "VL850800", "Yes", "VL + 6 digits", "^VL[0-9]{6}$; Unique per user", "Auth Microservice", "Internal", "Attribution mapping for outbound viral invites", "Confirmed"),
        ("Users", "primary_device", "VARCHAR(20)", "Primary hardware device category used by user", "Android", "Yes", "Android, iOS, Desktop Web, Mobile Web", "Must match allowed enum", "Client User-Agent", "Internal", "Hardware segmentation; OS-specific QA audits", "Confirmed"),
        ("Users", "platform", "VARCHAR(20)", "Application operating platform environment", "Web", "Yes", "Web, Mobile App", "Must match allowed enum", "Client User-Agent", "Internal", "Platform usage distribution", "Confirmed"),
        ("Users", "country", "VARCHAR(50)", "Country of residence derived from IP / profile", "India", "Yes", "Standard ISO country names", "Valid country name", "Geo-IP Lookup", "Internal", "Geographic market segmentation", "Confirmed"),
        ("Users", "state", "VARCHAR(50)", "State or province of user location", "Odisha", "No", "Standard state names", "Alpha string or Null", "Geo-IP / Profile", "Internal", "Regional performance and localization targeting", "Confirmed"),
        ("Users", "city", "VARCHAR(50)", "City of user location", "Bhubaneswar", "No", "Standard city names", "Alpha string or Null", "Geo-IP / Profile", "Internal", "Urban vs tier-2/tier-3 engagement profiling", "Confirmed"),
        ("Users", "age", "INTEGER", "User self-reported age in completed years", "28", "No", "13 to 100", "Integer >= 13 and <= 100", "User Profile Form", "Restricted", "Demographic age-bracket analysis", "Confirmed"),
        ("Users", "gender", "VARCHAR(25)", "User self-reported demographic gender", "Male", "No", "Male, Female, Non-binary, Prefer not to say", "Must match allowed enum", "User Profile Form", "Restricted", "Demographic balance analysis", "Confirmed"),

        # Entity: Sessions (8 fields)
        ("Sessions", "session_id", "VARCHAR(16)", "Unique contiguous session identifier", "SESS0000001", "Yes", "SESS + 7 digits", "^SESS[0-9]{7}$; PK, Not Null", "Client Telemetry SDK", "Internal", "Primary session key; binds events in session", "Confirmed"),
        ("Sessions", "user_id", "VARCHAR(16)", "Foreign key of session user", "VLUSR000001", "Yes", "Valid user_id", "FK to users(user_id); Not Null", "Client Telemetry SDK", "Internal", "Session per user aggregations", "Confirmed"),
        ("Sessions", "session_start", "TIMESTAMP", "Exact UTC start timestamp of session", "2026-08-11 10:30:01", "Yes", "ISO-8601 UTC", "Cannot be in future; Not Null", "Client Telemetry SDK", "Internal", "Session start timing and peak usage hours", "Confirmed"),
        ("Sessions", "session_end", "TIMESTAMP", "Exact UTC termination timestamp of session", "2026-08-11 10:30:46", "Yes", "ISO-8601 UTC", "Must be >= session_start", "Client Telemetry SDK", "Internal", "Session termination timing", "Confirmed"),
        ("Sessions", "session_duration_seconds", "INTEGER", "Total elapsed duration of session in seconds", "45", "Yes", "0 to 86400", "session_end - session_start", "Client Telemetry SDK", "Internal", "Average session duration; engagement depth", "Confirmed"),
        ("Sessions", "device", "VARCHAR(20)", "Device category for current session", "Android", "Yes", "Android, iOS, Desktop Web", "Must match allowed enum", "Client Telemetry SDK", "Internal", "Multi-device switching analysis", "Confirmed"),
        ("Sessions", "entry_point", "VARCHAR(50)", "Initial app screen loaded upon session start", "Help/Support", "Yes", "Dashboard, Daily Reward, Tasks, Wallet, etc.", "Must match allowed enum", "Client Navigation", "Internal", "Navigation entry-point attribution", "Confirmed"),
        ("Sessions", "exit_feature", "VARCHAR(50)", "Last feature screen viewed before session close", "CAPTCHA", "Yes", "Task Arena, Wallet, Spin, CAPTCHA, etc.", "Must match allowed enum", "Client Navigation", "Internal", "Drop-off and churn surface identification", "Confirmed"),

        # Entity: Feature_Events (10 fields)
        ("Feature_Events", "event_id", "VARCHAR(16)", "Unique identifier for every atomic telemetry event", "EVT00000001", "Yes", "EVT + 8 digits", "^EVT[0-9]{8}$; PK, Not Null", "Client / Ingestion API", "Internal", "Atomic event tracking and stream deduplication", "Confirmed"),
        ("Feature_Events", "session_id", "VARCHAR(16)", "Session during which event occurred", "SESS0000001", "Yes", "Valid session_id", "FK to sessions(session_id)", "Client Telemetry SDK", "Internal", "Session event stream aggregation", "Confirmed"),
        ("Feature_Events", "user_id", "VARCHAR(16)", "User who triggered the event", "VLUSR000001", "Yes", "Valid user_id", "FK to users(user_id)", "Client Telemetry SDK", "Internal", "User behavioral profiling", "Confirmed"),
        ("Feature_Events", "event_datetime", "TIMESTAMP", "Exact UTC timestamp of event emission", "2026-08-11 10:30:03", "Yes", "ISO-8601 UTC", "Must fall within session interval", "Client Telemetry SDK", "Internal", "Time-series behavioral trend analysis", "Confirmed"),
        ("Feature_Events", "feature_name", "VARCHAR(50)", "Product feature module generating the event", "Missions", "Yes", "18 Core Product Domains", "Must match approved feature list", "Client Telemetry SDK", "Internal", "Feature adoption and engagement distribution", "Confirmed"),
        ("Feature_Events", "event_name", "VARCHAR(50)", "Standardized atomic action name", "mission_viewed", "Yes", "[domain]_[action] format", "Must match Event Tracking Plan", "Client Telemetry SDK", "Internal", "Micro-funnel step conversion analysis", "Confirmed"),
        ("Feature_Events", "event_status", "VARCHAR(20)", "Execution outcome of the event", "Started", "Yes", "Started, Completed, Failed, Viewed", "Must match allowed enum", "Client Telemetry SDK", "Internal", "Action success vs failure tracking", "Confirmed"),
        ("Feature_Events", "sequence_number", "INTEGER", "Chronological order of event within session", "3", "Yes", "1 to 10000", "Integer >= 1; strictly ascending", "Client Telemetry SDK", "Internal", "Session clickstream sequence reconstruction", "Confirmed"),
        ("Feature_Events", "reward_related_flag", "VARCHAR(3)", "Indicates whether event mutates point balance", "Yes", "Yes", "Yes, No", "Enum: Yes, No", "Ingestion Parser", "Internal", "Filtering economy-impacting actions", "Confirmed"),
        ("Feature_Events", "xp_related_flag", "VARCHAR(3)", "Indicates whether event yields experience points", "Yes", "Yes", "Yes, No", "Enum: Yes, No", "Ingestion Parser", "Internal", "XP accrual source attribution", "Confirmed"),

        # Entity: Task_Activity (10 fields)
        ("Task_Activity", "activity_id", "VARCHAR(16)", "Unique execution instance of a task attempt", "ACT0000001", "Yes", "ACT + 7 digits", "^ACT[0-9]{7}$; PK, Not Null", "Task Engine API", "Internal", "Primary key for task execution tracking", "Confirmed"),
        ("Task_Activity", "user_id", "VARCHAR(16)", "User performing the task activity", "VLUSR000980", "Yes", "Valid user_id", "FK to users(user_id)", "Task Engine API", "Internal", "User task engagement aggregation", "Confirmed"),
        ("Task_Activity", "task_id", "VARCHAR(16)", "Identifier of task definition from catalog", "TASK0071", "Yes", "TASK + 4 digits", "^TASK[0-9]{4}$; FK to catalog", "Task Engine API", "Internal", "Task-level popularity and difficulty metrics", "Confirmed"),
        ("Task_Activity", "task_category", "VARCHAR(30)", "Operational genre of task", "Game", "Yes", "Ad, App, Survey, CAPTCHA, Social, Game", "Must match allowed enum", "Task Catalog", "Internal", "Category-level engagement and revenue analysis", "Confirmed"),
        ("Task_Activity", "task_viewed_at", "TIMESTAMP", "Timestamp when task card entered viewport", "2026-08-05 19:36:29", "Yes", "ISO-8601 UTC", "Must be <= task_started_at", "Client Telemetry SDK", "Internal", "Task discovery to start latency", "Confirmed"),
        ("Task_Activity", "task_started_at", "TIMESTAMP", "Timestamp when task execution began", "2026-08-05 19:38:50", "Yes", "ISO-8601 UTC", "Must be >= task_viewed_at", "Task Engine API", "Internal", "Task start baseline timestamp", "Confirmed"),
        ("Task_Activity", "task_completed_at", "TIMESTAMP", "Timestamp when task completion was reported", "2026-08-05 19:42:10", "No", "ISO-8601 UTC", "Must be >= task_started_at; Null if failed", "Task Engine API", "Internal", "Task completion duration and velocity", "Confirmed"),
        ("Task_Activity", "task_status", "VARCHAR(20)", "Final execution status of task attempt", "Failed", "Yes", "Completed, Abandoned, Failed, Pending", "Must match allowed enum", "Task Engine API", "Internal", "Task completion rate calculations", "Confirmed"),
        ("Task_Activity", "failure_reason", "VARCHAR(50)", "Root cause categorization for uncompleted tasks", "Task unavailable", "No", "Validation failed, Unavailable, Timeout, Exited", "Null if status is Completed", "Task Engine API", "Internal", "Task error diagnostics and partner debugging", "Confirmed"),
        ("Task_Activity", "reward_status", "VARCHAR(20)", "Status of reward disbursement for task", "Not Credited", "Yes", "Credited, Not Credited, Pending", "Must match allowed enum", "Wallet Service", "Internal", "Audit of task completion vs financial reward", "Confirmed"),

        # Entity: Rewards_Ledger (8 fields)
        ("Rewards_Ledger", "reward_id", "VARCHAR(16)", "Unique reward disbursement record key", "RWD0000001", "Yes", "RWD + 7 digits", "^RWD[0-9]{7}$; PK, Not Null", "Wallet Service", "Internal", "Disbursement transaction reconciliation", "Proposed"),
        ("Rewards_Ledger", "activity_id", "VARCHAR(16)", "Task activity that earned the reward", "ACT0000001", "No", "Valid activity_id", "FK to task_activity; Null for daily/spin", "Task Engine", "Internal", "Direct linkage between activity and payout", "Proposed"),
        ("Rewards_Ledger", "user_id", "VARCHAR(16)", "User receiving the reward credit", "VLUSR000001", "Yes", "Valid user_id", "FK to users(user_id)", "Wallet Service", "Internal", "User total earnings rollup", "Proposed"),
        ("Rewards_Ledger", "reward_source", "VARCHAR(30)", "Originating feature granting the reward", "Watch Ads", "Yes", "Task, Daily Check-In, Spin, Mining, Referral", "Must match allowed enum", "Wallet Service", "Internal", "Revenue and points inflation source breakdown", "Proposed"),
        ("Rewards_Ledger", "reward_amount", "DECIMAL(12,2)", "Numeric value of points/currency credited", "100.00", "Yes", "Positive decimal", "amount > 0; Not Null", "Wallet Service", "Internal", "Monetary and point volume calculations", "Proposed"),
        ("Rewards_Ledger", "reward_unit", "VARCHAR(10)", "Currency denomination of the reward", "XP", "Yes", "XP, GEMS, TOKENS, INR", "Must match allowed enum", "Wallet Service", "Internal", "Multi-currency economy tracking", "Proposed"),
        ("Rewards_Ledger", "disbursement_status", "VARCHAR(20)", "Financial status of disbursement", "Credited", "Yes", "Credited, Pending_Escrow, Reversed", "Must match allowed enum", "Wallet Service", "Internal", "Pending escrow vs realized liability audit", "Proposed"),
        ("Rewards_Ledger", "credited_at", "TIMESTAMP", "Exact timestamp when wallet was credited", "2026-08-11 10:31:00", "Yes", "ISO-8601 UTC", "Cannot be in future", "Wallet Service", "Internal", "Revenue recognition and disbursement timing", "Proposed"),

        # Entity: Wallet_Transactions (8 fields)
        ("Wallet_Transactions", "transaction_id", "VARCHAR(16)", "Immutable double-entry transaction key", "TXN00000001", "Yes", "TXN + 8 digits", "^TXN[0-9]{8}$; PK, Not Null", "Wallet Microservice", "Restricted", "ACID financial ledger auditing", "Proposed"),
        ("Wallet_Transactions", "user_id", "VARCHAR(16)", "Account holder whose balance is mutated", "VLUSR000001", "Yes", "Valid user_id", "FK to users(user_id)", "Wallet Microservice", "Internal", "User balance history reconstruction", "Proposed"),
        ("Wallet_Transactions", "timestamp", "TIMESTAMP", "Exact UTC timestamp of ledger commit", "2026-08-11 10:31:00", "Yes", "ISO-8601 UTC", "Cannot be in future", "Wallet Microservice", "Internal", "Chronological audit trail", "Proposed"),
        ("Wallet_Transactions", "transaction_type", "VARCHAR(25)", "Functional category of balance mutation", "Reward Credit", "Yes", "Reward Credit, Redemption, Reversal, Adjustment", "Must match allowed enum", "Wallet Microservice", "Internal", "Inflow vs outflow economic categorization", "Proposed"),
        ("Wallet_Transactions", "amount", "DECIMAL(12,2)", "Monetary or point magnitude of transaction", "100.00", "Yes", "Signed or positive decimal", "Non-zero decimal", "Wallet Microservice", "Internal", "Point circulation velocity and volume", "Proposed"),
        ("Wallet_Transactions", "unit", "VARCHAR(10)", "Currency unit of the balance transaction", "XP", "Yes", "XP, GEMS, TOKENS, INR", "Must match allowed enum", "Wallet Microservice", "Internal", "Multi-currency ledger segmentation", "Proposed"),
        ("Wallet_Transactions", "reference_id", "VARCHAR(32)", "External source entity identifier", "RWD0000001", "Yes", "Identifier string", "Points to reward, withdrawal, or ticket ID", "Wallet Microservice", "Internal", "Cross-system financial reconciliation", "Proposed"),
        ("Wallet_Transactions", "reversal_transaction_id", "VARCHAR(16)", "Self-referencing link if transaction is reversal", "TXN00000099", "No", "Valid transaction_id", "Null unless transaction_type == Reversal", "Wallet Microservice", "Internal", "Traceability of fraud clawbacks and reversals", "Proposed"),

        # Entity: Withdrawals (9 fields)
        ("Withdrawals", "withdrawal_id", "VARCHAR(16)", "Unique payout request identifier", "WDL0000001", "Yes", "WDL + 7 digits", "^WDL[0-9]{7}$; PK, Not Null", "Withdrawal Microservice", "Restricted", "Payout pipeline tracking and SLA management", "Proposed"),
        ("Withdrawals", "user_id", "VARCHAR(16)", "User requesting cash payout", "VLUSR000001", "Yes", "Valid user_id", "FK to users(user_id)", "Withdrawal Microservice", "Internal", "Payout frequency and volume per user", "Proposed"),
        ("Withdrawals", "requested_amount", "DECIMAL(10,2)", "Fiat amount requested for disbursement", "500.00", "Yes", "Positive decimal >= min_threshold", "amount >= 100.00", "Withdrawal Microservice", "Restricted", "Total requested payout volume", "Proposed"),
        ("Withdrawals", "payout_method", "VARCHAR(20)", "Payment rail selected for disbursement", "UPI", "Yes", "UPI, Paytm, Bank Transfer, PayPal", "Must match allowed enum", "Client Payout Form", "Internal", "Payment channel share and gateway cost analysis", "Proposed"),
        ("Withdrawals", "destination_hash", "CHAR(64)", "SHA-256 hash of payment address / VPA", "8f434346648f6b96df89ddd90e4...", "Yes", "64-char hex", "Valid SHA-256 string", "Client Payout Form", "Restricted", "Multi-account abuse and fraud ring detection", "Proposed"),
        ("Withdrawals", "requested_timestamp", "TIMESTAMP", "Time user submitted withdrawal form", "2026-08-15 14:22:00", "Yes", "ISO-8601 UTC", "Cannot be in future", "Withdrawal Microservice", "Internal", "SLA tracking starting timestamp", "Proposed"),
        ("Withdrawals", "final_timestamp", "TIMESTAMP", "Time withdrawal reached terminal state", "2026-08-15 16:45:00", "No", "ISO-8601 UTC", "Must be >= requested_timestamp", "Gateway Webhook", "Internal", "Fulfillment latency and processing duration", "Proposed"),
        ("Withdrawals", "status", "VARCHAR(20)", "Operational status of payout request", "Completed", "Yes", "Requested, Under_Review, Processing, Completed, Rejected", "Must match allowed enum", "Withdrawal Service", "Internal", "Withdrawal completion rate and queue depth", "Proposed"),
        ("Withdrawals", "rejection_reason", "VARCHAR(50)", "Root cause if payout was declined", "Invalid Payment Address", "No", "Invalid Address, Min Balance, Fraud Flag", "Null if status is Completed", "Risk Engine / Gateway", "Internal", "Payout failure and rejection diagnostics", "Proposed"),

        # Entity: Referrals (7 fields)
        ("Referrals", "referral_id", "VARCHAR(16)", "Unique referral relationship identifier", "REF00000001", "Yes", "REF + 8 digits", "^REF[0-9]{8}$; PK, Not Null", "Referral Service", "Internal", "Primary referral attribution key", "Proposed"),
        ("Referrals", "referring_user_id", "VARCHAR(16)", "Existing user who generated the invite", "VLUSR000120", "Yes", "Valid user_id", "FK to users(user_id)", "Referral Service", "Internal", "Referrer performance and virality index", "Proposed"),
        ("Referrals", "referred_user_id", "VARCHAR(16)", "New user created via the invite", "VLUSR000850", "Yes", "Valid user_id", "FK to users(user_id); Unique", "Auth / Referral Service", "Internal", "Attribution of referee cohort quality", "Proposed"),
        ("Referrals", "registration_timestamp", "TIMESTAMP", "Time referee completed registration", "2026-08-01 11:20:00", "Yes", "ISO-8601 UTC", "Matches user account creation", "Auth Microservice", "Internal", "Viral loop conversion latency", "Proposed"),
        ("Referrals", "activation_timestamp", "TIMESTAMP", "Time referee completed qualification milestone", "2026-08-01 14:10:00", "No", "ISO-8601 UTC", "Must be >= registration_timestamp", "Referral Service", "Internal", "Time-to-activation and referral ROI", "Proposed"),
        ("Referrals", "referral_status", "VARCHAR(20)", "Current state of referral lifecycle", "Converted", "Yes", "Created, Registered, Activated, Converted, Rejected", "Must match allowed enum", "Referral Service", "Internal", "Referral conversion funnel metrics", "Proposed"),
        ("Referrals", "commission_amount", "DECIMAL(10,2)", "Commission reward credited to referrer", "50.00", "No", "Non-negative decimal", "Null until Converted; amount >= 0", "Wallet Service", "Internal", "Referral program CAC and payout liability", "Proposed"),

        # Entity: Daily_Activity (5 fields)
        ("Daily_Activity", "user_id", "VARCHAR(16)", "User whose daily behavior is summarized", "VLUSR000001", "Yes", "Valid user_id", "Composite PK (user_id, activity_date)", "Daily ETL Aggregator", "Internal", "User daily activity time-series", "Confirmed"),
        ("Daily_Activity", "activity_date", "DATE", "Calendar date of aggregated activity", "2026-08-11", "Yes", "YYYY-MM-DD", "Composite PK; Valid calendar date", "Daily ETL Aggregator", "Internal", "Daily active user cohorting", "Confirmed"),
        ("Daily_Activity", "session_count", "INTEGER", "Number of distinct sessions on date", "1", "Yes", ">= 0", "Non-negative integer", "Daily ETL Aggregator", "Internal", "Daily user visit frequency", "Confirmed"),
        ("Daily_Activity", "completed_task_count", "INTEGER", "Number of tasks completed on date", "2", "Yes", ">= 0", "Non-negative integer", "Daily ETL Aggregator", "Internal", "Daily earning engagement depth", "Confirmed"),
        ("Daily_Activity", "active_flag", "VARCHAR(3)", "Flags whether user met DAU qualification rules", "Yes", "Yes", "Yes, No", "Enum: Yes, No", "Daily ETL Aggregator", "Internal", "Official DAU reporting flag", "Confirmed")
    ]

    for row_idx, r in enumerate(fields, 6):
        ws.row_dimensions[row_idx].height = 24
        is_zebra = (row_idx % 2 == 1)
        for col_idx, val in enumerate(r, 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            fill_override = None
            if col_idx == 12:  # Status
                if val == "Confirmed":
                    fill_override = STATUS_GREEN
                elif val == "Proposed":
                    fill_override = STATUS_BLUE
            elif col_idx == 10:  # Sensitivity
                if val == "Restricted":
                    fill_override = STATUS_RED
                elif val == "Internal":
                    fill_override = STATUS_YELLOW
            apply_data_cell(cell, val, is_zebra=is_zebra, align="left" if col_idx in [2,4,5,7,8,11] else "center", fill_override=fill_override)

    autofit_columns(ws, 1, 12)
    os.makedirs("04_deliverables/deliverable_09_data_dictionary", exist_ok=True)
    out_path = "04_deliverables/deliverable_09_data_dictionary/Data_Dictionary.xlsx"
    wb.save(out_path)
    print(f"[SUCCESS] Generated Deliverable 09 Excel: {out_path} ({len(fields)} fields)")

# ==============================================================================
# 3. DELIVERABLE 11: KPI CATALOGUE (EXCEL)
# ==============================================================================
def generate_kpi_catalogue():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "KPI_Catalogue"
    ws.views.sheetView[0].showGridLines = True

    create_banner(
        ws,
        "VELOOP REWARDS — ENTERPRISE KPI CATALOGUE",
        "Deliverable 11 | 35+ Standardized Production KPIs Across 7 Core Domains (Work Package I)",
        max_col=11
    )

    headers = [
        "KPI ID", "Domain", "KPI Name", "Technical Definition", "Exact Mathematical Formula", 
        "Required Fields", "Data Source", "Frequency", "Stakeholder", "Business Purpose & Interpretation", "Status"
    ]
    ws.row_dimensions[5].height = 28
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=5, column=col_idx)
        apply_header_style(cell, h, fill_color=NAVY_HEADER, font_size=10)

    # 35+ Standardized Production KPIs across 7 Domains
    kpis = [
        # User KPIs (5)
        ("KPI-USR-01", "User", "Daily Active Users (DAU)", "Unique users generating a qualifying value event within a calendar day", 
         "DAU = Count(Distinct user_id WHERE qualifying_event = TRUE)", "user_id, event_datetime, event_name", "Feature_Events / Daily_Activity", "Daily", "Executive / Product", 
         "Measures daily active product demand. Must exclude passive app opens or background events.", "Confirmed"),

        ("KPI-USR-02", "User", "Monthly Active Users (MAU)", "Unique users generating a qualifying value event in rolling 30-day window", 
         "MAU = Count(Distinct user_id WHERE event_date >= T - 30d)", "user_id, activity_date, active_flag", "Daily_Activity", "Monthly", "Executive / Growth", 
         "Evaluates overall active addressable audience and platform reach.", "Confirmed"),

        ("KPI-USR-03", "User", "Product Stickiness Ratio", "Proportion of monthly active users who return on an average day", 
         "Stickiness = (DAU / MAU) * 100%", "DAU, MAU", "Calculated KPI", "Daily / Weekly", "Product Management", 
         "High stickiness (>20%) indicates habitual daily utility; key predictor of retention.", "Confirmed"),

        ("KPI-USR-04", "User", "Day-30 Cohort Retention Rate", "Percentage of new users who remain active 30 days after registration", 
         "D30 Retention = (Active Users on Day 30 / Initial Cohort Registrations) * 100%", "account_created_at, activity_date, user_id", "Users, Daily_Activity", "Monthly", "Growth / Product", 
         "Measures long-term product-market fit and user lifecycle sustainability.", "Confirmed"),

        ("KPI-USR-05", "User", "Account Inactivity / Churn Rate", "Proportion of previously active users with no activity in >= 30 days", 
         "Churn Rate = (Users Inactive >= 30d / Total Cumulative Active Users) * 100%", "last_activity_datetime, account_status", "Users", "Monthly", "Retention Lead", 
         "Identifies audience attrition requiring automated win-back push campaigns.", "Confirmed"),

        # Engagement KPIs (6)
        ("KPI-ENG-01", "Engagement", "Feature Adoption Rate", "Proportion of active users who interact with a specific feature", 
         "Adoption_f = (Unique Users Using Feature f / Total DAU) * 100%", "user_id, feature_name, event_datetime", "Feature_Events, Users", "Weekly", "Product / Design", 
         "Identifies under-adopted features needing UI discovery optimization.", "Confirmed"),

        ("KPI-ENG-02", "Engagement", "Task Starts Volume", "Total number of task execution attempts initiated by users", 
         "Task Starts = Count(activity_id WHERE event = 'task_started')", "activity_id, task_started_at", "Task_Activity", "Daily", "Operations / Product", 
         "Measures top-of-funnel earning demand and partner offer click velocity.", "Confirmed"),

        ("KPI-ENG-03", "Engagement", "Task Completion Rate", "Percentage of started tasks that successfully reach completed status", 
         "Completion Rate = (Completed Tasks / Total Started Tasks) * 100%", "task_status, activity_id", "Task_Activity", "Daily / Weekly", "Operations / Partnerships", 
         "Reflects task UX friction, technical partner stability, and completion drop-off.", "Confirmed"),

        ("KPI-ENG-04", "Engagement", "Repeat Feature Usage Ratio", "Average number of distinct sessions using a feature per adopting user", 
         "Repeat Usage = Sessions with Feature / Unique Users with Feature", "session_id, user_id, feature_name", "Feature_Usage", "Weekly", "Product Analytics", 
         "Differentiates novelty one-off clicks from deeply retained daily habits.", "Confirmed"),

        ("KPI-ENG-05", "Engagement", "Daily Activity Breadth Score", "Average number of distinct features engaged with per active user day", 
         "Breadth Score = Mean(Distinct feature_count per user per day)", "feature_count, user_id, activity_date", "Daily_Activity", "Weekly", "Product Team", 
         "Users engaging with >= 3 features exhibit significantly higher lifetime retention.", "Confirmed"),

        ("KPI-ENG-06", "Engagement", "Average Session Duration", "Mean time elapsed between session start and session termination", 
         "Avg Duration = Sum(session_duration_seconds) / Total Sessions", "session_duration_seconds, session_id", "Sessions", "Daily", "Product / UX", 
         "Measures engagement depth; must be paired with task completions to avoid inflating idle time.", "Confirmed"),

        # Reward KPIs (5)
        ("KPI-RWD-01", "Rewards", "Daily Reward Credit Volume", "Total points/XP credited to users from all earning features combined", 
         "Credit Volume = Sum(reward_amount WHERE status = 'Credited')", "reward_amount, disbursement_status", "Rewards_Ledger", "Daily", "Finance / Economy", 
         "Monitors total platform points inflation and user earning velocity.", "Confirmed"),

        ("KPI-RWD-02", "Rewards", "Reward Crediting Fulfillment Rate", "Percentage of completed earning tasks that successfully receive reward credit", 
         "Fulfillment Rate = (Rewards Credited / Tasks Completed) * 100%", "reward_status, task_status", "Task_Activity", "Daily", "Engineering / QA", 
         "SLA monitoring metric: discrepancies reveal partner postback or ledger drops.", "Confirmed"),

        ("KPI-RWD-03", "Rewards", "Reward Reversal Ratio", "Proportion of credited rewards that are subsequently revoked for fraud", 
         "Reversal Ratio = (Reversed Reward Amount / Total Credited Amount) * 100%", "clawback_amount, reward_amount", "Rewards_Ledger", "Monthly", "Risk / Fraud", 
         "Evaluates partner chargeback liability and anti-fraud clawback efficiency.", "Proposed"),

        ("KPI-RWD-04", "Rewards", "Average Reward per Active User", "Mean daily points/XP earned per active user", 
         "Avg Reward = Total Points Credited / DAU", "reward_amount, user_id, activity_date", "Rewards_Ledger, Daily_Activity", "Daily", "Product Economy", 
         "Core economy balance metric: prevents runaway inflation while maintaining user motivation.", "Confirmed"),

        ("KPI-RWD-05", "Rewards", "Reward Contribution by Feature", "Percentage breakdown of total reward points distributed across features", 
         "Share_f = (Points from Feature f / Total Points Distributed) * 100%", "reward_amount, reward_source", "Rewards_Ledger", "Weekly", "Game Economy Lead", 
         "Reveals economic dependency on specific ad networks, surveys, or games.", "Confirmed"),

        # Wallet KPIs (4)
        ("KPI-WAL-01", "Wallet", "Total Circulating Points Balance", "Aggregate outstanding unredeemed platform points held by all users", 
         "Circulating Points = Sum(xp_balance across all users)", "xp_balance, account_status", "Users", "Daily", "Finance / Treasury", 
         "Represents future platform redemption liability; vital for liquidity planning.", "Confirmed"),

        ("KPI-WAL-02", "Wallet", "Net Currency Velocity", "Ratio of points earned (credits) to points redeemed or withdrawn (debits)", 
         "Point Velocity = Total Credits / Total Debits", "amount, transaction_type", "Wallet_Transactions", "Monthly", "CFO / Finance", 
         "Velocity > 1.0 indicates point accumulation; Velocity < 1.0 indicates capital outflow.", "Proposed"),

        ("KPI-WAL-03", "Wallet", "Wallet Transaction Volume", "Total number of atomic balance ledger movements committed", 
         "Txn Volume = Count(transaction_id WHERE status = 'Committed')", "transaction_id, status", "Wallet_Transactions", "Daily", "Engineering / DB", 
         "Database write load and transactional throughput indicator.", "Proposed"),

        ("KPI-WAL-04", "Wallet", "Escrow Hold Ratio", "Proportion of user point balances held in pending escrow verification", 
         "Escrow Ratio = (Points in Pending Escrow / Total Wallet Points) * 100%", "reward_amount, disbursement_status", "Rewards_Ledger", "Weekly", "Risk / Operations", 
         "Measures anti-fraud holding friction on user balances.", "Proposed"),

        # Withdrawal KPIs (6)
        ("KPI-WDL-01", "Withdrawals", "Withdrawal Requests Count", "Total number of withdrawal requests submitted by users", 
         "Requests = Count(withdrawal_id WHERE event = 'withdrawal_requested')", "withdrawal_id, requested_timestamp", "Withdrawals", "Daily", "Operations / Finance", 
         "Measures cash payout demand and customer service queue workload.", "Proposed"),

        ("KPI-WDL-02", "Withdrawals", "Completed Withdrawals Count", "Total number of withdrawal requests successfully settled in bank accounts", 
         "Completed = Count(withdrawal_id WHERE status = 'Completed')", "withdrawal_id, status", "Withdrawals", "Daily", "Finance / Leadership", 
         "Primary trust metric: users receiving verified cash payouts.", "Proposed"),

        ("KPI-WDL-03", "Withdrawals", "Withdrawal Fulfillment Rate", "Percentage of submitted withdrawals that reach completed status", 
         "Fulfillment Rate = (Completed / (Completed + Rejected + Reversed)) * 100%", "withdrawal_id, status", "Withdrawals", "Weekly", "Finance / Product", 
         "Measures end-to-end payment gateway and anti-fraud approval efficiency.", "Proposed"),

        ("KPI-WDL-04", "Withdrawals", "Average Payout Latency (Hours)", "Median elapsed duration from withdrawal submission to bank settlement", 
         "Payout Latency = Median(final_timestamp - requested_timestamp in hours)", "requested_timestamp, final_timestamp, status", "Withdrawals", "Daily", "Operations / UX", 
         "Key driver of user NPS and reviews; target SLA is < 24 hours.", "Proposed"),

        ("KPI-WDL-05", "Withdrawals", "Total Cash Disbursed Volume", "Total fiat monetary value settled and paid out to users", 
         "Disbursed Volume = Sum(requested_amount WHERE status = 'Completed')", "requested_amount, status", "Withdrawals", "Daily / Monthly", "CFO / Finance", 
         "Cash expenditure tracking against ad revenue receipts.", "Proposed"),

        ("KPI-WDL-06", "Withdrawals", "Withdrawal Method Distribution", "Percentage breakdown of payouts across UPI, Paytm, Bank, and PayPal", 
         "Method Share = (Withdrawals via Method m / Total Completed) * 100%", "payout_method, withdrawal_id", "Withdrawals", "Monthly", "Treasury / Ops", 
         "Guides payment gateway negotiations and fee optimization.", "Proposed"),

        # Referral KPIs (5)
        ("KPI-REF-01", "Referrals", "Referral Invites Generated", "Total outbound referral links or share intents created by users", 
         "Invites Generated = Count(referral_id WHERE event = 'referral_created')", "referral_id, creation_timestamp", "Referrals", "Daily", "Growth Team", 
         "Measures user intent to advocate and promote platform to personal network.", "Confirmed"),

        ("KPI-REF-02", "Referrals", "Referral Registration Conversion", "Percentage of shared referral invites that result in a registered account", 
         "Reg Conversion = (Referred Registrations / Invites Shared) * 100%", "referral_id, referral_status", "Referrals", "Weekly", "Growth / Marketing", 
         "Evaluates viral landing page and onboarding conversion appeal.", "Proposed"),

        ("KPI-REF-03", "Referrals", "Referee Activation Rate", "Percentage of registered referees who achieve qualification activity", 
         "Activation Rate = (Activated Referees / Registered Referees) * 100%", "referral_id, referral_status", "Referrals", "Weekly", "Growth / Product", 
         "Distinguishes empty bot registrations from genuine active referred users.", "Proposed"),

        ("KPI-REF-04", "Referrals", "Viral Coefficient (K-factor)", "Number of newly converted users generated by each existing active user", 
         "K = (Invites per User) * (Registration Rate) * (Activation Rate)", "referrals_shared, registrations, activations, DAU", "Calculated KPI", "Monthly", "Growth Lead / CEO", 
         "K > 1.0 achieves viral self-sustaining loop; K < 1.0 requires external acquisition.", "Proposed"),

        ("KPI-REF-05", "Referrals", "Referral Retention Uplift", "Relative difference in 30-day retention between referred and organic users", 
         "Retention Uplift = Retention(Referred) - Retention(Organic)", "user_id, acquisition_source, activity_date", "Users, Daily_Activity", "Monthly", "Growth Analytics", 
         "Quantifies cohort quality premium of socially acquired users.", "Proposed"),

        # Support & Content KPIs (4)
        ("KPI-SUP-01", "Support", "Support Ticket Submission Rate", "Total customer service inquiries submitted per 1,000 active users", 
         "Ticket Rate = (Support Tickets Submitted / DAU) * 1000", "ticket_id, user_id, DAU", "Support System", "Weekly", "Customer Support", 
         "Product friction barometer; spikes indicate broken tasks or delayed withdrawals.", "Proposed"),

        ("KPI-SUP-02", "Support", "Help Center Search Deflection Rate", "Percentage of help center visits resolved without submitting a ticket", 
         "Deflection Rate = ((Help Center Visits - Tickets Submitted) / Visits) * 100%", "session_id, entry_point, ticket_id", "Sessions, Support", "Monthly", "Support Operations", 
         "Measures self-service efficacy of FAQ and knowledge base documentation.", "Proposed"),

        ("KPI-SUP-03", "Support", "Inquiry Distribution by Category", "Breakdown of support tickets across Withdrawal, Task, and Account issues", 
         "Category Share = (Tickets in Category c / Total Tickets) * 100%", "ticket_id, issue_category", "Support System", "Weekly", "Product / Support", 
         "Prioritizes engineering bug fixes based on actual user friction volume.", "Proposed"),

        ("KPI-SUP-04", "Support", "Median Ticket Resolution Time (Hours)", "Median elapsed hours from ticket submission to verified user resolution", 
         "Resolution Time = Median(resolved_timestamp - submitted_timestamp in hours)", "submitted_ts, resolved_ts", "Support System", "Weekly", "Support Lead", 
         "Core operational SLA for customer satisfaction and retention.", "Proposed")
    ]

    for row_idx, r in enumerate(kpis, 6):
        ws.row_dimensions[row_idx].height = 24
        is_zebra = (row_idx % 2 == 1)
        for col_idx, val in enumerate(r, 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            fill_override = None
            if col_idx == 11:  # Status
                if val == "Confirmed":
                    fill_override = STATUS_GREEN
                elif val == "Proposed":
                    fill_override = STATUS_BLUE
            apply_data_cell(cell, val, is_zebra=is_zebra, align="left" if col_idx in [3,4,5,6,10] else "center", fill_override=fill_override)

    autofit_columns(ws, 1, 11)
    os.makedirs("04_deliverables/deliverable_11_kpi_catalogue", exist_ok=True)
    out_path = "04_deliverables/deliverable_11_kpi_catalogue/KPI_Catalogue.xlsx"
    wb.save(out_path)
    print(f"[SUCCESS] Generated Deliverable 11 Excel: {out_path} ({len(kpis)} KPIs)")

if __name__ == "__main__":
    generate_event_tracking_plan()
    generate_data_dictionary()
    generate_kpi_catalogue()

