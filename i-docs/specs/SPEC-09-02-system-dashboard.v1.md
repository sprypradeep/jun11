---
id: SPEC-09-02
title: System Efficiency & Observability Dashboard
status: draft
phase: 9
sequence: 2
dependencies: [SPEC-02-02, SPEC-05-03]
---

# System Efficiency & Observability Dashboard

## Overview
While Logfire handles deep distributed tracing, the solopreneur requires a quick, in-app operational dashboard to monitor the "pulse" of the system's background processes, infrastructure health, and AI costs without leaving the admin panel.

## Goals
1. Aggregate and display real-time metrics for Taskiq background queues.
2. Monitor the success/failure rates and latency of financial data scrapers.
3. Track LLM inference costs, token usage, and cache hit rates.

## Requirements

### 9.1 Taskiq Queue Monitoring
- **Backend**: Create an endpoint `GET /api/v1/admin/metrics/queues` that queries Redis for Taskiq queue states.
- **Metrics**: 
  - Queue lengths (pending tasks) for `market_data`, `fundamentals`, `cas_parsing`, and `reporting`.
  - Count of tasks in the Dead Letter Queue (DLQ).
  - Average task processing time over the last 1 hour.

### 9.2 Scraper & Data Freshness Metrics
- **Backend**: Create `GET /api/v1/admin/metrics/scrapers`.
- **Metrics**:
  - Success/Failure ratio of daily NSE/BSE and AMFI ingestion tasks over the last 7 days.
  - "Data Freshness": The timestamp of the latest record in `market_data_daily` and `fundamentals_daily`. If the latest date is not the most recent trading day, flag as `STALE`.

### 9.3 AI & LLM Cost Tracking
- **Backend**: Create `GET /api/v1/admin/metrics/ai-usage`.
- **Metrics**:
  - Total tokens consumed by `PublicDataAgent` (Gemini) vs `PrivateDataAgent` (Ollama) in the current billing cycle.
  - Average latency (p50, p95) for narrative generation.
  - Redis cache hit rate for the `NarrativeService` (to measure caching efficiency).

## Acceptance Criteria
- [ ] Admin metrics endpoints execute in < 200ms by utilizing efficient Redis commands and pre-aggregated DB views.
- [ ] The Admin Observability UI (`frontend/app/admin/observability/page.tsx`) renders real-time charts for queue depths and scraper success rates.
- [ ] The UI prominently displays a red "STALE DATA" warning if market data ingestion has failed for the current trading day.
- [ ] AI usage metrics correctly differentiate between cloud (Gemini) and local (Ollama) token consumption.
- [ ] Unit tests mock Redis and DB queries to verify the metric aggregation logic.

## Technical Details
- **Backend**: Use `redis-py` for queue introspection. Use TimescaleDB `time_bucket` functions for fast time-series aggregation of scraper logs.
- **Frontend**: Use `recharts` to render the operational dashboards within the admin layout.
