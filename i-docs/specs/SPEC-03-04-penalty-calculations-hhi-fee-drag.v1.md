---
id: SPEC-03-04
title: Penalty Calculations (HHI, Fee Drag)
status: draft
phase: 3
sequence: 4
dependencies: [SPEC-03-03]
---

# Penalty Calculations (HHI, Fee Drag)

## Overview
A mathematically sound score is useless if it ignores real-world portfolio risks like extreme concentration or high mutual fund fees. This specification defines the penalty functions that deduct points from the aggregated Portfolio Health Score to reflect these risks.

## Goals
1. Calculate the Herfindahl-Hirschman Index (HHI) to measure sector concentration risk.
2. Calculate the weighted average Expense Ratio (Fee Drag) for Mutual Fund/ETF holdings.
3. Apply deterministic point deductions to the final portfolio score based on predefined thresholds.

## Requirements

### 4.1 HHI Concentration Penalty
- **Calculation**: For each sector in the portfolio, sum the weights of all holdings in that sector. Square each sector's total weight. Sum these squared values. `HHI = SUM(Sector_Weight^2)`.
- **Scale**: HHI ranges from 0 (perfectly diversified across infinite sectors) to 1 (100% in one sector).
- **Penalty Logic**:
  - HHI < 0.15: Well diversified. Penalty = `0`.
  - 0.15 <= HHI < 0.25: Moderate concentration. Penalty = `(HHI - 0.15) * 20` (Max 2 points).
  - HHI >= 0.25: High concentration. Penalty = `2 + ((HHI - 0.25) * 40)` (Max 10 points).
- **Deduction**: The calculated penalty is subtracted from the `overall_health_score`.

### 4.2 Fee Drag Penalty
- **Calculation**: Calculate the value-weighted average `expense_ratio` of all holdings where `type` IN ('MUTUAL_FUND', 'ETF').
- **Penalty Logic**:
  - Expense Ratio <= 1.0%: Penalty = `0`.
  - 1.0% < Expense Ratio <= 1.5%: Penalty = `(ER - 1.0) * 10` (Max 5 points).
  - Expense Ratio > 1.5%: Penalty = `5 + ((ER - 1.5) * 20)` (Max 15 points).
- **Deduction**: The calculated penalty is subtracted from the `overall_health_score`.

### 4.3 Final Score Clamping
- After applying HHI and Fee Drag penalties, the final `overall_health_score` must be clamped to a minimum of `0`. It cannot go negative.

## Acceptance Criteria
- [ ] `PenaltyCalculator` service correctly computes HHI based on sector weights.
- [ ] `PenaltyCalculator` correctly computes weighted average expense ratios for MF/ETF holdings.
- [ ] Unit tests verify the exact penalty point deductions at boundary conditions (e.g., HHI = 0.15, 0.25, 0.50).
- [ ] The final portfolio score is updated in the `portfolio_scores` table, including the `hhi_index`, `hhi_penalty`, and `fee_drag_penalty` columns for transparency.
- [ ] The frontend API response includes these penalty breakdowns so users understand *why* points were deducted.

## Out of Scope
- Penalties for single-stock concentration (e.g., >10% in one stock). This is a future enhancement.

## Technical Details
- **Transparency**: The `portfolio_scores` table must store the raw HHI and Fee Drag values alongside the penalties, allowing the frontend to display "You lost 4 points due to high IT sector concentration."
