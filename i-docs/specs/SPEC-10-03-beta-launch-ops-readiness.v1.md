---
id: SPEC-10-03
title: Beta Launch, Operational Readiness & Resilience
status: draft
phase: 10
sequence: 3
dependencies: [SPEC-09-02, SPEC-10-02]
---

# Beta Launch, Operational Readiness & Resilience

## Overview
This specification defines the final operational checklists, data seeding, feature flagging, load testing, and incident response protocols required to safely and resiliently open INIVESTEC to beta users and pilot advisory firms. It ensures the system is not only functional but performant and observable under real-world stress.

## Goals
1. Populate the production database with clean, validated seed data and historical backfills.
2. Implement robust feature flags (kill switches) to allow instant disabling of volatile features without code rollbacks.
3. Validate system performance under load to establish baseline metrics and identify bottlenecks.
4. Establish proactive monitoring alerts and comprehensive operational runbooks for incident response.
5. Execute a flawless, secure launch sequence for the beta cohort.

## Requirements

### 10.1 Production Data Seeding & Backfill
- **Script**: `scripts/seed_production.py`
- **Action**: 
  1. Insert the definitive list of Nifty 500 equities and active AMFI mutual funds into the `instruments` table.
  2. Trigger the Taskiq backfill jobs to populate `market_data_daily` and `fundamentals_daily` with 5 years of historical data.
  3. Seed the `site_content` (CMS) and `scoring_parameters` tables with finalized, production-ready values.
  4. Verify data integrity post-backfill (e.g., ensure no gaps in trading days for Nifty 500 constituents).

### 10.2 Feature Flagging & Kill Switches
- **Implementation**: A lightweight, Redis-backed feature flag system (`backend/app/services/core/feature_flags.py`).
- **Critical Flags**:
  - `enable_ai_narratives`: Toggle the Local LLM narrative generation.
  - `enable_cas_upload`: Toggle the CAS parsing pipeline.
  - `maintenance_mode`: Instantly block all non-admin write operations and display a maintenance UI.
- **Integration**: 
  - FastAPI middleware/dependencies must check these flags before queuing heavy Taskiq tasks.
  - Next.js frontend must check flags to conditionally render premium UI components or show "Temporarily Unavailable" badges.
  - Flags must be cached in Redis with a 60s TTL to prevent DB reads on every request.

### 10.3 Load Testing & Performance Baselines
- **Tooling**: Use `Locust` (Python-native) to simulate beta user traffic.
- **Scenarios**:
  - **Scenario A (Dashboard)**: 500 concurrent users fetching portfolio scores and historical charts.
  - **Scenario B (Ingestion)**: 50 concurrent CAS file uploads (2MB each) triggering parsing tasks.
  - **Scenario C (AI)**: 20 concurrent AI narrative generation requests.
- **Baselines to Establish**:
  - API response times (p95 < 500ms for read operations).
  - Taskiq queue processing latency under load.
  - Ollama (Local LLM) inference time and VRAM utilization peaks.
- **Output**: Generate a `performance_baseline.md` report to guide future scaling decisions.

### 10.4 Proactive Alerting & Operational Runbooks
- **Logfire Alerts**: Configure automated alerts for critical thresholds:
  - Taskiq Dead Letter Queue (DLQ) length > 0.
  - Ollama inference latency p95 > 5 seconds.
  - CAS parsing failure rate > 10% in a 1-hour window.
  - GPU VRAM utilization > 90% (Risk of OOM).
- **Runbooks** (`/docs/runbooks/`):
  - **Incident Response**: Steps for queue backups, API timeouts, and GPU OOM recovery.
  - **DPDP Breach Protocol**: Exact legal/technical steps for PII leaks (shut down API, rotate keys, notify authorities within 72 hours).
  - **Database Recovery**: Point-in-Time Recovery (PITR) steps for the managed PostgreSQL instance.
  - **Data Staleness**: Steps to manually trigger scrapers if NSE/AMFI feeds fail.

### 10.5 Beta Onboarding & Launch Sequence
- **Feedback Loop**: Integrate a lightweight feedback widget (e.g., Intercom, or a custom `/feedback` endpoint linked to a specific Postgres table) for beta users to report bugs or UI friction.
- **Launch Checklist**:
  - [ ] Switch Stripe from Test Mode to Live Mode.
  - [ ] Configure production domain DNS and issue SSL certificates.
  - [ ] Verify Logfire production environment and alert routing (e.g., to email/Slack).
  - [ ] Execute `seed_production.py`.
  - [ ] Send "Welcome" and "Beta Guidelines" emails to the waitlist via Resend.

## Acceptance Criteria
- [ ] `seed_production.py` executes cleanly against an empty production database and populates all required reference tables without foreign key violations.
- [ ] Toggling the `enable_ai_narratives` flag to `false` immediately hides the AI Insights panel in the frontend and returns `503` on the backend endpoint within 60 seconds.
- [ ] Locust load tests complete successfully, and the `performance_baseline.md` is generated and stored in `/docs/`.
- [ ] Logfire alerts are verified to trigger successfully when mock threshold breaches are injected.
- [ ] All four core runbooks are documented, reviewed, and stored in `/docs/runbooks/`.
- [ ] The Launch Sequence Checklist is fully completed and signed off.

## Out of Scope
- Marketing and user acquisition campaigns (handled outside the technical SDLC).
- Auto-scaling infrastructure (Beta will run on fixed-size instances; auto-scaling is deferred to post-beta growth phase).

## Technical Details
- **Load Testing**: Locust scripts must be placed in `tests/load/` and excluded from standard `pytest` runs.
- **Alerting**: Logfire webhooks must be configured to send alerts to a dedicated, secure communication channel (e.g., a private Slack channel or dedicated email).
