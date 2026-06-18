---
id: SPEC-09-01
title: Admin Security & Compliance Audit Interface
status: draft
phase: 9
sequence: 1
dependencies: [SPEC-04-03, SPEC-08-02]
---

# Admin Security & Compliance Audit Interface

## Overview
This specification defines the admin-only backend APIs and frontend views required to monitor security events, track DPDP compliance actions, and review data quality anomalies. It provides a centralized dashboard for the administrator to maintain the integrity and legal compliance of the platform.

## Goals
1. Provide real-time visibility into PII sanitization failures and security anomalies.
2. Track and manage DPDP-specific events (erasure requests, consent revocations).
3. Monitor data ingestion health, specifically CAS schema drift and unmapped holdings.

## Requirements

### 9.1 Security & PII Audit Logs
- **Backend**: Create an `audit_logs` table (or leverage Logfire API) to store security events.
- **Events Tracked**: 
  - PII leakage attempts blocked by `PIISanitizationMiddleware`.
  - Unusual login patterns or failed API key authentications.
  - Rate limit (`429`) triggers on premium endpoints.
- **API**: `GET /api/v1/admin/audit/security?limit=50` (Strictly admin-only).

### 9.2 DPDP Compliance Dashboard
- **Backend**: Query the `data_erasure_logs` and `consent_tracking` tables (from SPEC-08-02).
- **API**: `GET /api/v1/admin/audit/compliance`
- **UI Features**:
  - List of pending or recently completed "Right to Erasure" requests.
  - Aggregate view of user consent opt-in rates.
  - Ability to manually trigger a "Forget User" action if a legal request is received via support channels.

### 9.3 Data Quality & Schema Drift Monitor
- **Backend**: Aggregate logs from the CAS parsing pipeline (SPEC-04-02).
- **API**: `GET /api/v1/admin/audit/data-quality`
- **UI Features**:
  - Alert banner if `CAS_SCHEMA_DRIFT` events exceed a threshold (e.g., > 5 failures in 24h).
  - Table of recent parsing failures with sanitized error snippets (no PII) to help the admin debug regex changes.
  - Global count of `unmapped_holdings` across the platform.

## Acceptance Criteria
- [ ] All `/api/v1/admin/audit/*` endpoints are protected by the admin role dependency and return `403` for non-admins.
- [ ] The Security UI successfully renders a paginated list of blocked PII leakage attempts.
- [ ] The Compliance UI displays erasure logs and allows an admin to manually initiate an erasure workflow.
- [ ] The Data Quality UI correctly aggregates and displays CAS drift alerts without exposing raw user text.
- [ ] Unit tests verify that admin audit endpoints never return raw PII, even if the underlying log accidentally captured it (applying a final `PIISanitizer` pass on the API response).

## Technical Details
- **Security**: The API response payload for audit logs must pass through the `PIISanitizer` one last time before being sent to the frontend, ensuring defense-in-depth.
- **Frontend**: Next.js Admin Layout (`frontend/app/admin/audit/page.tsx`) using data tables with server-side pagination.
