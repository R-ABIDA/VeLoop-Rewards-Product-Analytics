"""
Deep forensic comparison between 03_Feature_Events and 10_Event_Data_Quality_Audit
in 01_raw_data/VELOOP_Simulated_User_Behavior_1000.xlsx.
Performs all 10 required row-level and column-level comparisons.
"""

import os
import pandas as pd
import numpy as np

wb_path = os.path.join("01_raw_data", "VELOOP_Simulated_User_Behavior_1000.xlsx")
users_wb = os.path.join("01_raw_data", "VELoop_Rewards_Data_01.xlsx")

print("--- 1. Loading datasets ---")
df_events = pd.read_excel(wb_path, sheet_name="03_Feature_Events")
df_audit = pd.read_excel(wb_path, sheet_name="10_Event_Data_Quality_Audit")
df_users = pd.read_excel(users_wb, sheet_name="Users_1000_Clean")

print(f"03_Feature_Events rows: {len(df_events)}, cols: {len(df_events.columns)}")
print(f"10_Event_Data_Quality_Audit rows: {len(df_audit)}, cols: {len(df_audit.columns)}")

print("\n--- 2. Column Names and Data Types ---")
print("Events cols:", list(df_events.columns))
print("Audit cols: ", list(df_audit.columns))
cols_match = list(df_events.columns) == list(df_audit.columns)
print("Columns match exactly?:", cols_match)

print("\n--- 3. Missing and Extra Rows Analysis ---")
events_ids = set(df_events["event_id"])
audit_ids = set(df_audit["event_id"])

print(f"Unique event_id in Events: {len(events_ids)}")
print(f"Unique event_id in Audit:  {len(audit_ids)}")
print(f"Event IDs in Events but not in Audit: {len(events_ids - audit_ids)}")
print(f"Event IDs in Audit but not in Events: {len(audit_ids - events_ids)}")
print(f"Intersection of Event IDs: {len(events_ids & audit_ids)}")

print("\n--- 4. Duplicate Event IDs in Each Dataset ---")
dupes_events = df_events[df_events.duplicated(subset=["event_id"], keep=False)]
dupes_audit = df_audit[df_audit.duplicated(subset=["event_id"], keep=False)]
print(f"Duplicate event_id rows in Events: {len(dupes_events)}")
print(f"Duplicate event_id rows in Audit:  {len(dupes_audit)}")

if len(dupes_audit) > 0:
    print("Audit duplicate event IDs and counts:")
    counts = df_audit["event_id"].value_counts()
    dupe_ids = counts[counts > 1]
    print(dupe_ids)

print("\n--- 5. Complete-Row Duplicates ---")
full_dupes_events = df_events.duplicated().sum()
full_dupes_audit = df_audit.duplicated().sum()
print(f"Complete-row duplicates in Events: {full_dupes_events}")
print(f"Complete-row duplicates in Audit:  {full_dupes_audit}")

print("\n--- 6. Missing Values (Nulls) Comparison ---")
print("Nulls in Events:")
print(df_events.isnull().sum()[df_events.isnull().sum() > 0])
print("Nulls in Audit:")
print(df_audit.isnull().sum()[df_audit.isnull().sum() > 0])

print("\n--- 7. Timestamp & Chronological Checks ---")
print("Events min/max date:", df_events["event_datetime"].min(), "to", df_events["event_datetime"].max())
print("Audit min/max date: ", df_audit["event_datetime"].min(), "to", df_audit["event_datetime"].max())

print("\n--- 8. User References Integrity ---")
valid_user_ids = set(df_users["user_id"])
orphans_events = df_events[~df_events["user_id"].isin(valid_user_ids)]
orphans_audit = df_audit[~df_audit["user_id"].isin(valid_user_ids)]
print(f"Orphan user_id in Events: {len(orphans_events)}")
print(f"Orphan user_id in Audit:  {len(orphans_audit)}")

print("\n--- 9. Feature Names & Casing Discrepancies ---")
events_features = set(df_events["feature_name"].dropna().unique())
audit_features = set(df_audit["feature_name"].dropna().unique())
print("Events features count:", len(events_features), sorted(list(events_features)))
print("Audit features count: ", len(audit_features), sorted(list(audit_features)))
print("Differences (Audit - Events):", audit_features - events_features)
print("Differences (Events - Audit):", events_features - audit_features)

print("\n--- 10. Granular Row-by-Row Value Discrepancies on Shared Deduplicated IDs ---")
df_audit_dedup = df_audit.drop_duplicates(subset=["event_id"], keep="first").sort_values("event_id").reset_index(drop=True)
df_events_sorted = df_events.sort_values("event_id").reset_index(drop=True)

diff_count_by_col = {}
for col in df_events.columns:
    if col in df_audit_dedup.columns:
        s1 = df_events_sorted[col].astype(str)
        s2 = df_audit_dedup[col].astype(str)
        diffs = (s1 != s2).sum()
        diff_count_by_col[col] = diffs

print("Cell differences across columns between Events and Deduplicated Audit:")
for col, diffs in diff_count_by_col.items():
    print(f"  {col}: {diffs} differences")

