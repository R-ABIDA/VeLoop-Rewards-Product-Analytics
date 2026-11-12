-- =============================================================================
-- VELOOP REWARDS — DATA QUALITY ASSURANCE & AUDIT CHECKS
-- Work Package I & K | Deliverables 12 & 13
-- Integrity Policy: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
-- Dialect: PostgreSQL 15+
-- =============================================================================

-- -----------------------------------------------------------------------------
-- CHECK 1: Email Syntax Conformance (RFC 5322 Standard)
-- -----------------------------------------------------------------------------
SELECT 
    user_id,
    email,
    'Invalid Email Syntax' AS defect_reason
FROM veloop.users
WHERE email !~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$';

-- -----------------------------------------------------------------------------
-- CHECK 2: Negative Balance Constraint Violations
-- -----------------------------------------------------------------------------
SELECT 
    user_id,
    xp_balance,
    gems_balance,
    tokens_balance,
    'Negative Balance Violation' AS defect_reason
FROM veloop.users
WHERE xp_balance < 0 OR gems_balance < 0 OR tokens_balance < 0;

-- -----------------------------------------------------------------------------
-- CHECK 3: Future Timestamp Temporal Drift
-- -----------------------------------------------------------------------------
SELECT 
    user_id,
    registration_datetime,
    'Future Registration Timestamp' AS defect_reason
FROM veloop.users
WHERE registration_datetime > CURRENT_TIMESTAMP;

-- -----------------------------------------------------------------------------
-- CHECK 4: Missing Mandatory Demographics / ISO Country Codes
-- -----------------------------------------------------------------------------
SELECT 
    user_id,
    country,
    age,
    'Missing or Malformed Demographic' AS defect_reason
FROM veloop.users
WHERE country IS NULL OR LENGTH(country) != 2 OR age IS NULL;

-- -----------------------------------------------------------------------------
-- CHECK 5: Orphaned Event Telemetry (Foreign Key Drift)
-- -----------------------------------------------------------------------------
SELECT 
    e.event_id,
    e.user_id,
    'Orphaned Event: User Not in Master Table' AS defect_reason
FROM veloop.feature_events e
LEFT JOIN veloop.users u ON e.user_id = u.user_id
WHERE u.user_id IS NULL;

