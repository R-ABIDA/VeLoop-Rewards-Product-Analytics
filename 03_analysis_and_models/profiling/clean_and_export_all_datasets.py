"""
VELOOP REWARDS — REPRODUCIBLE DATA PIPELINE & CLEANING SCRIPT
Generates cleaned datasets in 02_processed_data/ directly from original Excel workbooks
Investigates and documents:
  - Event record count difference (35,704 vs 35,714)
  - Messy user audit anomalies (1,008 vs 1,000)
"""

import os
import json
import pandas as pd
import numpy as np

raw_f1 = '01_raw_data/VELoop_Rewards_Data_01.xlsx'
raw_f2 = '01_raw_data/VELOOP_Simulated_User_Behavior_1000.xlsx'
proc_dir = '02_processed_data'
evidence_dir = '07_tests_and_validation/evidence'

os.makedirs(proc_dir, exist_ok=True)
os.makedirs(evidence_dir, exist_ok=True)

print("1. Loading raw workbooks...")
xl1 = pd.ExcelFile(raw_f1)
xl2 = pd.ExcelFile(raw_f2)

# Load Sheets
users_clean = xl1.parse("Users_1000_Clean")
users_messy = xl1.parse("Users_Messy_Audit")
sessions = xl2.parse("02_Sessions")
events_clean = xl2.parse("03_Feature_Events")
events_audit = xl2.parse("10_Event_Data_Quality_Audit")
daily = xl2.parse("04_Daily_Activity")
tasks = xl2.parse("05_Task_Activity")
milestones = xl2.parse("06_Milestones")
features = xl2.parse("07_Feature_Usage")

print("2. Investigating Event Count Difference (03_Feature_Events vs 10_Event_Data_Quality_Audit)...")
# 03_Feature_Events: 35,704 rows
# 10_Event_Data_Quality_Audit: 35,714 rows
event_dup_mask = events_audit['event_id'].duplicated(keep=False)
event_dup_rows = events_audit[event_dup_mask].sort_values('event_id')
dup_event_ids = list(events_audit[events_audit['event_id'].duplicated()]['event_id'].unique())

print(f"  Total rows in 03_Feature_Events: {len(events_clean)}")
print(f"  Total rows in 10_Event_Data_Quality_Audit: {len(events_audit)}")
print(f"  Duplicate rows in 10_Event_Data_Quality_Audit: {len(events_audit) - events_audit['event_id'].nunique()}")
print(f"  Exact 10 duplicate Event IDs: {dup_event_ids}")

# Verify exact duplicate content
exact_dups = True
for eid in dup_event_ids:
    sub = events_audit[events_audit['event_id'] == eid]
    if not sub.iloc[0].equals(sub.iloc[1]):
        exact_dups = False
print(f"  Are all 10 duplicated audit rows 100% exact duplicate records? {exact_dups}")

event_reconciliation = {
    "source_feature_events_count": int(len(events_clean)),
    "audit_feature_events_count": int(len(events_audit)),
    "row_difference": int(len(events_audit) - len(events_clean)),
    "unique_event_ids_in_events": int(events_clean['event_id'].nunique()),
    "unique_event_ids_in_audit": int(events_audit['event_id'].nunique()),
    "duplicate_event_ids_in_audit_count": len(dup_event_ids),
    "duplicate_event_ids": dup_event_ids,
    "audit_exact_duplicates": exact_dups,
    "root_cause_explanation": (
        "The 10-record difference between 03_Feature_Events (35,704) and 10_Event_Data_Quality_Audit (35,714) "
        "is caused by exactly 10 duplicate rows present in the audit worksheet for intentional data quality testing. "
        "When 10_Event_Data_Quality_Audit is deduplicated on event_id, its unique record count is exactly 35,704, "
        "matching 03_Feature_Events 1:1."
    )
}

print("3. Investigating Users Messy Audit vs Clean...")
messy_dup_mask = users_messy['user_id'].duplicated(keep=False)
messy_dup_rows = users_messy[messy_dup_mask].sort_values('user_id')
dup_user_ids = list(users_messy[users_messy['user_id'].duplicated()]['user_id'].unique())
print(f"  Total rows in Users_1000_Clean: {len(users_clean)}")
print(f"  Total rows in Users_Messy_Audit: {len(users_messy)}")
print(f"  Duplicate rows in Users_Messy_Audit: {len(users_messy) - users_messy['user_id'].nunique()}")
print(f"  Exact 8 duplicate User IDs: {dup_user_ids}")

# Missing values in messy
null_counts = users_messy.isna().sum()[users_messy.isna().sum() > 0].to_dict()

users_reconciliation = {
    "clean_users_count": int(len(users_clean)),
    "messy_users_count": int(len(users_messy)),
    "row_difference": int(len(users_messy) - len(users_clean)),
    "unique_user_ids_clean": int(users_clean['user_id'].nunique()),
    "unique_user_ids_messy": int(users_messy['user_id'].nunique()),
    "duplicate_user_ids_count": len(dup_user_ids),
    "duplicate_user_ids": dup_user_ids,
    "missing_values_by_column": {k: int(v) for k, v in null_counts.items()},
    "root_cause_explanation": (
        "Users_Messy_Audit contains 1,008 records representing 1,000 unique users. "
        "The 8-record excess is caused by 8 duplicate user records, along with missing values "
        "in age, gender, city, registration_datetime, and primary_device."
    )
}

print("4. Standardizing and Exporting Clean Datasets to 02_processed_data/...")

