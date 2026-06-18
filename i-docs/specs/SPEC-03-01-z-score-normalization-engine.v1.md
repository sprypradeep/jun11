---
id: SPEC-03-01
title: Z-Score Normalization Engine
status: draft
phase: 3
sequence: 1
dependencies: [SPEC-01-04, SPEC-02-03]
---

# Z-Score Normalization Engine

## Overview
This specification defines the mathematical engine that converts raw financial metrics into standardized Z-scores. This allows for apples-to-apples comparison of instruments within their specific peer universes (e.g., comparing a Mid-Cap IT stock only against other Mid-Cap IT stocks, not against Large-Cap Banks).

## Goals
1. Dynamically group instruments into peer universes based on `peer_group_id` (e.g., "NIFTY_500", "LARGE_CAP_IT", "MID_CAP_PHARMA").
2. Calculate mean and standard deviation for each metric within each peer group.
3. Apply Winsorization to cap extreme outliers (e.g., at the 1st and 99th percentiles) before Z-score calculation to prevent skewed distributions.
4. Handle missing or `NULL` data gracefully without breaking the aggregation pipeline.

## Requirements

### 3.1 Peer Group Definition
- Instruments must be grouped by `peer_group_id` as defined in the `instruments` table.
- A fallback peer group (`ALL_EQUITY`) must be used if an instrument's specific peer group has fewer than 10 constituents.

### 3.2 Winsorization Logic
- Before calculating mean and standard deviation, cap values at the 1st and 99th percentiles of the peer group distribution.
- Formula: `Z = (Winsorized_Value - Peer_Group_Mean) / Peer_Group_StdDev`

### 3.3 Handling Edge Cases
- **Zero Standard Deviation**: If all instruments in a peer group have the exact same value (StdDev = 0), assign a Z-score of `0.0`.
- **Missing Data**: If an instrument lacks a specific metric, its Z-score for that metric is `NULL`. It will be excluded from that specific pillar's calculation (handled in SPEC-03-02).
- **New Listings**: Instruments with `< 1 year` of historical data are flagged as `INSUFFICIENT_HISTORY` and excluded from Momentum/Growth Z-scores.

## Acceptance Criteria
- [ ] `ZScoreCalculator` service correctly groups instruments by `peer_group_id`.
- [ ] Winsorization is applied correctly, verified by unit tests with synthetic skewed data.
- [ ] Division by zero (StdDev = 0) is handled without raising exceptions.
- [ ] Performance: Calculating Z-scores for 1000 instruments across 10 metrics completes in < 3 seconds using vectorized Pandas/NumPy operations.
- [ ] Results are cached in Redis with a 24-hour TTL to prevent redundant daily calculations.

## Out of Scope
- Assigning weights to different Z-scores (handled in SPEC-03-02).
- Calculating the final 0-100 Health Score (handled in SPEC-03-02).

## Technical Details
- **Libraries**: `pandas`, `numpy`, `redis` (for caching).
- **Execution**: Triggered via a daily Taskiq cron job (`tasks/scoring/calculate_zscores.py`).
