-- schema.sql
-- Run with: psql -d fieldforce_db -f schema.sql
-- PostgreSQL 14+

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ─────────────────────────────────────────
-- STAFF
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS staff (
    id         VARCHAR(36)  PRIMARY KEY DEFAULT gen_random_uuid()::text,
    name       VARCHAR(120) NOT NULL,
    phone      VARCHAR(20)  NOT NULL UNIQUE,
    email      VARCHAR(120) UNIQUE,
    role       VARCHAR(50)  NOT NULL DEFAULT 'field_staff',
    region     VARCHAR(100),
    manager_id VARCHAR(36)  REFERENCES staff(id),
    active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ─────────────────────────────────────────
-- CLIENTS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS clients (
    id            VARCHAR(36)  PRIMARY KEY DEFAULT gen_random_uuid()::text,
    company_name  VARCHAR(200) NOT NULL,
    industry      VARCHAR(100),
    address       TEXT,
    city          VARCHAR(100),
    contact_name  VARCHAR(120),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(120),
    account_tier  VARCHAR(20)  DEFAULT 'standard',
    notes         TEXT,
    active        BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ─────────────────────────────────────────
-- VISITS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS visits (
    id                  VARCHAR(36)    PRIMARY KEY DEFAULT gen_random_uuid()::text,
    staff_id            VARCHAR(36)    NOT NULL REFERENCES staff(id),
    client_id           VARCHAR(36)    NOT NULL REFERENCES clients(id),
    visit_date          DATE           NOT NULL DEFAULT CURRENT_DATE,
    time_in             VARCHAR(10),
    time_out            VARCHAR(10),
    visit_type          VARCHAR(50)    NOT NULL DEFAULT 'Visit',
    rep_met             VARCHAR(200),
    purpose             TEXT,
    prev_visit_summary  TEXT,
    priority            VARCHAR(20)    NOT NULL DEFAULT 'Medium',
    notes               TEXT,
    gps_lat             NUMERIC(10,7),
    gps_lng             NUMERIC(10,7),
    source              VARCHAR(20)    NOT NULL DEFAULT 'text',
    created_at          TIMESTAMPTZ    NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_visits_staff_date ON visits(staff_id, visit_date);
CREATE INDEX IF NOT EXISTS idx_visits_client     ON visits(client_id);
CREATE INDEX IF NOT EXISTS idx_visits_date       ON visits(visit_date);

-- ─────────────────────────────────────────
-- ACTION ITEMS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS action_items (
    id          VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    visit_id    VARCHAR(36) NOT NULL REFERENCES visits(id) ON DELETE CASCADE,
    staff_id    VARCHAR(36) NOT NULL REFERENCES staff(id),
    description TEXT        NOT NULL,
    status      VARCHAR(30) NOT NULL DEFAULT 'open',
    help_needed TEXT,
    due_date    DATE,
    resolved_at TIMESTAMPTZ,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_actions_staff  ON action_items(staff_id, status);
CREATE INDEX IF NOT EXISTS idx_actions_due    ON action_items(due_date) WHERE status != 'done';

-- ─────────────────────────────────────────
-- FOLLOW-UPS
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS follow_ups (
    id             VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    visit_id       VARCHAR(36) NOT NULL REFERENCES visits(id) ON DELETE CASCADE,
    client_id      VARCHAR(36) NOT NULL REFERENCES clients(id),
    assigned_to_id VARCHAR(36) NOT NULL REFERENCES staff(id),
    due_date       DATE        NOT NULL,
    notes          TEXT,
    status         VARCHAR(30) NOT NULL DEFAULT 'scheduled',
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_followups_staff_date ON follow_ups(assigned_to_id, due_date);
CREATE INDEX IF NOT EXISTS idx_followups_due        ON follow_ups(due_date) WHERE status = 'scheduled';

-- ─────────────────────────────────────────
-- REPORTS (audit log)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reports (
    id               VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    report_date      DATE        NOT NULL,
    generated_by     VARCHAR(50) DEFAULT 'scheduler',
    delivery_channel VARCHAR(50) DEFAULT 'api',
    payload          TEXT,
    sent_at          TIMESTAMPTZ,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
