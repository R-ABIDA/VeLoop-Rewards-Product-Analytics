# VELOOP REWARDS — SQL DATA MODELS & ANALYTICAL SCRIPTS
**Directory:** `03_analysis_and_models/sql`  
**Dialect:** PostgreSQL 15+  
**Integrity Policy:** SIMULATED DATA — CREATED FOR ANALYTICAL TESTING  

---

## Overview

This directory organizes all SQL relational definitions, DDL schemas, analytics reporting queries, and automated quality control assertions for the VELOOP Rewards platform.

```
03_analysis_and_models/sql/
├── 01_schema_ddl.sql                       # Complete PostgreSQL 15+ Schema DDL (10 core tables)
├── 02_user_and_engagement_analytics.sql    # DAU, WAU, MAU, Retention Cohorts, Session Cadence
├── 03_earning_and_reward_analytics.sql     # Task Funnels, Category Performance, Credit Auditing
├── 04_wallet_and_withdrawal_analytics.sql  # Balance Quartiles, Payout SLA Aging, Rail Distribution
├── 05_referral_virality_analytics.sql      # 4-Stage Referral Funnel, Affiliate Leaderboard
├── 06_data_quality_audit_checks.sql        # Automated Anomaly Detection & Gating Queries
└── README.md                               # Architecture Guide (this document)
```

## Execution Instructions

All scripts can be executed against any PostgreSQL 15+ database instance using `psql`:

```bash
# 1. Initialize schema and tables
psql -h <host> -U <user> -d <database> -f 01_schema_ddl.sql

# 2. Run analytical reporting queries
psql -h <host> -U <user> -d <database> -f 02_user_and_engagement_analytics.sql
psql -h <host> -U <user> -d <database> -f 03_earning_and_reward_analytics.sql
psql -h <host> -U <user> -d <database> -f 04_wallet_and_withdrawal_analytics.sql
psql -h <host> -U <user> -d <database> -f 05_referral_virality_analytics.sql

# 3. Execute automated data quality assertions
psql -h <host> -U <user> -d <database> -f 06_data_quality_audit_checks.sql
```