# Clean Users
users_clean_export = users_clean.copy()
users_clean_export['registration_datetime'] = pd.to_datetime(users_clean_export['registration_datetime'])
users_clean_export['last_login_datetime'] = pd.to_datetime(users_clean_export['last_login_datetime'])
users_clean_export.to_csv(os.path.join(proc_dir, "users_cleaned.csv"), index=False)
print("  Saved users_cleaned.csv (1,000 rows)")

# Clean Events
events_clean_export = events_clean.copy()
events_clean_export['event_datetime'] = pd.to_datetime(events_clean_export['event_datetime'])
events_clean_export.to_csv(os.path.join(proc_dir, "events_cleaned.csv"), index=False)
print("  Saved events_cleaned.csv (35,704 rows)")

# Clean Sessions
sessions_export = sessions.copy()
sessions_export['session_start'] = pd.to_datetime(sessions_export['session_start'])
sessions_export['session_end'] = pd.to_datetime(sessions_export['session_end'])
sessions_export.to_csv(os.path.join(proc_dir, "sessions_cleaned.csv"), index=False)
print(f"  Saved sessions_cleaned.csv ({len(sessions_export)} rows)")

# Clean Daily Activity
daily_export = daily.copy()
daily_export['activity_date'] = pd.to_datetime(daily_export['activity_date'])
daily_export.to_csv(os.path.join(proc_dir, "daily_activity_cleaned.csv"), index=False)
print(f"  Saved daily_activity_cleaned.csv ({len(daily_export)} rows)")

# Clean Tasks
tasks_export = tasks.copy()
tasks_export['task_viewed_at'] = pd.to_datetime(tasks_export['task_viewed_at'])
tasks_export['task_started_at'] = pd.to_datetime(tasks_export['task_started_at'])
tasks_export['task_completed_at'] = pd.to_datetime(tasks_export['task_completed_at'])
tasks_export.to_csv(os.path.join(proc_dir, "tasks_cleaned.csv"), index=False)
print(f"  Saved tasks_cleaned.csv ({len(tasks_export)} rows)")

# Clean Milestones
milestones_export = milestones.copy()
milestones_export['milestone_datetime'] = pd.to_datetime(milestones_export['milestone_datetime'])
milestones_export.to_csv(os.path.join(proc_dir, "milestones_cleaned.csv"), index=False)
print(f"  Saved milestones_cleaned.csv ({len(milestones_export)} rows)")

# Export Audit Reconciliation Evidence
event_dup_rows.to_csv(os.path.join(proc_dir, "event_audit_10_duplicates.csv"), index=False)
messy_dup_rows.to_csv(os.path.join(proc_dir, "users_messy_8_duplicates.csv"), index=False)

# Save Master Data Quality Audit Output
dq_summary = {
    "project": "VELOOP Rewards Product Analytics",
    "evidentiary_standard": "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING",
    "execution_timestamp": pd.Timestamp.now().isoformat(),
    "event_reconciliation": event_reconciliation,
    "users_reconciliation": users_reconciliation,
    "dataset_inventory": {
        "users_1000_clean": {"rows": len(users_clean), "cols": len(users_clean.columns)},
        "users_messy_audit": {"rows": len(users_messy), "cols": len(users_messy.columns)},
        "sessions": {"rows": len(sessions), "cols": len(sessions.columns)},
        "feature_events": {"rows": len(events_clean), "cols": len(events_clean.columns)},
        "event_data_quality_audit": {"rows": len(events_audit), "cols": len(events_audit.columns)},
        "daily_activity": {"rows": len(daily), "cols": len(daily.columns)},
        "task_activity": {"rows": len(tasks), "cols": len(tasks.columns)},
        "milestones": {"rows": len(milestones), "cols": len(milestones.columns)},
        "feature_usage": {"rows": len(features), "cols": len(features.columns)}
    },
    "wallet_source_findings": {
        "wallet_activity_daily_records": int((daily['wallet_activity'] == 'Yes').sum()),
        "wallet_activity_unique_users": int(daily[daily['wallet_activity'] == 'Yes']['user_id'].nunique()),
        "wallet_viewed_events": int((events_clean['event_name'] == 'wallet_viewed').sum()),
        "wallet_viewed_unique_users": int(events_clean[events_clean['event_name'] == 'wallet_viewed']['user_id'].nunique()),
        "monetary_withdrawal_records_found": 0,
        "monetary_withdrawal_note": "No monetary withdrawal or fiat payout records exist in the supplied Excel workbooks. Tables and metrics must reflect schema/reconciliation only."
    },
    "referral_source_findings": {
        "users_acquired_via_referral": int((users_clean['acquisition_source'] == 'Referral').sum()),
        "referral_source_detail_breakdown": users_clean['referral_source_detail'].value_counts(dropna=False).to_dict(),
        "referral_activity_daily_records": int((daily['referral_activity'] == 'Yes').sum()),
        "referral_events_total": int((events_clean['feature_name'] == 'Referral').sum()),
        "referral_events_by_name": events_clean[events_clean['feature_name'] == 'Referral']['event_name'].value_counts().to_dict(),
        "referrer_referee_pairs_found": 0,
        "referral_relationship_note": "No referrer-to-referee user ID mapping exists in source workbooks. Referral conversions cannot be calculated without relational links."
    }
}

with open(os.path.join(evidence_dir, "data_quality_audit_output.json"), "w") as f:
    json.dump(dq_summary, f, indent=2)

print(f"5. Saved data quality audit evidence to {os.path.join(evidence_dir, 'data_quality_audit_output.json')}")
print("Pipeline execution complete!")

