---
id: SPEC-03-03
title: Portfolio Aggregation
status: draft
phase: 3
sequence: 3
dependencies: [SPEC-01-04, SPEC-03-02]
---

# Portfolio Aggregation

## Overview
This specification defines how individual instrument Health Scores are rolled up into a single, cohesive Portfolio Health Score. A simple average is insufficient; the aggregation must reflect the economic reality of the portfolio through value-weighting.

## Goals
1. Calculate a value-weighted average of instrument scores based on current market valuation.
2. Handle portfolios containing instruments with missing or insufficient scoring data.
3. Persist the aggregated portfolio scores daily for historical tracking and frontend charting.

## Requirements

### 3.1 Valuation Calculation
- For each holding in a portfolio, calculate `Current_Value = quantity * last_valuation_price`.
- If `last_valuation_price` is missing, fallback to `avg_acquisition_price` (with a Logfire warning).

### 3.2 Weighted Aggregation Formula
- Calculate the weight of each holding: `Weight_i = Current_Value_i / Total_Portfolio_Value`.
- Calculate the weighted average for each pillar: `Portfolio_Pillar_Score = SUM(Weight_i * Instrument_Pillar_Score_i)`.
- Calculate the overall portfolio score: Average of the 5 Portfolio Pillar Scores.

### 3.3 Handling Unscored Holdings
- If an instrument has no score (e.g., newly listed, missing data), its `Weight` is temporarily normalized out of the denominator for that specific calculation, and a Logfire metric `unscored_portfolio_weight_pct` is recorded.
- If > 50% of the portfolio's value consists of unscored instruments, the portfolio score is flagged as `UNRELIABLE`.

### 3.4 Taskiq Orchestration
- Triggered daily after market close and after `instrument_scores` are updated.
- Iterates through all active portfolios, calculates the aggregation, and upserts into the `portfolio_scores` table.

## Acceptance Criteria
- [ ] `PortfolioAggregator` service correctly calculates current values and weights.
- [ ] Weighted average math is verified via unit tests (e.g., a portfolio with 90% weight in a score-80 stock and 10% in a score-20 stock yields ~74).
- [ ] Unscored holdings are gracefully excluded from the denominator, and the `UNRELIABLE` flag is triggered if >50% weight is unscored.
- [ ] Results are successfully upserted into the `portfolio_scores` TimescaleDB-compatible table.
