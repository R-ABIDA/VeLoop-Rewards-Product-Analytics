"""
VELOOP REWARDS — EVIDENCE CHARTS GENERATOR
Generates high-resolution PNG charts using Matplotlib & Seaborn for documentation and presentation.
Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Corporate Palette
NAVY = "#1B365D"
TEAL = "#008080"
GOLD = "#D4AF37"
CORAL = "#E05638"
GREEN = "#2E7D32"
LIGHT_GRAY = "#F8F9FA"

os.makedirs("08_evidence_charts", exist_ok=True)
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams['figure.dpi'] = 300

# -----------------------------------------------------------------------------
# 1. LOAD DATA
# -----------------------------------------------------------------------------
f_users = "Data/VELoop_Rewards_Data_01.xlsx"
f_behavior = "Data/VELOOP_Simulated_User_Behavior_1000.xlsx"

users = pd.read_excel(f_users, sheet_name="Users_1000_Clean")
sessions = pd.read_excel(f_behavior, sheet_name="02_Sessions")
events = pd.read_excel(f_behavior, sheet_name="03_Feature_Events")
daily = pd.read_excel(f_behavior, sheet_name="04_Daily_Activity")
tasks = pd.read_excel(f_behavior, sheet_name="05_Task_Activity")
features = pd.read_excel(f_behavior, sheet_name="07_Feature_Usage")

daily["activity_date"] = pd.to_datetime(daily["activity_date"])

# -----------------------------------------------------------------------------
# CHART 1: DAILY ACTIVE USERS (DAU) & EVENT VELOCITY
# -----------------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10, 5))

dau_trend = daily.groupby("activity_date").agg(
    dau=("user_id", "nunique"),
    events=("event_count", "sum")
).reset_index()

ax1.plot(dau_trend["activity_date"], dau_trend["dau"], color=NAVY, linewidth=2.2, label="DAU (Active Users)")
ax1.set_xlabel("Calendar Date", fontweight="bold")
ax1.set_ylabel("Daily Active Users (DAU)", color=NAVY, fontweight="bold")
ax1.tick_params(axis='y', labelcolor=NAVY)

ax2 = ax1.twinx()
ax2.plot(dau_trend["activity_date"], dau_trend["events"], color=TEAL, linewidth=1.8, linestyle="--", label="Total Event Volume")
ax2.set_ylabel("Total Event Volume", color=TEAL, fontweight="bold")
ax2.tick_params(axis='y', labelcolor=TEAL)
ax2.grid(False)

plt.title("VELOOP Rewards: Daily Active Users & Event Velocity Over Time\n[SIMULATED DATA — CREATED FOR ANALYTICAL TESTING]", fontsize=12, fontweight="bold", pad=15)
fig.tight_layout()
plt.savefig("08_evidence_charts/01_daily_active_users_trend.png")
plt.close()
print("Saved 01_daily_active_users_trend.png")

# -----------------------------------------------------------------------------
# CHART 2: FEATURE ADOPTION & EVENT VOLUME
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
feat_sorted = features.sort_values(by="total_events", ascending=True)
bars = ax.barh(feat_sorted["feature_name"], feat_sorted["total_events"], color=NAVY, edgecolor=TEAL)

for bar in bars:
    w = bar.get_width()
    ax.text(w + 50, bar.get_y() + bar.get_height()/2, f"{int(w):,}", va='center', ha='left', fontsize=8, color="#333333")

ax.set_xlabel("Total Event Volume", fontweight="bold")
ax.set_title("VELOOP Rewards: Interaction Telemetry Volume Across 15 Features\n[SIMULATED DATA — CREATED FOR ANALYTICAL TESTING]", fontsize=12, fontweight="bold", pad=15)
fig.tight_layout()
plt.savefig("08_evidence_charts/02_feature_adoption_and_event_volume.png")
plt.close()
print("Saved 02_feature_adoption_and_event_volume.png")

# -----------------------------------------------------------------------------
# CHART 3: TASK EXECUTION STATUS BREAKDOWN
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
status_counts = tasks["task_status"].value_counts()
colors = [GREEN, GOLD, CORAL, "#0288D1"]
wedges, texts, autotexts = ax.pie(
    status_counts, labels=status_counts.index, autopct='%1.1f%%',
    startangle=140, colors=colors, textprops=dict(color="black", fontweight="bold"),
    wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2)
)
for at in autotexts:
    at.set_fontsize(10)

ax.set_title("Earning Task Execution Outcomes (9,846 Total Attempts)\n[SIMULATED DATA — CREATED FOR ANALYTICAL TESTING]", fontsize=12, fontweight="bold", pad=15)
fig.tight_layout()
plt.savefig("08_evidence_charts/03_task_execution_status_breakdown.png")
plt.close()
print("Saved 03_task_execution_status_breakdown.png")

# -----------------------------------------------------------------------------
# CHART 4: DEMOGRAPHIC AGE & GENDER PYRAMID
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
valid_age = users.dropna(subset=["age", "gender"])
valid_age = valid_age[valid_age["gender"].isin(["Male", "Female", "Non-binary", "Prefer not to say"])]

sns.histplot(data=valid_age, x="age", hue="gender", multiple="stack", palette="deep", ax=ax, bins=18)
ax.set_xlabel("User Age (Completed Years)", fontweight="bold")
ax.set_ylabel("User Count", fontweight="bold")
ax.set_title("VELOOP Rewards: Demographic Age Distribution by Gender\n[SIMULATED DATA — CREATED FOR ANALYTICAL TESTING]", fontsize=12, fontweight="bold", pad=15)
fig.tight_layout()
plt.savefig("08_evidence_charts/04_demographic_age_gender_pyramid.png")
plt.close()
print("Saved 04_demographic_age_gender_pyramid.png")

# -----------------------------------------------------------------------------
# CHART 5: ACQUISITION SOURCE BREAKDOWN
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
acq = users["acquisition_source"].value_counts()
sns.barplot(x=acq.index, y=acq.values, palette="mako", ax=ax)
ax.set_xlabel("Acquisition Source Channel", fontweight="bold")
ax.set_ylabel("User Registrations", fontweight="bold")
for p in ax.patches:
    ax.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold', fontsize=9)

ax.set_title("User Registrations by Acquisition Channel (1,000 Users)\n[SIMULATED DATA — CREATED FOR ANALYTICAL TESTING]", fontsize=12, fontweight="bold", pad=15)
fig.tight_layout()
plt.savefig("08_evidence_charts/05_acquisition_channel_distribution.png")
plt.close()
print("Saved 05_acquisition_channel_distribution.png")

# -----------------------------------------------------------------------------
# CHART 6: ANALYTICS READINESS SCORECARD RADAR
# -----------------------------------------------------------------------------
categories = ['Event\nCoverage', 'Data\nModel', 'Data\nDictionary', 'KPI\nDefinitions', 'Data\nQuality', 'Dashboard\nReadiness', 'Engineering\nInstrumentation', 'Access\nControl', 'Documentation', 'Reporting']
scores = [85, 75, 90, 90, 80, 95, 55, 70, 95, 85]

N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
scores += scores[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
ax.plot(angles, scores, color=NAVY, linewidth=2)
ax.fill(angles, scores, color=TEAL, alpha=0.35)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=8, fontweight='bold')
ax.set_ylim(0, 100)
ax.set_title("VELOOP Analytics Readiness Scorecard (Overall: 68/100)\n[SIMULATED DATA — CREATED FOR ANALYTICAL TESTING]", fontsize=11, fontweight="bold", pad=20)
fig.tight_layout()
plt.savefig("08_evidence_charts/06_analytics_readiness_radar.png")
plt.close()
print("Saved 06_analytics_readiness_radar.png")

print("All 6 high-resolution evidence charts successfully generated in 08_evidence_charts/")

