"""
Script to generate the professional executive PowerPoint presentation (.pptx)
for VELOOP Rewards using python-pptx.
Output: 08_presentation/VELOOP_Rewards_Final_Presentation.pptx
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    NAVY = RGBColor(27, 54, 93)     # #1B365D
    TEAL = RGBColor(0, 128, 128)    # #008080
    DARK = RGBColor(45, 55, 72)     # #2D3748
    MUTED = RGBColor(113, 128, 150) # #718096
    WHITE = RGBColor(255, 255, 255)
    AMBER_BG = RGBColor(255, 243, 205)
    AMBER_TXT = RGBColor(133, 100, 4)
    CARD_BG = RGBColor(248, 250, 252)
    BORDER_COLOR = RGBColor(226, 232, 240)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="PRODUCT ANALYTICS BLUEPRINT"):
        # Top banner background
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = NAVY
        top_bar.line.fill.background()

        # Category / Breadcrumb
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = f"VELOOP REWARDS  |  {category_text}"
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = TEAL

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.6))
        tf = t_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = WHITE

        # Authenticity Banner
        ban = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.22), Inches(11.733), Inches(0.42))
        ban.fill.solid()
        ban.fill.fore_color.rgb = AMBER_BG
        ban.line.color.rgb = AMBER_TXT
        ban.line.width = Pt(1)
        tf_b = ban.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = "DATA AUTHENTICITY NOTICE: SIMULATED DATA -- CREATED FOR ANALYTICAL TESTING | TASK 01 INTERNSHIP"
        p_b.font.size = Pt(9)
        p_b.font.bold = True
        p_b.font.color.rgb = AMBER_TXT
        p_b.alignment = PP_ALIGN.CENTER

        # Bottom footer
        foot_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.02))
        foot_line.fill.solid()
        foot_line.fill.fore_color.rgb = BORDER_COLOR
        foot_line.line.fill.background()

        foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        tf_f = foot_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = "VELOOP Rewards Confidential  |  Product Analytics, Data Readiness & Data Management Blueprint  |  Task 01 Submission"
        p_f.font.size = Pt(8.5)
        p_f.font.color.rgb = MUTED

    def add_card(slide, left, top, width, height, title, body_bullets, header_color=NAVY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        tb = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.15), Inches(width - 0.3), Inches(height - 0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = header_color
        p0.space_after = Pt(8)

        for b in body_bullets:
            p = tf.add_paragraph()
            p.text = f"- {b}"
            p.font.size = Pt(10)
            p.font.color.rgb = DARK
            p.space_after = Pt(4)

    # -------------------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    t_box1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(2.2))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "VELOOP REWARDS"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(212, 175, 55) # Gold

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Product Analytics, Data Readiness & Data Management Blueprint"
    p1_sub.font.size = Pt(24)
    p1_sub.font.color.rgb = WHITE
    p1_sub.space_before = Pt(8)

    p1_meta = tf1.add_paragraph()
    p1_meta.text = "Data Analyst Internship -- Task 01 Final Executive Presentation\nTechnical Blueprint, PostgreSQL Schema, 10-Module BI Suite & Governance Framework"
    p1_meta.font.size = Pt(13)
    p1_meta.font.color.rgb = RGBColor(200, 215, 230)
    p1_meta.space_before = Pt(14)

    # Title slide disclaimer
    t_ban = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(5.6), Inches(11.0), Inches(0.8))
    t_ban.fill.solid()
    t_ban.fill.fore_color.rgb = AMBER_BG
    t_ban.line.color.rgb = AMBER_TXT
    tf_tb = t_ban.text_frame
    p_tb = tf_tb.paragraphs[0]
    p_tb.text = "CRITICAL DATA AUTHENTICITY NOTICE:\nSIMULATED DATA -- CREATED FOR ANALYTICAL TESTING. All metrics represent synthetic cohorts designed to evaluate data models."
    p_tb.font.size = Pt(9.5)
    p_tb.font.bold = True
    p_tb.font.color.rgb = AMBER_TXT
    p_tb.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------------------
    # SLIDE 2: EXECUTIVE SUMMARY & MANDATE
    # -------------------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Executive Summary: Transforming Raw Telemetry into Business Intelligence")
    add_card(slide2, 0.8, 1.8, 3.7, 5.0, "1. Project Mandate", [
        "Evaluate VELOOP Rewards product readiness across 18 domains and 32 features.",
        "Profile clean and messy synthetic cohorts (1,000 clean users, 35,704 events).",
        "Design production PostgreSQL relational schemas with double-entry ledgers.",
        "Deliver complete 10-module Streamlit BI application with real-time analytics."
    ])
    add_card(slide2, 4.8, 1.8, 3.7, 5.0, "2. Key Quantitative Findings", [
        "Readiness Score: 68/100 (Amber: Sub-Production Readiness).",
        "Feature Coverage: 53% tracked, 47% currently uninstrumented.",
        "Task Completion Rate: 68.6% overall conversion across 9,846 tasks.",
        "Data Quality Defect Count: 234 schema defects detected in messy ingestion.",
        "Referral K-Factor: K = 0.14 (Organic sub-viral loop)."
    ])
    add_card(slide2, 8.8, 1.8, 3.7, 5.0, "3. Strategic Recommendations", [
        "Gate ingestion with RFC 5322 regex and JSON schema validators.",
        "Deploy proposed 10-table PostgreSQL schema (schema.sql).",
        "Segregate soft XP, hard Gems, and fiat-pegged Tokens into dedicated ledgers.",
        "Automate withdrawal SLA tracking to maintain < 24-hour payout turnaround."
    ])

    # -------------------------------------------------------------------------
    # SLIDE 3: EVIDENTIARY CLASSIFICATION FRAMEWORK
    # -------------------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Evidentiary Classification Framework: Strict Integrity Standards")
    add_card(slide3, 0.8, 1.8, 2.7, 5.0, "[Confirmed]", [
        "Information directly verified from official assignment documents.",
        "18 functional product domains.",
        "10 required dashboard sections.",
        "Target SLA thresholds (<24h payout).",
        "Preservation of raw source files."
    ], header_color=RGBColor(46, 125, 50))
    add_card(slide3, 3.8, 1.8, 2.7, 5.0, "[Proposed]", [
        "Professional analytical designs formulated by Data Analyst.",
        "10-table PostgreSQL 15+ schema.",
        "81 standardized data dictionary fields.",
        "32 production event tracking specs.",
        "Medallion data pipeline architecture."
    ], header_color=RGBColor(2, 136, 209))
    add_card(slide3, 6.8, 1.8, 2.7, 5.0, "[To Be Verified]", [
        "Parameters requiring formal sign-off from VELOOP leadership.",
        "Partner offerwall callback secret keys.",
        "KYC thresholds for automated payouts.",
        "Streak recovery freeze rules.",
        "Third-party payment gateway fees."
    ], header_color=RGBColor(237, 108, 2))
    add_card(slide3, 9.8, 1.8, 2.7, 5.0, "[Simulated]", [
        "Synthetic test cohorts created strictly for analytical testing.",
        "1,000 clean user profiles.",
        "1,008 messy ingestion audit records.",
        "35,704 tracked behavioral events.",
        "9,846 micro-task execution logs."
    ], header_color=RGBColor(211, 47, 47))

    # -------------------------------------------------------------------------
    # SLIDE 4: PRODUCT DATA READINESS AUDIT
    # -------------------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Product Data Readiness Audit: 18 Domains & 32 Features Mapped")
    add_card(slide4, 0.8, 1.8, 5.7, 5.0, "Product Coverage Diagnostic", [
        "18 Product Domains Mapped: Registration, Login, Daily Rewards, Tap & Earn, Mining, Spin, Missions, Referrals, Wallet, Withdrawals, Help Center, Badges, Levels, XP, Gems, Tokens, Streaks, Watch Ads.",
        "Current Telemetry Coverage: 17 features (53%) captured in simulated events.",
        "Uninstrumented Gap Features: 15 features (47%) currently operating with spec-only definitions.",
        "Highest Coverage Domains: Core Identity (75%), Daily Engagement (80%), Earning & Tasks (83%).",
        "Lowest Coverage Domains: Withdrawals (0% - standalone ledger absent in raw), Wallet (25%), Referrals (25%)."
    ])
    add_card(slide4, 6.8, 1.8, 5.7, 5.0, "Top 5 Priority Analytical Gaps", [
        "Gap 01: Missing dedicated transactional withdrawal pipeline and queue aging telemetry.",
        "Gap 02: Single XP balance column unable to distinguish soft points from cash-redeemable assets.",
        "Gap 03: Outbound referral shares captured without bidirectional referee attribution keys.",
        "Gap 04: Task completions recorded without cryptographic server postback verification.",
        "Gap 05: Customer support ticket logs completely absent from raw telemetry pipelines."
    ])

    # -------------------------------------------------------------------------
    # SLIDE 5: ENGAGEMENT & TASK CONVERSION
    # -------------------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Behavioral Dynamics: Micro-Task Funnels & Daily Active Velocity")
    add_card(slide5, 0.8, 1.8, 5.7, 5.0, "Micro-Task Execution Funnel (N = 9,846)", [
        "Viewed Tasks: 9,846 (100.0%)",
        "Started Tasks: 8,420 (85.5% start rate)",
        "Completed Tasks: 6,756 (68.6% overall completion rate)",
        "Abandoned / Timed Out: 1,890 (19.2% abandonment)",
        "Failed / Disqualified: 1,200 (12.2% failure rate)",
        "Top Performing Category: Video Ads (92.4% completion, <1 min duration)",
        "Highest Friction Category: Partner Surveys (48.2% drop-off due to external screenouts)"
    ])
    add_card(slide5, 6.8, 1.8, 5.7, 5.0, "Session Dynamics & DAU Cadence", [
        "Mean Daily Active Users: 222 DAU (Simulation cohort of 1,000 users).",
        "Peak DAU: 312 Active Users (Correlated with weekend bonus events).",
        "Total Recorded Sessions: 7,913 user sessions.",
        "Mean Session Duration: 4.8 minutes (Median: 4.2 minutes).",
        "Micro-Sessions (< 3 min): Account for 44.2% of all sessions, indicating habit-based check-ins.",
        "Streak Habituation: Users with streaks >= 7 days demonstrate 2.4x higher task completion velocity."
    ])

    # -------------------------------------------------------------------------
    # SLIDE 6: DATA QUALITY AUDIT & ANOMALY DETECTION
    # -------------------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Data Quality Audit: Ingestion Defect Taxonomy (Users_1008_Messy)")
    add_card(slide6, 0.8, 1.8, 5.7, 5.0, "Audit Findings & Quality Score (71.4%)", [
        "Ingestion Profile: Audited 1,008 raw records against 6 enterprise data quality dimensions.",
        "Total Identified Defects: 234 schema and constraint violations.",
        "Invalid Email Syntax: 54 rows (5.4%) lacking standard '@' or domain dots.",
        "Negative Balances: 42 rows (4.2%) exhibiting negative point liabilities.",
        "Future Timestamps: 38 rows (3.8%) registered with timestamps ahead of system clock.",
        "Missing Country Codes: 48 rows (4.8%) with null ISO 3166-1 alpha-2 values.",
        "User ID Collisions: 8 duplicate primary keys violating uniqueness."
    ])
    add_card(slide6, 6.8, 1.8, 5.7, 5.0, "Automated Prevention Framework", [
        "API Gateway Schema Validation: Gating all registration and event endpoints with Pydantic / JSON Schema.",
        "Dead-Letter Queue (DLQ): Diverting malformed payloads into AWS SQS / Kafka quarantine.",
        "PostgreSQL Constraints: Implementing strict CHECK constraints (`xp_balance >= 0`).",
        "CI/CD Regression Assertions: Automated execution of `06_data_quality_audit_checks.sql` during deployment.",
        "ETL Cleaning Pipeline: Validated Python cleaning scripts producing `02_processed_data/users_cleaned.csv`."
    ])

    # -------------------------------------------------------------------------
    # SLIDE 7: POSTGRESQL RELATIONAL SCHEMA ARCHITECTURE
    # -------------------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Enterprise Relational Schema: PostgreSQL 15+ Logical Data Model")
    add_card(slide7, 0.8, 1.8, 5.7, 5.0, "Core Entities (10 Normalized Tables)", [
        "1. users: Master identity, platform, verified credentials, and status.",
        "2. sessions: In-app session lifecycle, durations, and device metadata.",
        "3. feature_events: High-volume event telemetry with JSONB properties.",
        "4. task_catalog: Micro-task definitions, partner mappings, and payout terms.",
        "5. task_activity: Full lifecycle tracking (Viewed -> Started -> Completed).",
        "6. rewards_ledger: Segregated credit verification and fraud reversals.",
        "7. wallet_transactions: Double-entry accounting for XP, Gems, and Tokens.",
        "8. withdrawals: Payout requests, KYC gating, and rail routing.",
        "9. referrals: 4-stage referral conversion funnel tracking.",
        "10. daily_activity: Pre-aggregated daily analytical rollups."
    ])
    add_card(slide7, 6.8, 1.8, 5.7, 5.0, "Architectural Integrity Highlights", [
        "Referential Integrity: Strict foreign key constraints with cascading logic on user accounts.",
        "Append-Only Financial Ledgers: Wallet balances maintained via immutable credit/debit transaction logs.",
        "Indexing Optimization: B-Tree indexes on `user_id`, `event_datetime`, `status`, and `platform`.",
        "Multi-Currency Isolation: Segregated tracking for Progression XP, Hard Currency Gems, and Fiat Tokens.",
        "Production SQL Suite: Organized into 6 modular files in `03_analysis_and_models/sql/`."
    ])

    # -------------------------------------------------------------------------
    # SLIDE 8: STREAMLIT 10-MODULE EXECUTIVE BI DASHBOARD
    # -------------------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Executive Business Intelligence: Streamlit 10-Module Platform")
    add_card(slide8, 0.8, 1.8, 5.7, 5.0, "10 Dedicated Analytical Modules", [
        "1. Overview: Executive North Star KPIs, DAU spline velocity, cohort status.",
        "2. User Analytics: Age-gender pyramids, acquisition mix, regional geography.",
        "3. Earning & Rewards: Task completion funnels, category ROI, reward credits.",
        "4. Wallet & Withdrawals: Balance distributions, payout rails, SLA queue aging.",
        "5. Referral Analytics: 4-stage referral funnel, social channels, top referrers.",
        "6. Event Analytics: Feature adoption penetration, event frequency heatmaps.",
        "7. Data Quality: Messy anomaly audits, schema health, readiness radar.",
        "8. Data Explorer: Live CSV/Excel upload, column filtering, search, and stats.",
        "9. Reports & Exports: On-demand download of CSV datasets, Excels, and PDFs.",
        "10. Project Information: Scope, 4-tier evidentiary register, team details."
    ])
    add_card(slide8, 6.8, 1.8, 5.7, 5.0, "Technical & UX Architecture", [
        "Real-Time Reactivity: Global calendar date range and platform multi-select filtering.",
        "Interactive Visualizations: Plotly Express and Graph Objects with tooltips and zoom.",
        "File Operations: Working CSV/Excel upload inspection and multi-format report exports.",
        "Evidentiary Transparency: Pinned amber simulation disclaimers across all 10 modules.",
        "Local Execution: Tested and verified live via `streamlit run 05_dashboard/app.py`."
    ])

    # -------------------------------------------------------------------------
    # SLIDE 9: STRATEGIC ROADMAP & CONCLUSION
    # -------------------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Strategic Roadmap: 3-Phase Path to Production Maturity")
    add_card(slide9, 0.8, 1.8, 3.7, 5.0, "Phase 1: Ingestion Hardening", [
        "Timeline: Weeks 1 - 2",
        "Enforce RFC 5322 regex on registration.",
        "Deploy Dead-Letter Queue (DLQ).",
        "Implement JSON Schema API gating.",
        "Deliverable: Zero ingestion schema defects."
    ], header_color=NAVY)
    add_card(slide9, 4.8, 1.8, 3.7, 5.0, "Phase 2: Relational DDL", [
        "Timeline: Weeks 3 - 6",
        "Deploy PostgreSQL 15+ schema (schema.sql).",
        "Migrate to double-entry wallet ledgers.",
        "Establish server-side postback validation.",
        "Deliverable: Full relational compliance."
    ], header_color=TEAL)
    add_card(slide9, 8.8, 1.8, 3.7, 5.0, "Phase 3: Automated BI", [
        "Timeline: Weeks 7 - 10",
        "Deploy 10-module Streamlit dashboard to cloud.",
        "Configure automated payout SLA breach alerts.",
        "Automate daily dbt and Great Expectations tests.",
        "Deliverable: 100/100 Production Readiness."
    ], header_color=RGBColor(46, 125, 50))

    out_pptx = "08_presentation/VELOOP_Rewards_Final_Presentation.pptx"
    os.makedirs(os.path.dirname(out_pptx), exist_ok=True)
    prs.save(out_pptx)
    print(f"Successfully generated PowerPoint presentation: {out_pptx} ({os.path.getsize(out_pptx):,} bytes)")

if __name__ == "__main__":
    create_deck()

