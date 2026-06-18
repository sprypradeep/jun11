---
id: SPEC-08-01
title: Credit Consumption Model
status: draft
phase: 8
sequence: 1
dependencies: [SPEC-04-01, SPEC-05-03, SPEC-07-03]
---

# Credit Consumption Model

## Overview
This specification defines the rules, enforcement mechanisms, and user experience for the credit-based usage metering system. It leverages the scaffold’s existing `credit_ledger` and Stripe integration to monetize compute-heavy operations like CAS parsing, AI narrative generation, and PDF report creation.

## Goals
1. Define a clear, predictable credit cost matrix for all premium actions.
2. Implement atomic credit deduction: credits are only consumed if the underlying Taskiq task succeeds.
3. Provide clear user feedback and graceful degradation when credit balances are insufficient.

## Requirements

### 8.1 Credit Cost Matrix
Define the following consumption rates in `backend/app/config/credit_config.py`:
- **CAS Upload & Parse**: 10 credits per file.
- **AI Narrative Generation**: 15 credits per request.
- **White-Label PDF Report**: 20 credits per generation.
- **Historical Backtest Run** (Post-MVP): 50 credits per run.
- **Basic Scoring & Dashboard View**: 0 credits (included in base subscription).

### 8.2 Credit Manager Service
- Create a `CreditManager` service responsible for:
  - `check_balance(team_id: UUID, required_credits: int) -> bool`
  - `reserve_credits(team_id: UUID, required_credits: int, task_id: str) -> bool` (Optional: holds credits pending task completion).
  - `consume_credits(team_id: UUID, task_id: str) -> bool` (Finalizes deduction on Taskiq success).
  - `refund_credits(team_id: UUID, task_id: str) -> bool` (Reverses reservation on Taskiq failure).

### 8.3 Enforcement & UX
- **API Level**: Premium endpoints (`/cas/upload`, `/narrative/stream`, `/reports/generate`) must call `check_balance` before queuing the Taskiq job. If insufficient, return `402 Payment Required` with a message: "Insufficient credits. Please top up your account."
- **Frontend Level**: Display the user’s current credit balance prominently in the top navigation. Show the expected credit cost next to action buttons (e.g., "Generate Insights (15 Credits)").
- **Webhook Integration**: Ensure the scaffold’s existing Stripe webhook handler correctly increments the `credit_ledger` upon successful top-up purchases.

## Acceptance Criteria
- [ ] `CreditManager` service correctly implements atomic reserve/consume/refund logic.
- [ ] API endpoints return `402 Payment Required` when the balance is below the required threshold.
- [ ] Taskiq jobs for CAS parsing and AI narratives successfully call `consume_credits` on completion, and `refund_credits` on failure.
- [ ] Frontend UI accurately displays the live credit balance and expected costs.
- [ ] Integration tests verify that a failed Taskiq job does not result in a net credit loss for the user.

## Out of Scope
- Complex tiered pricing logic (e.g., volume discounts). Handled via Stripe Subscription plans mapping to monthly credit allowances.
- Negative credit balances (system must strictly block actions at 0).

## Technical Details
- **Database**: Use PostgreSQL transactions (`async with session.begin():`) to ensure ledger updates and task state changes are atomic.
- **Scaffold Alignment**: Extend the scaffold’s existing `credits` and `billing` modules rather than building a new ledger.
