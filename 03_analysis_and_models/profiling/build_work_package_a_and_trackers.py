"""
VELOOP REWARDS — WORK PACKAGE A & INITIAL TRACKERS GENERATOR
Generates:
1. Deliverable 03: Data Coverage Matrix (Excel)
2. Deliverable 19: Source & Verification Register (Excel)
3. Deliverable 02: Product Data Readiness Audit (Markdown)
4. Requirements & Deliverables Tracker (Markdown)
5. Phased Implementation Plan (Markdown)
6. Missing Dependencies & Source Register (Markdown)
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

# Status colors
STATUS_GREEN = "D4EDDA"
STATUS_YELLOW = "FFF3CD"
STATUS_RED = "F8D7DA"
STATUS_BLUE = "CCE5FF"

def apply_header_style(cell, text, fill_color=NAVY_HEADER, font_size=11, font_color=WHITE, bold=True):
    cell.value = text
    cell.font = Font(name="Calibri", size=font_size, bold=bold, color=font_color)
    cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

def apply_data_cell(cell, value, is_zebra=False, align="left", bold=False, font_size=10, fill_override=None):
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

def create_banner(ws, title, subtitle):
    ws.merge_cells("A1:G1")
    banner_cell = ws["A1"]
    banner_cell.value = title
    banner_cell.font = Font(name="Calibri", size=14, bold=True, color=WHITE)
    banner_cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    banner_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    ws.merge_cells("A2:G2")
    sub_cell = ws["A2"]
    sub_cell.value = subtitle
    sub_cell.font = Font(name="Calibri", size=10, italic=True, color="CCCCCC")
    sub_cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    sub_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 20

    ws.merge_cells("A3:G3")
    disclaimer_cell = ws["A3"]
    disclaimer_cell.value = "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING | VELOOP REWARDS DATA ANALYST INTERNSHIP"
    disclaimer_cell.font = Font(name="Calibri", size=9, bold=True, color="856404")
    disclaimer_cell.fill = PatternFill(start_color=STATUS_YELLOW, end_color=STATUS_YELLOW, fill_type="solid")
    disclaimer_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[3].height = 18

def autofit_columns(ws, min_col=1, max_col=None, padding=3):
    if max_col is None:
        max_col = ws.max_column
    for col in range(min_col, max_col + 1):
        max_len = 0
        col_letter = get_column_letter(col)
        for row in range(4, ws.max_row + 1):
            val = ws.cell(row=row, column=col).value
            if val is not None:
                lines = str(val).split("\n")
                line_max = max(len(l) for l in lines)
                max_len = max(max_len, line_max)
        ws.column_dimensions[col_letter].width = max(max_len + padding, 12)

# ==============================================================================
# 1. BUILD DELIVERABLE 03: DATA COVERAGE MATRIX EXCEL
# ==============================================================================
def generate_data_coverage_matrix():
    wb = openpyxl.Workbook()
    ws_cov = wb.active
    ws_cov.title = "Data_Coverage_Matrix"
    ws_cov.views.sheetView[0].showGridLines = True

    create_banner(
        ws_cov, 
        "VELOOP REWARDS — PRODUCT DATA READINESS & COVERAGE MATRIX",
        "Deliverable 03 | Comprehensive Coverage Across 18 Core Product Domains & 32 Features"
    )

    headers = [
        "Product Area", "Feature / Component", "User Action", "System Outcome", 
        "Data Required", "Business Question", "Telemetry Coverage", 
        "Supplied Dataset Coverage", "Evidentiary Tier", "Readiness Status"
    ]
    ws_cov.merge_cells("A1:J1")
    ws_cov.merge_cells("A2:J2")
    ws_cov.merge_cells("A3:J3")
    
    ws_cov.row_dimensions[5].height = 28
    for col_idx, h in enumerate(headers, 1):
        cell = ws_cov.cell(row=5, column=col_idx)
        apply_header_style(cell, h, fill_color=NAVY_HEADER, font_size=10)

    # 18 Product Domains with 32 Granular Features
    rows_data = [
        # 1. Registration
        ("Registration", "Account Sign-Up", "Submits registration form via email/social", "Creates user record, sets status to pending/verified", 
         "user_id, email, auth_method, timestamp, device_id", "What is the primary acquisition channel and sign-up conversion rate?", 
         "Missing stream (user_registered event absent)", "Available in Users_1000_Clean (static profile)", "Simulated", "Partial Readiness"),
        ("Registration", "Email Verification", "Clicks email verification link / enters OTP", "Updates email_verification_status to Verified", 
         "user_id, otp_timestamp, verification_latency_sec", "What percentage of users verify email within 24h?", 
         "Missing stream (verification event absent)", "Available in Users_1000_Clean (status flag)", "Simulated", "Partial Readiness"),
        
        # 2. Login
        ("Login", "User Authentication", "Enters credentials or OAuth token", "Validates session, issues JWT, logs session", 
         "user_id, session_id, login_timestamp, ip_hash, platform", "What is our DAU/MAU ratio and login frequency?", 
         "Present in Sessions sheet (7,913 rows)", "Present in 02_Sessions & 04_Daily_Activity", "Simulated", "Production Ready"),
        ("Login", "Session Termination", "Logs out or session expires after inactivity", "Closes session, calculates duration", 
         "session_id, session_end, session_duration_seconds", "What is average session length and bounce rate?", 
         "Present in Sessions sheet (session_end, duration)", "Present in 02_Sessions", "Simulated", "Production Ready"),
        
        # 3. Watch Ads
        ("Watch Ads", "Ad Impression / Start", "Clicks 'Watch Ad' button", "Calls ad network SDK, initializes video playback", 
         "event_id, user_id, ad_network_id, ad_unit_id, timestamp", "How many ad views are initiated per DAU?", 
         "Present in Feature_Events (ad_started: 1,007)", "Present in 03_Feature_Events & Feature_Usage", "Simulated", "Production Ready"),
        ("Watch Ads", "Ad Completion", "Watches full rewarded video", "Verifies callback from ad network, credits XP/Coins", 
         "event_id, user_id, completion_rate, reward_credited_flag", "What is the ad completion rate and cost-per-completion?", 
         "Present in Feature_Events (ad_completed: 1,054)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),
        ("Watch Ads", "Ad Skipped / Abandoned", "Closes ad before completion threshold", "Discards reward, logs drop-off timestamp", 
         "event_id, user_id, elapsed_seconds, skip_reason", "At what point in the video do users abandon?", 
         "Present in Feature_Events (ad_skipped: 1,065)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),

        # 4. Daily Rewards
        ("Daily Rewards", "Reward Inspection", "Opens daily check-in screen", "Displays 7-day reward calendar and claim status", 
         "user_id, streak_day_number, available_reward_val", "What percentage of active users check daily reward?", 
         "Present in Feature_Events (daily_reward_viewed: 1,218)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),
        ("Daily Rewards", "Reward Claim", "Clicks 'Claim Reward'", "Validates 24h eligibility, credits balance, updates streak", 
         "user_id, claim_datetime, streak_day, reward_unit, reward_amount", "Does daily reward claiming improve D7 retention?", 
         "Present in Feature_Events (daily_reward_claimed: 1,281)", "Present in 03_Feature_Events & 04_Daily_Activity", "Simulated", "Production Ready"),

        # 5. Tap & Earn
        ("Tap & Earn", "Tap Session Start", "Initiates tapping energy meter", "Loads tap mechanics, validates client integrity", 
         "user_id, session_id, initial_energy_level", "What is the user adoption rate of tap mechanics?", 
         "Present in Feature_Events (tap_started: 1,327)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),
        ("Tap & Earn", "Tap Batch Submission", "Submits accumulated taps upon cooldown/exit", "Server validates tap rate, prevents autoclicker, credits points", 
         "user_id, tap_count, duration_sec, taps_per_sec, reward_awarded", "What proportion of tap sessions exhibit bot-like behavior?", 
         "Present in Feature_Events (tap_completed: 1,327)", "Present in 03_Feature_Events (lacks tap_count payload)", "Simulated", "Partial Readiness"),

        # 6. Mining
        ("Mining", "Mining Rig Activation", "Clicks 'Start Mining' (time-based yield)", "Starts background countdown timer (e.g. 8h cycle)", 
         "user_id, mining_start_time, target_yield, rig_level", "How many users maintain active mining sessions continuously?", 
         "Present in Feature_Events (mining_started: 882)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),
        ("Mining", "Yield Collection & Stop", "Collects mined tokens when cycle finishes", "Calculates yield, credits wallet, halts mining process", 
         "user_id, stop_time, total_mined_tokens, cycle_duration_hours", "What is the token emission rate from passive mining?", 
         "Present in Feature_Events (mining_stopped: 915, activity: 819)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),

        # 7. Spin
        ("Spin", "Wheel Inspection / Opened", "Opens lucky wheel interface", "Checks available free spins vs ticket cost", 
         "user_id, available_spins, last_free_spin_time", "How frequently do users visit the lucky wheel?", 
         "Present in Feature_Events (spin_opened: 798)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),
        ("Spin", "Wheel Execution", "Clicks spin button", "Server generates RNG outcome, animates wheel, awards prize", 
         "user_id, spin_id, prize_type, prize_amount, rng_seed_hash", "Is prize distribution adhering to configured probabilities?", 
         "Present in Feature_Events (spin_started: 801, completed: 826)", "Present in 03_Feature_Events (lacks prize details payload)", "Simulated", "Partial Readiness"),

        # 8. Missions
        ("Missions", "Mission Exploration", "Views active mission list", "Fetches progress against mission objectives", 
         "user_id, mission_category, active_mission_count", "Which mission types attract the highest engagement?", 
         "Present in Feature_Events (mission_viewed: 685)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),
        ("Missions", "Mission Execution & Completion", "Starts and finishes mission criteria", "Validates completion conditions, issues mission badge/points", 
         "user_id, mission_id, start_time, complete_time, reward_xp", "What is the mission completion funnel and drop-off rate?", 
         "Present in Feature_Events (started: 694, completed: 702, abandoned: 699)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),

        # 9. Referrals
        ("Referrals", "Referral Link Generation & Share", "Generates unique code / clicks share to social", "Generates referral URL, tracks share intent", 
         "user_id, referral_code, share_channel (WhatsApp/FB/Telegram)", "Which social channel generates highest referral shares?", 
         "Present in Feature_Events (created: 871, shared: 834, viewed: 816)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),
        ("Referrals", "Referred User Conversion & Attribution", "New user signs up and meets activation criteria", "Links referee to referrer, calculates commission, credits bonus", 
         "referral_id, referrer_id, referee_id, registration_time, activation_time, commission_amount", "What is true viral coefficient (K-factor) and referral conversion rate?", 
         "Missing relational stream (no referee-referrer conversion link)", "Only static source in Users table ('WhatsApp')", "To Be Verified", "Critical Gap"),

        # 10. Wallet
        ("Wallet", "Balance & Transaction Inspection", "Opens wallet dashboard", "Queries balance ledger across XP, Gems, Cash", 
         "user_id, timestamp, total_xp, total_gems, cash_balance", "How often do users check their balance relative to withdrawal?", 
         "Present in Feature_Events (wallet_viewed: 2,172)", "Present in 03_Feature_Events", "Simulated", "Partial Readiness"),
        ("Wallet", "Transaction Ledger Record", "System credits or debits points/cash", "Creates immutable double-entry ledger record", 
         "transaction_id, user_id, amount, currency_unit, transaction_type, reference_id, status", "What is the daily net inflow/outflow of platform points?", 
         "Missing standalone transaction ledger dataset", "Only aggregate xp_balance in Users table", "To Be Verified", "Critical Gap"),

        # 11. Withdrawals
        ("Withdrawals", "Withdrawal Request Submission", "Selects payout method, enters details and amount", "Validates balance, checks minimum threshold, freezes funds, puts in queue", 
         "withdrawal_id, user_id, amount, payout_method (UPI/PayPal), destination_hash, request_time", "What is the total requested withdrawal volume and method breakdown?", 
         "Missing withdrawal events and ledger", "Missing standalone Withdrawals dataset (~1,200 expected)", "To Be Verified", "Critical Gap"),
        ("Withdrawals", "Withdrawal Fulfillment & Processing", "Finance/Automated payout executes or rejects", "Updates status to Completed/Rejected, triggers notification", 
         "withdrawal_id, processing_latency_hours, payout_txn_id, failure_reason, final_status", "What is average processing time and fulfillment success rate?", 
         "Missing fulfillment status and timestamp telemetry", "Missing standalone Withdrawals dataset", "To Be Verified", "Critical Gap"),

        # 12. Help Center
        ("Help Center", "Support FAQ & Ticket Browse", "Opens help center, searches knowledge base", "Logs article views, search queries, deflection rate", 
         "user_id, article_id, search_term, resolved_flag", "What are the most frequent user friction points?", 
         "Present only as session entry_point in Sessions sheet", "No dedicated event stream in Feature_Events", "Proposed", "Analytics Gap"),

        # 13. Badges
        ("Badges", "Badge Catalog Inspection", "Browses achievement hall", "Displays locked and unlocked achievement badges", 
         "user_id, viewed_timestamp, badges_unlocked_count", "Do achievement badges drive long-term engagement?", 
         "Present in Feature_Events (badge_viewed: 878)", "Present in 03_Feature_Events & 07_Feature_Usage", "Simulated", "Production Ready"),
        ("Badges", "Badge Unlocked / Earned", "Meets badge criteria (e.g. 50 tasks completed)", "Issues badge, awards bonus XP, triggers in-app celebration", 
         "user_id, badge_id, badge_tier, bonus_awarded, timestamp", "Which badges exhibit the highest completion velocity?", 
         "Present in Feature_Events (badge_earned: 954) & Milestones", "Present in 03_Feature_Events & 06_Milestones", "Simulated", "Production Ready"),

        # 14. Levels
        ("Levels", "Level Progress Check", "Checks XP progression bar to next level", "Displays current level, XP needed for level-up", 
         "user_id, current_level, current_xp, next_level_threshold", "What is the level distribution across user base?", 
         "Present in Feature_Events (level_viewed: 1,161)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),
        ("Levels", "Level-Up Event", "Reaches required XP threshold", "Increments level, unlocks new features/tiers, grants reward", 
         "user_id, old_level, new_level, level_up_datetime, reward_unlocked", "What is the median time-to-level across user cohorts?", 
         "Present in Feature_Events (level_up: 1,266)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),

        # 15. XP
        ("XP", "Experience Point Accrual", "Completes any rewarded action (tasks, ads, spin)", "Credits XP, evaluates level-up trigger", 
         "user_id, source_event_id, xp_amount, new_total_xp", "Which product feature contributes most to total platform XP?", 
         "Flagged in Feature_Events (xp_related_flag: Yes)", "Static balance in Users; no granular ledger", "Simulated", "Partial Readiness"),

        # 16. Gems
        ("Gems", "Premium Currency Allocation & Spend", "Buys spins or completes premium sponsor tasks", "Debits/credits Gem balance in user profile", 
         "user_id, transaction_type, gem_amount, item_purchased", "What is the burn-to-earn velocity for premium gems?", 
         "Missing explicit Gem telemetry stream", "No Gem fields in Users or Events sheets", "Proposed", "Critical Gap"),

        # 17. Tokens
        ("Tokens", "Platform Token Generation (Mining/Tasks)", "Yields crypto/platform tokens via mining or high-tier tasks", "Updates blockchain/internal token balance", 
         "user_id, token_amount, token_contract_id, conversion_rate", "What is the circulating supply and token redemption rate?", 
         "Partially implied by mining events; no token ledger", "No dedicated Token balance or ledger sheet", "Proposed", "Critical Gap"),

        # 18. Streaks
        ("Streaks", "Streak Milestone Inspection", "Views consecutive login/task streak", "Displays current streak count, multiplier, freeze days", 
         "user_id, current_streak_days, streak_multiplier", "What streak threshold marks the retention inflection point?", 
         "Present in Feature_Events (streak_viewed: 893)", "Present in 03_Feature_Events", "Simulated", "Production Ready"),
        ("Streaks", "Streak Claim & Break Tracking", "Claims streak bonus or misses 24h window", "Credits streak reward OR resets streak counter to 0", 
         "user_id, streak_status (Claimed/Broken), streak_length, reset_timestamp", "What percentage of broken streaks result in churn within 7 days?", 
         "Present in Feature_Events (claimed: 922, broken: 919)", "Present in 03_Feature_Events & 04_Daily_Activity", "Simulated", "Production Ready")
    ]

    for row_idx, r in enumerate(rows_data, 6):
        ws_cov.row_dimensions[row_idx].height = 24
        is_zebra = (row_idx % 2 == 1)
        for col_idx, val in enumerate(r, 1):
            cell = ws_cov.cell(row=row_idx, column=col_idx)
            fill_override = None
            if col_idx == 10:  # Readiness Status
                if "Production Ready" in val:
                    fill_override = STATUS_GREEN
                elif "Partial" in val:
                    fill_override = STATUS_YELLOW
                elif "Critical Gap" in val or "Gap" in val:
                    fill_override = STATUS_RED
            apply_data_cell(cell, val, is_zebra=is_zebra, align="left" if col_idx <= 6 else "center", fill_override=fill_override)

    autofit_columns(ws_cov, 1, 10)

    # -------------------------------------------------------------------------
    # Sheet 2: Analytics Gaps Register
    # -------------------------------------------------------------------------
    ws_gaps = wb.create_sheet(title="Analytics_Gaps_Register")
    ws_gaps.views.sheetView[0].showGridLines = True
    create_banner(
        ws_gaps,
        "VELOOP REWARDS — PRODUCT ANALYTICS GAPS REGISTER",
        "Deliverable 02/03 Support | 15 Identified Analytics Instrumentation & Schema Gaps"
    )
    ws_gaps.merge_cells("A1:H1")
    ws_gaps.merge_cells("A2:H2")
    ws_gaps.merge_cells("A3:H3")

    gap_headers = [
        "Gap ID", "Domain", "Gap Description", "Current State in Data", 
        "Business & Analytical Impact", "Severity / Priority", "Recommended Remediation", "Status"
    ]
    ws_gaps.row_dimensions[5].height = 28
    for col_idx, h in enumerate(gap_headers, 1):
        cell = ws_gaps.cell(row=5, column=col_idx)
        apply_header_style(cell, h, fill_color=NAVY_HEADER, font_size=10)

    gaps_data = [
        ("GAP-001", "Withdrawals", "Absence of Standalone Withdrawals Transaction Ledger", 
         "No withdrawal events in Feature_Events; no withdrawals sheet provided (~1,200 expected)", 
         "Cannot calculate withdrawal request volume, fulfillment rate, processing latency, or payout method distribution", 
         "Critical", "Implement dedicated `withdrawals` table and instrument `withdrawal_requested`, `withdrawal_processing`, `withdrawal_completed`, `withdrawal_rejected` events", "Proposed"),
        
        ("GAP-002", "Wallet", "Absence of Immutable Double-Entry Wallet Transaction Model", 
         "Only static `xp_balance` in Users and `wallet_viewed` in Events; no transaction ledger (~3,500 expected)", 
         "Cannot perform financial reconciliation, balance auditing, currency flow tracking, or fraud detection", 
         "Critical", "Establish `wallet_transactions` ledger with immutable transaction IDs, currency units (XP/Gems/Cash), source references, and reversal links", "Proposed"),
        
        ("GAP-003", "Rewards", "Separation of Task Activity from Reward Credit Lifecycle", 
         "Task_Activity contains `reward_status`, but no dedicated `rewards` ledger (~5,000 expected) with exact reward unit and disbursement time", 
         "Ambiguity between task completion verification and financial disbursement; inability to audit pending vs credited rewards", 
         "High", "Create distinct `rewards` table with full lifecycle: Viewed -> Started -> Completed -> Validated -> Credited/Pending/Reversed", "Proposed"),
        
        ("GAP-004", "Referrals", "Missing Relational Referrer-Referee Conversion Link", 
         "Referral events exist (created, shared, viewed) and acquisition source has text names, but no table links referring user to referee's user_id", 
         "Inability to calculate viral coefficient (K-factor), referral conversion rates, or attribute referral commission payouts", 
         "Critical", "Deploy `referrals` entity linking `referring_user_id` to `referred_user_id` with registration, activation, and qualification timestamps", "Proposed"),

        ("GAP-005", "User Lifecycle", "Absence of Telemetry Stream for Registration & Login Events", 
         "Registration and last login are static timestamps in Users table; no event records exist in `Feature_Events` stream", 
         "Cannot measure multi-device sign-ins, login failure rates, auth provider switches, or drop-offs during onboarding steps", 
         "High", "Instrument atomic client/server events: `user_registered`, `user_logged_in`, `onboarding_started`, `onboarding_completed`", "Proposed"),

        ("GAP-006", "Tap & Earn", "Missing Tap Volume & Anti-Cheat Payload in Tap Events", 
         "Events sheet records `tap_started` and `tap_completed` but contains no payload indicating tap count, duration, or taps/second", 
         "Impossible to audit bot/autoclicker behavior, tap frequency distribution, or player fatigue patterns", 
         "Medium", "Add payload attributes: `tap_count`, `duration_seconds`, `taps_per_second`, `client_integrity_hash` to `tap_completed` event", "Proposed"),

        ("GAP-007", "Spin the Wheel", "Missing Prize Outcome & Cost Payload in Spin Events", 
         "Spin events record start and completion, but lack properties for prize won, prize value, currency spent, and RNG audit hash", 
         "Cannot audit wheel economy, prize distribution variance against theoretical probabilities, or wheel ROI", 
         "High", "Add properties: `spin_cost_gems`, `prize_type`, `prize_value`, `rng_seed_id` to `spin_completed` payload", "Proposed"),

        ("GAP-008", "Currencies", "Lack of Distinction Between XP, Gems, and Tokens in Ledger", 
         "Users sheet has only `xp_balance`; no representation of premium Gems or platform Tokens exists", 
         "Multi-currency economy cannot be analyzed; tokenomics and monetization metrics cannot be calculated", 
         "High", "Define explicit currency schemas for XP (experience), Gems (premium hard currency), and Tokens (redeemable cash/crypto value)", "Proposed"),

        ("GAP-009", "Help Center", "Missing Customer Support Interaction Telemetry", 
         "Help Center is only listed as a session entry point; zero FAQ view, article search, or support ticket events exist", 
         "Blind spot regarding user frustration, onboarding confusion, withdrawal inquiry volume, and bug reports", 
         "Medium", "Instrument `faq_viewed`, `search_executed`, `support_ticket_created`, `support_ticket_resolved` events", "Proposed"),

        ("GAP-010", "Ad Network", "Missing Ad Network SDK Attribution & eCPM Metadata", 
         "Ad events capture start, skip, and complete, but do not record ad network partner (AdMob, Unity, AppLovin), ad unit type, or revenue eCPM", 
         "Cannot measure monetization yield per ad network, fill rates, or partner performance discrepancies", 
         "High", "Enrich ad events with: `network_partner`, `ad_placement_id`, `ad_format` (interstitial vs rewarded), `estimated_cpm`", "Proposed"),

        ("GAP-011", "Missions", "Lack of Mission Progression & Step-Level Telemetry", 
         "Events capture start, completed, and abandoned, but no incremental milestone progression (e.g. 3 of 5 steps finished)", 
         "Cannot identify bottleneck steps within complex multi-step reward missions", 
         "Medium", "Instrument `mission_step_completed` with `step_number`, `total_steps`, `percent_complete`", "Proposed"),

        ("GAP-012", "Data Quality", "Dirty Data Injection in Event Streams (Messy Audit Sheet)", 
         "`10_Event_Data_Quality_Audit` contains duplicate event IDs, lowercase feature names, null sequence numbers, and unverified devices", 
         "Analytics queries will produce skewed aggregates, broken dashboard filters, and duplicate counts if run directly on raw data", 
         "High", "Deploy pipeline automated data quality validation layer with schema enforcement, casing standardization, and deduplication", "Proposed"),

        ("GAP-013", "Sessionization", "Incomplete Session State Modeling on Mobile Interruptions", 
         "Sessions are modeled with start and end, but no background/foreground transition events or app crash telemetry", 
         "Abrupt mobile app terminations are counted as abandoned sessions rather than technical failures", 
         "Medium", "Implement `app_backgrounded`, `app_foregrounded`, and crash diagnostic SDK integration", "Proposed"),

        ("GAP-014", "Privacy & PII", "Plaintext PII Storage in Analytical Data Layers", 
         "`Users` sheet includes plaintext `full_name` and `email` directly in the analytical reporting view", 
         "Violates privacy best practices (GDPR/DPDP); exposes sensitive personal data to unauthorized analytical consumers", 
         "High", "Implement pseudo-anonymization: hash or mask email and name in analytical marts; restrict raw PII to production auth database", "Proposed"),

        ("GAP-015", "Schema Documentation", "Absence of Centralized Enterprise Data Dictionary", 
         "Supplied data dictionary sheets contain only 25-26 fields; lacks unified catalog covering all 18 domains and 75+ core entities", 
         "Cross-functional confusion between engineering, analytics, and product teams on metric definitions and field validations", 
         "High", "Publish complete 75+ field enterprise Data Dictionary (Deliverable 09) with validation rules, sensitivity tiers, and owners", "Proposed")
    ]

    for row_idx, r in enumerate(gaps_data, 6):
        ws_gaps.row_dimensions[row_idx].height = 24
        is_zebra = (row_idx % 2 == 1)
        for col_idx, val in enumerate(r, 1):
            cell = ws_gaps.cell(row=row_idx, column=col_idx)
            fill_override = None
            if col_idx == 6:  # Severity
                if val == "Critical":
                    fill_override = STATUS_RED
                elif val == "High":
                    fill_override = STATUS_YELLOW
                elif val == "Medium":
                    fill_override = STATUS_BLUE
            apply_data_cell(cell, val, is_zebra=is_zebra, align="left" if col_idx in [2,3,4,5,7] else "center", fill_override=fill_override)

    autofit_columns(ws_gaps, 1, 8)

    os.makedirs("04_deliverables/deliverable_03_data_coverage_matrix", exist_ok=True)
    out_path = "04_deliverables/deliverable_03_data_coverage_matrix/Data_Coverage_Matrix.xlsx"
    wb.save(out_path)
    print(f"[SUCCESS] Generated Deliverable 03 Excel: {out_path}")

# ==============================================================================
# 2. BUILD DELIVERABLE 19: SOURCE & VERIFICATION REGISTER EXCEL
# ==============================================================================
def generate_source_and_verification_register():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Source_Verification_Register"
    ws.views.sheetView[0].showGridLines = True

    create_banner(
        ws,
        "VELOOP REWARDS — SOURCE AND VERIFICATION REGISTER",
        "Deliverable 19 | 4-Tier Evidentiary Classification & Technical Unknowns Tracker"
    )
    ws.merge_cells("A1:I1")
    ws.merge_cells("A2:I2")
    ws.merge_cells("A3:I3")

    headers = [
        "Item ID", "Technical Unknown / Assumption", "Category / Domain", "Why It Matters", 
        "Official Source Checked", "Evidence Level", "Identified Risk", "Verification Status", "Owner & Action"
    ]
    ws.row_dimensions[5].height = 28
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=5, column=col_idx)
        apply_header_style(cell, h, fill_color=NAVY_HEADER, font_size=10)

    register_data = [
        ("REG-001", "Missing Official PDF: Work_Schedule_and_Performance_Policy_VELOOP_Internship.pdf", 
         "Governance", "Establishes mandatory attendance, submission deadlines, and evaluation policies", 
         "Local workspace search", "To Be Verified", "Non-compliance with internal review windows and reporting templates", 
         "Pending User Upload", "Data Analyst Intern: Request user upload to workspace"),

        ("REG-002", "Missing Official PDF: Data_Analyst_01.pdf", 
         "Assignment Brief", "Contains baseline work packages, scoring rubric, and official task instructions", 
         "Local workspace search", "To Be Verified", "Unverified scope expectations or omitted mandatory appendices", 
         "Pending User Upload", "Data Analyst Intern: Request user upload to workspace"),

        ("REG-003", "Missing Standalone Dataset: Rewards (~5,000 expected records)", 
         "Dataset Dependency", "Required for detailed reward disbursement auditing and pending vs credited analysis", 
         "VELoop_Rewards_Data_01.xlsx & Simulated_User_Behavior.xlsx", "To Be Verified", "Cannot compute reward cycle completion vs credit latency", 
         "Documented Missing Dependency", "Data Analyst: Propose schema; request raw dataset"),

        ("REG-004", "Missing Standalone Dataset: Wallet Transactions (~3,500 expected records)", 
         "Dataset Dependency", "Required for balance reconciliation, transaction type breakdown, and double-entry auditing", 
         "VELoop_Rewards_Data_01.xlsx & Simulated_User_Behavior.xlsx", "To Be Verified", "Financial metrics and net currency flows unverified", 
         "Documented Missing Dependency", "Data Analyst: Propose schema; request raw dataset"),

        ("REG-005", "Missing Standalone Dataset: Withdrawals (~1,200 expected records)", 
         "Dataset Dependency", "Required to analyze payout queue, rejection rates, fulfillment latency, and payout methods", 
         "VELoop_Rewards_Data_01.xlsx & Simulated_User_Behavior.xlsx", "To Be Verified", "Withdrawal KPI analysis blocked without simulated or actual ledger", 
         "Documented Missing Dependency", "Data Analyst: Propose schema; request raw dataset"),

        ("REG-006", "Missing Standalone Dataset: Referrals (~900 expected records)", 
         "Dataset Dependency", "Required to map referrer-referee conversion tree and calculate viral coefficient (K-factor)", 
         "VELoop_Rewards_Data_01.xlsx & Simulated_User_Behavior.xlsx", "To Be Verified", "Referral analytics limited to high-level acquisition channel text", 
         "Documented Missing Dependency", "Data Analyst: Propose schema; request raw dataset"),

        ("REG-007", "Simulated Data Authenticity Labeling Across All Artifacts", 
         "Integrity Policy", "Mandatory policy prevents misrepresenting simulated datasets as production performance", 
         "Section 3 Brief Directives & Workbook README sheets", "Confirmed", "Severe professional violation if simulated figures are reported as real revenue/users", 
         "Enforced Across All Files", "Lead Analyst: Continuous audit across all deliverables"),

        ("REG-008", "Actual Production Database Engine and Cloud Architecture", 
         "Infrastructure", "Determines exact SQL dialect, indexing strategy, and pipeline orchestration tools", 
         "Assignment Technology Stack Guidelines", "Proposed", "Sub-optimal schema design if production DB differs from PostgreSQL/Standard SQL", 
         "Proposed Standard PostgreSQL", "Data Engineer: Standardized on PostgreSQL 15+ compatible DDL"),

        ("REG-009", "Currency Valuation & Exchange Rates (XP vs Gems vs Fiat Currency)", 
         "Monetization / Economy", "Required to calculate real financial liability of outstanding user reward balances", 
         "Exchange Center & Users sheets", "To Be Verified", "Inability to accurately report dollar/rupee equivalent liability", 
         "To Be Confirmed by Product", "Product Owner: Document official exchange conversion ratios"),

        ("REG-010", "Withdrawal Fee Structure and Minimum Payout Thresholds", 
         "Business Rules", "Required to validate withdrawal request eligibility and calculate net platform payout cost", 
         "Withdrawal feature requirements", "Proposed", "Withdrawal validation logic may diverge from commercial rules", 
         "Proposed Standard Thresholds", "Business Operations: Confirm minimum payout tiers per payment method")
    ]

    for row_idx, r in enumerate(register_data, 6):
        ws.row_dimensions[row_idx].height = 24
        is_zebra = (row_idx % 2 == 1)
        for col_idx, val in enumerate(r, 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            fill_override = None
            if col_idx == 6:  # Evidence Level
                if val == "Confirmed":
                    fill_override = STATUS_GREEN
                elif val == "Proposed":
                    fill_override = STATUS_BLUE
                elif val == "To Be Verified":
                    fill_override = STATUS_YELLOW
                elif val == "Simulated":
                    fill_override = STATUS_YELLOW
            elif col_idx == 7:  # Risk
                if "Non-compliance" in val or "Severe" in val or "blocked" in val:
                    fill_override = STATUS_RED
                elif "Sub-optimal" in val or "unverified" in val or "Cannot" in val:
                    fill_override = STATUS_YELLOW
            apply_data_cell(cell, val, is_zebra=is_zebra, align="left" if col_idx in [2,4,7,9] else "center", fill_override=fill_override)

    autofit_columns(ws, 1, 9)

    os.makedirs("04_deliverables/deliverable_19_assumption_and_verification_register", exist_ok=True)
    out_path = "04_deliverables/deliverable_19_assumption_and_verification_register/Source_and_Verification_Register.xlsx"
    wb.save(out_path)
    print(f"[SUCCESS] Generated Deliverable 19 Excel: {out_path}")

if __name__ == "__main__":
    generate_data_coverage_matrix()
    generate_source_and_verification_register()

