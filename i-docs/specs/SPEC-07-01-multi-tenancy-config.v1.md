---
id: SPEC-07-01
title: Multi-Tenancy Configuration
status: draft
phase: 7
sequence: 1
dependencies: [SPEC-01-03, SPEC-01-04]
---

# Multi-Tenancy Configuration

## Overview
This specification defines how INIVESTEC leverages the scaffold’s existing Teams and RBAC infrastructure to provide a secure, isolated B2B "AdvisorOS" experience. It ensures strict data isolation between different advisory firms and their clients.

## Goals
1. Map scaffold concepts to AdvisorOS domain concepts (e.g., Team = Advisory Firm).
2. Enforce strict application-level data scoping to prevent cross-tenant data leakage.
3. Provide programmatic API access for advisors via scoped API keys.

## Requirements

### 7.1 Domain Mapping
- **Organization/Team**: Represents an Advisory Firm or Wealth Management Company.
- **Team Member**: Represents an Advisor, Analyst, or Admin within the firm.
- **Roles**: 
  - `OWNER`: Firm administrator, manages billing, invites members, views all firm data.
  - `ADMIN`: Senior advisor, can create model portfolios and view all firm client portfolios.
  - `MEMBER`: Junior advisor/analyst, can view assigned client portfolios and generate reports.

### 7.2 Data Isolation (Application-Level Scoping)
- Every database query retrieving portfolio or client data **must** be scoped by `team_id`.
- Implement a FastAPI dependency `get_current_team_context(user: User) -> TeamContext` that extracts the user's active `team_id`.
- All repository methods for AdvisorOS endpoints must accept `team_id` as a mandatory filter parameter. 
- **Hard Rule**: No query in the `backend/app/api/routes/v1/advisor/` directory may execute without an explicit `team_id` filter.

### 7.3 Programmatic API Access
- Advisors require API access to integrate INIVESTEC scores into their own CRM systems.
- Extend the scaffold’s `api_keys` table to include a `scope` column (e.g., `read_only`, `full_access`).
- API keys are strictly bound to the `team_id` of the creator.

## Acceptance Criteria
- [ ] Domain mapping is documented in `/system_meta/adr/005_teams_for_advisoros.md`.
- [ ] `get_current_team_context` dependency is implemented and applied to all new advisor routes.
- [ ] Unit tests verify that User A from Team 1 cannot access User B's portfolio in Team 2, even if they guess the `portfolio_id` (returns `403 Forbidden`).
- [ ] API key generation and validation logic correctly scopes requests to the creating `team_id`.

## Out of Scope
- Custom PostgreSQL Row-Level Security (RLS) policies (application-level scoping via SQLAlchemy is sufficient and aligns with the scaffold).
- Complex hierarchical team structures (e.g., sub-branches).

## Technical Details
- **Libraries**: FastAPI `Depends`, SQLAlchemy `filter_by(team_id=...)`.
- **Security**: All advisor actions (e.g., viewing a client portfolio) must be logged to Logfire with the `team_id` and `user_id` for audit trails.
