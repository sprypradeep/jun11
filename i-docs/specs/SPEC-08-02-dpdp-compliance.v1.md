---
id: SPEC-08-02
title: DPDP Compliance
status: draft
phase: 8
sequence: 2
dependencies: [SPEC-04-03, SPEC-05-01]
---

# DPDP Compliance

## Overview
This specification formalizes the technical controls required to comply with India’s Digital Personal Data Protection (DPDP) Act. It focuses on explicit consent, data retention, the Right to Erasure, and the Right to Data Portability.

## Goals
1. Implement explicit, auditable consent collection before processing any PII (e.g., CAS uploads).
2. Automate data retention policies to purge or anonymize PII after a defined period.
3. Provide users with self-serve mechanisms to export their data or request account deletion.

## Requirements

### 8.1 Explicit Consent Tracking
- Add a `consent_given_at` (TIMESTAMPTZ) and `consent_version` (VARCHAR) column to the `users` or `portfolios` table.
- **Frontend Gate**: The CAS upload flow (SPEC-06-02) must include a mandatory, unchecked checkbox: "I consent to the processing of my financial data for portfolio analysis, as per the Privacy Policy." The API must reject the upload if this consent flag is not present and valid.

### 8.2 Automated Data Retention
- **CAS Files**: Raw uploaded CAS files in `/tmp/cas_uploads/` must be deleted immediately after parsing (already in SPEC-04-01). 
- **Database Retention**: Implement a monthly Taskiq cron job `purge_stale_pii.py` that:
  - Hard-deletes CAS parsing logs older than 90 days.
  - Anonymizes `unmapped_holdings` data older than 180 days (replaces scheme names with "REDACTED").
- **Logfire**: Ensure Logfire retention policies are configured to drop PII-containing spans after 30 days.

### 8.3 Right to Erasure (Right to be Forgotten)
- **Endpoint**: `POST /api/v1/users/me/erase`
- **Logic**: 
  1. Soft-delete the user record (set `is_deleted = True`, clear email/name).
  2. Cascade delete or anonymize all associated `portfolios`, `holdings`, and `portfolio_scores`.
  3. Invalidate all active sessions and API keys.
  4. Log the erasure request in an immutable audit table (`data_erasure_logs`).

### 8.4 Right to Data Portability
- **Endpoint**: `GET /api/v1/users/me/export`
- **Logic**: Generate a comprehensive JSON or CSV file containing the user’s profile, portfolio holdings, and historical scores. Trigger a secure, time-limited (24h) download link via Resend email.

## Acceptance Criteria
- [ ] CAS upload API strictly enforces the `consent_given` payload field, returning 400 if missing.
- [ ] `purge_stale_pii` Taskiq job successfully executes and anonymizes target records without breaking foreign key constraints.
- [ ] Erasure endpoint successfully anonymizes user data and invalidates sessions, verified by integration tests.
- [ ] Data export endpoint generates a valid, complete JSON payload and emails the link.
- [ ] `/docs/domain/dpdp_compliance.md` is fully updated with these technical implementations and mapped to specific DPDP Act clauses.

## Out of Scope
- Legal drafting of the Privacy Policy or Terms of Service (assumed to be provided by legal counsel).
- Cross-border data transfer mechanisms (all data and Local LLM inference remain strictly within the designated region/VPC).

## Technical Details
- **Libraries**: SQLAlchemy `soft_delete` patterns, `pandas` for CSV export, scaffold's Resend integration.
- **Security**: Erasure and export endpoints must require re-authentication (e.g., recent JWT issuance or 2FA) to prevent malicious account wiping.
