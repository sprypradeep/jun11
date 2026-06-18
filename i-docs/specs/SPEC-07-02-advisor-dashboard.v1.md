---
id: SPEC-07-02
title: Advisor Dashboard
status: draft
phase: 7
sequence: 2
dependencies: [SPEC-07-01, SPEC-06-01]
---

# Advisor Dashboard

## Overview
This specification defines the backend APIs and frontend views for advisors to manage their client base, monitor aggregate portfolio health, and create "Model Portfolios" that can be cloned to clients.

## Goals
1. Provide a high-level dashboard for advisors to view firm-wide metrics (Total AUM, Average Health Score).
2. Enable CRUD operations for client profiles and their associated portfolios.
3. Implement a "Model Portfolio" feature allowing advisors to define a target allocation and clone it to multiple clients.

## Requirements

### 7.1 Firm-Wide Metrics API
- **Endpoint**: `GET /api/v1/advisor/firm/metrics`
- **Logic**: Aggregates data across all portfolios where `team_id` matches the advisor's firm.
- **Response**: Total AUM, count of active clients, average overall health score, count of portfolios with "UNRELIABLE" or high-penalty scores.

### 7.2 Client & Portfolio Management
- **Endpoints**: 
  - `GET /api/v1/advisor/clients` (Lists clients with their primary portfolio's health score).
  - `POST /api/v1/advisor/clients/{client_id}/portfolios` (Create a new portfolio for a client).
- **Logic**: All operations strictly scoped by `team_id`.

### 7.3 Model Portfolio & Cloning
- **Concept**: A `is_model_portfolio=True` portfolio acts as a template.
- **Endpoint**: `POST /api/v1/advisor/model-portfolios/{model_id}/clone`
- **Payload**: `{ "target_client_id": "uuid", "target_portfolio_name": "string" }`
- **Logic**: 
  1. Fetch all holdings from the model portfolio.
  2. Create a new portfolio for the `target_client_id`.
  3. Insert holdings with `quantity=0` (or a base unit), allowing the advisor or client to fund it later, OR copy exact quantities if specified.
  4. Trigger a background Taskiq job to calculate the initial score for the new portfolio.

## Acceptance Criteria
- [ ] Firm metrics API returns aggregated data in < 500ms using optimized SQLAlchemy queries.
- [ ] Client list endpoint correctly filters and returns only clients belonging to the authenticated advisor's `team_id`.
- [ ] Model portfolio cloning successfully creates a new portfolio and copies all holdings, returning the new `portfolio_id`.
- [ ] Frontend Advisor Dashboard (`frontend/app/advisor/page.tsx`) renders the metrics and client list with skeleton loaders.
- [ ] Unit tests verify the cloning logic and ensure the new portfolio is correctly linked to the `target_client_id` and `team_id`.

## Out of Scope
- Automated rebalancing alerts (deferred to Post-MVP).
- Direct execution of trades based on model portfolios.

## Technical Details
- **Backend**: SQLAlchemy `func.sum`, `func.avg` for metrics. Taskiq for async cloning score calculation.
- **Frontend**: Next.js 15 Server Components for initial data fetch, Client Components for the cloning modal.
