---
id: SPEC-03-02
title: 5-Pillar Scoring Logic
status: draft
phase: 3
sequence: 2
dependencies: [SPEC-03-01]
---

# 5-Pillar Scoring Logic

## Overview
This specification maps the normalized Z-scores (from SPEC-03-01) to the 5 core pillars of the INIVESTEC Health Score: Quality, Value, Momentum, Growth, and Risk. It defines the exact financial metrics, their directional bias (higher is better vs. lower is better), and the aggregation formula to produce a 0-100 pillar score.

## Goals
1. Map specific financial ratios to the 5 pillars.
2. Invert Z-scores where necessary (e.g., high PE is bad for Value, so its Z-score must be inverted).
3. Aggregate metric Z-scores into a single 0-100 score per pillar using a Cumulative Distribution Function (CDF) or Min-Max scaling mapped to a normal distribution.

## Requirements

### 3.1 Pillar Definitions & Metric Mapping
Each pillar is an equally weighted average of its constituent metric Z-scores (unless specified otherwise):
1. **Quality**: ROE, ROCE, Debt-to-Equity (inverted), Interest Coverage.
2. **Value**: PE Ratio (inverted), PB Ratio (inverted), EV/EBITDA (inverted), Dividend Yield.
3. **Momentum**: 3-Month Return, 6-Month Return, 12-Month Return, Relative Strength Index (RSI).
4. **Growth**: 3-Year Sales Growth, 3-Year EPS Growth, 3-Year Profit Growth.
5. **Risk**: Beta (inverted, target ~1.0), 1-Year Volatility (inverted), Max Drawdown (inverted).

### 3.2 Directional Inversion
- For metrics where a *lower* value is better (e.g., PE Ratio, Debt-to-Equity, Volatility), the Z-score must be multiplied by `-1` before aggregation.

### 3.3 0-100 Scaling
- Raw pillar Z-scores (typically ranging from -3 to +3) must be converted to a 0-100 scale.
- **Formula**: `Pillar_Score = 50 + (Aggregate_Z_Score * 15)`
- **Clamping**: The result must be strictly clamped between `0` and `100`. (A Z-score of 0 equals a score of 50, representing the peer group median).

### 3.4 Overall Instrument Health Score
- The final `overall_health_score` for an instrument is the simple average of the 5 Pillar Scores, *excluding* any pillar that resulted in `NULL` due to missing data.

## Acceptance Criteria
- [ ] `PillarCalculator` service correctly maps metrics to pillars and applies directional inversion.
- [ ] The 0-100 scaling formula correctly maps a Z-score of 0 to 50, and clamps extremes to 0 and 100.
- [ ] Missing data in one pillar does not nullify the entire instrument score; the overall score averages only available pillars.
- [ ] Taskiq successfully executes the daily scoring pipeline, updating the `instrument_scores` table.
- [ ] Unit tests verify the exact mathematical output for a mock instrument with known Z-scores.

## Out of Scope
- Portfolio-level aggregation (handled in SPEC-03-03).
- Penalty applications (handled in SPEC-03-04).

## Technical Details
- **Configuration**: Pillar mappings and weights should be defined in a configuration file (`backend/app/config/scoring_config.py`) to allow easy future adjustments without code changes.
