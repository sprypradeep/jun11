---
spec_id: SPEC-02-02
title: Market Data Ingestion Pipeline
status: draft
phase: 2
sequence: 2
dependencies: [SPEC-01-04, SPEC-02-01]
---

# Market Data Ingestion Pipeline

## Overview
This specification defines the automated pipeline for ingesting daily equity market data (OHLCV) from NSE and BSE, and orchestrating the fundamental data fetched by the scrapers (SPEC-02-01) into the TimescaleDB database.

## Goals
1. Automate the daily download and processing of NSE/BSE bhav copies.
2. Orchestrate the execution of fundamental scrapers via Taskiq.
3. Normalize and upsert all market and fundamental data into TimescaleDB hypertables.

## Requirements

### 2.1 Equity Market Data (NSE/BSE)
- **Source**: Daily Bhav Copies (CSV/ZIP) from NSE and BSE websites.
- **Process**:
  - Taskiq worker triggers daily at 18:00 IST (post-market close).
  - Download the ZIP file, extract the CSV.
  - Parse relevant columns: Symbol, ISIN, Open, High, Low, Close, Volume, Deliverable Quantity.
  - Handle corporate actions (splits/bonus) by checking for "Series" = "EQ" vs others.
- **Storage**: Bulk upsert into `market_data_daily` hypertable.

### 2.2 Fundamental Data Orchestration
- **Process**:
  - Taskiq worker triggers weekly (e.g., Sunday 02:00 IST) for Screener.in data.
  - Taskiq worker triggers daily at 20:00 IST for AMFI NAV data.
  - Fetch data using the scrapers defined in SPEC-02-01.
  - Normalize the data structures to match the `fundamentals_daily` schema.
- **Storage**: Bulk upsert into `fundamentals_daily` hypertable.

### 2.3 Taskiq Integration
- Define Taskiq brokers and queues:
  - `market_data_queue`: High priority, daily execution.
  - `fundamentals_queue`: Low priority, weekly/daily execution.
- Implement dead-letter queues (DLQ) for failed parsing tasks to prevent data loss.

## Acceptance Criteria
- [ ] Daily NSE/BSE bhav copies are automatically downloaded, parsed, and inserted into `market_data_daily`.
- [ ] Taskiq successfully schedules and executes scraper tasks without manual intervention.
- [ ] Data is correctly upserted (no duplicate primary key errors on re-runs).
- [ ] Failed tasks are routed to the DLQ and trigger a Logfire alert.
- [ ] Pipeline processes 5000 equity records in under 60 seconds.

## Out of Scope
- Intraday/minute-level market data.
- Real-time WebSocket market feeds.

## Technical Details
- **Task Scheduling**: Taskiq-cron or external cron triggering Taskiq.
- **Database**: `asyncpg` bulk insert/upsert using `INSERT ... ON CONFLICT DO UPDATE`.
- **Error Handling**: Idempotent processing; re-running the pipeline for the same date yields the exact same database state.
