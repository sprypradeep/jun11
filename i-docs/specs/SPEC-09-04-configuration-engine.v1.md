---
id: SPEC-09-04
title: Data Refinement & Scoring Configuration Engine
status: draft
phase: 9
sequence: 4
dependencies: [SPEC-03-02, SPEC-03-04, SPEC-04-02]
---

# Data Refinement & Scoring Configuration Engine

## Overview
Financial data is messy, and scoring models require tuning. This specification provides the admin with direct control over the quantitative engine, allowing for manual data correction, peer group adjustments, and dynamic tweaking of scoring parameters without code deployments.

## Goals
1. Allow admins to manually resolve and map `unmapped_holdings` from CAS parses.
2. Enable dynamic adjustment of scoring parameters (e.g., HHI penalty thresholds, pillar weights).
3. Provide the ability to trigger manual re-scoring for specific instruments or portfolios.

## Requirements

### 9.1 Data Refinement & Unmapped Holdings Resolution
- **Backend**: 
  - `GET /api/v1/admin/data/unmapped`: Fetch a paginated list of all unresolved `unmapped_holdings` across the platform, showing the raw scheme name and the portfolio it belongs to (anonymized).
  - `POST /api/v1/admin/data/map-holding`: Payload `{ "raw_scheme_name": "string", "target_isin": "string", "apply_globally": boolean }`.
- **Logic**: If `apply_globally` is true, create a permanent alias in an `instrument_aliases` table so future CAS parses automatically map this raw name to the `target_isin`.

### 9.2 Dynamic Scoring Configuration
- **Database**: Create a `scoring_parameters` table (key-value store for floats/ints).
  - Keys: `hhi_threshold_moderate`, `hhi_threshold_high`, `fee_drag_threshold`, `pillar_weight_quality`, etc.
- **Backend**: 
  - `GET /api/v1/admin/config/scoring`: Fetch current parameters.
  - `PUT /api/v1/admin/config/scoring`: Update parameters.
- **Logic**: Update `backend/app/config/scoring_config.py` (from SPEC-03-02) to read from this database table (cached in Redis) instead of hardcoded Python constants.

### 9.3 Manual Re-Scoring Triggers
- **Backend**: 
  - `POST /api/v1/admin/scoring/recalculate`: Payload `{ "scope": "instrument" | "portfolio" | "global", "target_id": "uuid" | null }`.
- **Logic**: Queues a high-priority Taskiq job to recalculate Z-scores or portfolio aggregations based on the new parameters or corrected data, bypassing the daily cron schedule.

## Acceptance Criteria
- [ ] Admin UI displays a queue of unmapped holdings with a searchable dropdown to assign an ISIN and a toggle for "Apply Globally".
- [ ] Updating a scoring parameter (e.g., changing HHI threshold from 0.25 to 0.30) successfully updates the Redis cache and database.
- [ ] The next portfolio score calculation uses the newly updated HHI threshold, verified by unit tests.
- [ ] The "Recalculate" button successfully triggers the Taskiq job and updates the UI state to "Processing".
- [ ] Global instrument aliases correctly resolve raw CAS text to ISINs in subsequent parser tests.

## Technical Details
- **Caching**: `scoring_parameters` must be cached in Redis with a short TTL (e.g., 5 minutes) or invalidated immediately upon update to ensure the scoring engine uses the latest rules.
- **Safety**: Changing scoring parameters should ideally be versioned or logged in the `audit_logs` table to track why a portfolio's score might have suddenly changed.
