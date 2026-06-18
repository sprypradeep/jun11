---
spec_id: SPEC-02-03
title: Data Quality & Validation
status: draft
phase: 2
sequence: 3
dependencies: [SPEC-01-04, SPEC-02-02]
---

# Data Quality & Validation

## Overview
Financial data is inherently messy. This specification defines the validation rules, anomaly detection mechanisms, and data reconciliation processes to ensure that only clean, accurate data flows into the Scoring Engine (Phase 3).

## Goals
1. Prevent invalid or anomalous financial data from corrupting the scoring models.
2. Detect missing data points (e.g., holidays, scraping failures).
3. Provide actionable alerts to the administrator when data quality degrades.

## Requirements

### 3.1 Schema & Range Validation
- **Pydantic Validators**: All data entering the database must pass through strict Pydantic models.
  - *Price checks*: OHLC prices must be > 0. High >= Low, High >= Open/Close, Low <= Open/Close.
  - *Ratio checks*: PE Ratio must be > 0 (or explicitly null for loss-making companies). ROE/ROCE should logically be between -100% and +500%.
  - *Volume checks*: Volume must be >= 0.

### 3.2 Completeness & Reconciliation
- **Trading Calendar Check**: Verify that `market_data_daily` has exactly one record per active ISIN for every trading day defined in the NSE holiday calendar.
- **Cross-Source Verification**: 
  - Compare AMFI reported NAV for ETFs against the NSE closing price for the same ISIN. Tolerance: < 1% variance.
  - Compare total AUM reported by AMFI against the sum of (shares outstanding * market price) for equity funds.

### 3.3 Anomaly Detection
- **Z-Score Outliers**: If a daily price change exceeds ±20% (excluding newly listed stocks or NSE circuit breakers), flag it for manual review.
- **Stale Data**: If fundamental data (e.g., PE ratio) hasn't updated in 90 days, flag the instrument's fundamental data as "Stale".

### 3.4 Alerting & Dashboard
- Integrate with Logfire to create a "Data Quality" dashboard.
- Metrics to track:
  - % of successful daily bhav parses.
  - Number of schema drift alerts.
  - Number of cross-source verification failures.

## Acceptance Criteria
- [ ] Pydantic validators reject and log any OHLC data where High < Low.
- [ ] A daily Taskiq reconciliation task successfully identifies missing trading days and logs them.
- [ ] Cross-verification between AMFI ETF NAV and NSE close price triggers an alert if variance > 1%.
- [ ] Logfire dashboard accurately reflects data quality metrics for the last 30 days.
- [ ] "Stale" fundamental data prevents the instrument from being scored in Phase 3.

## Out of Scope
- Automated correction of bad data (e.g., auto-adjusting for splits). This requires manual intervention or a specialized corporate action API.

## Technical Details
- **Validation Library**: Pydantic V2 `@field_validator` and `@model_validator`.
- **Reconciliation**: Taskiq scheduled task running at 21:00 IST daily.
- **Observability**: Logfire metrics and dashboards.
