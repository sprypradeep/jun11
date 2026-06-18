---
id: SPEC-01-04
title: Database Schema
status: draft
phase: 1
sequence: 4
dependencies: [SPEC-01-03]
---

# Database Schema

## Overview
This specification defines the layered database schema for INIVESTEC. We utilize a layered approach to build upon the existing boilerplate schema without modifying it directly.

## Schema Layers

### Layer 0: Scaffold Base (Immutable)
- `users`, `sessions`, `teams`, `team_members`, `api_keys`, `billing_subscriptions`, `credit_ledger`.
- *Action*: Do not modify these tables. Reference them via foreign keys where necessary.

### Layer 1: Core Domain Schema
Defines investment instruments and portfolio structures.
- **`instruments`**: `isin` (PK), `symbol`, `name`, `type` (EQUITY, MUTUAL_FUND), `sector`, `peer_group_id`, `expense_ratio`.
- **`portfolios`**: `id` (PK), `user_id` (FK), `team_id` (FK, nullable), `name`, `is_model_portfolio`.
- **`holdings`**: `id` (PK), `portfolio_id` (FK), `isin` (FK), `quantity`, `avg_acquisition_price`.

### Layer 2: Time-Series Schema (TimescaleDB)
Optimized for high-write market data.
- **`market_data_daily`**: `isin`, `time`, `open`, `high`, `low`, `close`, `volume`. (Converted to hypertable partitioned by `time`).
- **`fundamentals_daily`**: `isin`, `time`, `pe_ratio`, `pb_ratio`, `roe`, `debt_to_equity`, `eps_growth_yoy`, `market_cap`. (Converted to hypertable).

### Layer 3: Scoring Schema
Stores calculated analytics.
- **`instrument_scores`**: `isin`, `as_of_date`, `quality_zscore`, `value_zscore`, `momentum_zscore`, `growth_zscore`, `risk_zscore`, `overall_health_score`.
- **`portfolio_scores`**: `portfolio_id`, `as_of_date`, `overall_health_score`, `hhi_index`, `hhi_penalty`, `fee_drag_penalty`.

### Layer 4: Future RAG Schema (pgvector)
- **`fund_documents`**: `id`, `isin`, `document_type`, `chunk_text`, `embedding` (vector(1536)).

## Implementation Rules
1. All Layer 1-3 tables must be created via Alembic migrations.
2. TimescaleDB hypertables must be created immediately after the base table creation in the migration script.
3. Foreign keys to Layer 0 tables (e.g., `user_id`) must include `ON DELETE CASCADE`.
4. Indexes must be created on all foreign keys and date columns (`as_of_date`, `time`).

## Acceptance Criteria
- [ ] Alembic migration `001_add_inivestec_schema.py` is created and applies Layers 1, 2, and 3 successfully.
- [ ] TimescaleDB extension is enabled and hypertables are verified in the database.
- [ ] `docs/domain/data_dictionary.md` is generated containing all tables, columns, types, and descriptions.
- [ ] SQLAlchemy models are generated in `backend/app/models/` matching the schema exactly.
