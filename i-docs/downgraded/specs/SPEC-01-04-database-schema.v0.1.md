---
spec_id: SPEC-01-04
title: Database Schema
phase: 1
sequence: 4
status: Approved
owner: Lead Database Architect
project: INIVESTEC
last_updated: 2023-10-27
---

# SPEC-01-04: Database Schema

## Purpose
Define the complete database schema for Nivesh Pulse using a layered approach that builds on the boilerplate base schema.

## Schema Layers

### Layer 0: Boilerplate Base (Already Exists)
- users
- sessions
- teams (organizations)
- team_members
- api_keys
- billing (Stripe integration)
- credits

### Layer 1: Core Domain Schema
**Purpose**: Define investment instruments and portfolio structures

```sql
-- Instruments (stocks, mutual funds, ETFs, bonds)
CREATE TABLE instruments (
    isin VARCHAR(20) PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(20) CHECK (type IN ('EQUITY', 'MUTUAL_FUND', 'ETF', 'BOND')),
    sector VARCHAR(100),
    peer_group_id VARCHAR(100),
    expense_ratio DECIMAL(5,4),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Portfolios
CREATE TABLE portfolios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    team_id UUID REFERENCES teams(id),  -- For B2B
    name VARCHAR(255) NOT NULL,
    is_model_portfolio BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Holdings
CREATE TABLE holdings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_id UUID REFERENCES portfolios(id) ON DELETE CASCADE,
    isin VARCHAR(20) REFERENCES instruments(isin),
    quantity NUMERIC NOT NULL,
    avg_acquisition_price NUMERIC NOT NULL,
    last_valuation_price NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_holdings_portfolio ON holdings(portfolio_id);
CREATE INDEX idx_holdings_isin ON holdings(isin);
CREATE INDEX idx_portfolios_user ON portfolios(user_id);
CREATE INDEX idx_portfolios_team ON portfolios(team_id);
```

### Layer 2: Time-Series Schema (TimescaleDB)
**Purpose**: Store historical market data and fundamentals

```sql
-- Enable TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Daily market data
CREATE TABLE market_data_daily (
    isin VARCHAR(20) REFERENCES instruments(isin),
    time TIMESTAMPTZ NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    PRIMARY KEY (isin, time)
);

-- Convert to hypertable
SELECT create_hypertable('market_data_daily', 'time');

-- Daily fundamentals
CREATE TABLE fundamentals_daily (
    isin VARCHAR(20) REFERENCES instruments(isin),
    time TIMESTAMPTZ NOT NULL,
    pe_ratio NUMERIC,
    pb_ratio NUMERIC,
    roe DECIMAL(5,2),
    debt_to_equity DECIMAL(5,2),
    eps_growth_yoy DECIMAL(5,2),
    dividend_yield DECIMAL(5,2),
    market_cap BIGINT,
    PRIMARY KEY (isin, time)
);

SELECT create_hypertable('fundamentals_daily', 'time');

-- Retention policies
SELECT add_retention_policy('market_data_daily', INTERVAL '10 years');
SELECT add_retention_policy('fundamentals_daily', INTERVAL '10 years');
```

### Layer 3: Scoring Schema
**Purpose**: Store calculated scores and analytics

```sql
-- Instrument scores (daily)
CREATE TABLE instrument_scores (
    isin VARCHAR(20) REFERENCES instruments(isin),
    as_of_date DATE NOT NULL,
    quality_zscore DECIMAL(5,2),
    value_zscore DECIMAL(5,2),
    momentum_zscore DECIMAL(5,2),
    growth_zscore DECIMAL(5,2),
    risk_zscore DECIMAL(5,2),
    overall_health_score DECIMAL(5,2) CHECK (overall_health_score BETWEEN 0 AND 100),
    PRIMARY KEY (isin, as_of_date)
);

-- Portfolio scores (daily)
CREATE TABLE portfolio_scores (
    portfolio_id UUID REFERENCES portfolios(id) ON DELETE CASCADE,
    as_of_date DATE NOT NULL,
    overall_health_score DECIMAL(5,2),
    quality_score DECIMAL(5,2),
    value_score DECIMAL(5,2),
    momentum_score DECIMAL(5,2),
    growth_score DECIMAL(5,2),
    risk_score DECIMAL(5,2),
    hhi_index DECIMAL(5,4),
    hhi_penalty DECIMAL(5,2),
    fee_drag_penalty DECIMAL(5,2),
    PRIMARY KEY (portfolio_id, as_of_date)
);

-- Indexes
CREATE INDEX idx_instrument_scores_date ON instrument_scores(as_of_date DESC);
CREATE INDEX idx_portfolio_scores_date ON portfolio_scores(as_of_date DESC);
```

### Layer 4: Future RAG Schema (Post-MVP)
**Purpose**: Store document embeddings for RAG

```sql
-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Fund documents
CREATE TABLE fund_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    isin VARCHAR(20) REFERENCES instruments(isin),
    document_type VARCHAR(50),
    chunk_text TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON fund_documents USING ivfflat (embedding vector_cosine_ops);
```

## Data Dictionary

### instruments
| Column | Type | Description |
|--------|------|-------------|
| isin | VARCHAR(20) | International Securities Identification Number |
| symbol | VARCHAR(50) | Trading symbol (NSE/BSE) |
| name | VARCHAR(255) | Full name of instrument |
| type | VARCHAR(20) | EQUITY, MUTUAL_FUND, ETF, BOND |
| sector | VARCHAR(100) | Sector classification |
| peer_group_id | VARCHAR(100) | Peer group for Z-score calculation |
| expense_ratio | DECIMAL(5,4) | Expense ratio (for MFs) |

### portfolios
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Owner (B2C) |
| team_id | UUID | Advisory firm (B2B) |
| name | VARCHAR(255) | Portfolio name |
| is_model_portfolio | BOOLEAN | Template portfolio |

### holdings
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| portfolio_id | UUID | Parent portfolio |
| isin | VARCHAR(20) | Instrument |
| quantity | NUMERIC | Units held |
| avg_acquisition_price | NUMERIC | Average buy price |
| last_valuation_price | NUMERIC | Current price |

### market_data_daily
| Column | Type | Description |
|--------|------|-------------|
| isin | VARCHAR(20) | Instrument |
| time | TIMESTAMPTZ | Timestamp |
| open/high/low/close | NUMERIC | OHLC prices |
| volume | BIGINT | Trading volume |

### fundamentals_daily
| Column | Type | Description |
|--------|------|-------------|
| isin | VARCHAR(20) | Instrument |
| time | TIMESTAMPTZ | Timestamp |
| pe_ratio | NUMERIC | Price-to-Earnings |
| pb_ratio | NUMERIC | Price-to-Book |
| roe | DECIMAL(5,2) | Return on Equity |
| debt_to_equity | DECIMAL(5,2) | Debt-to-Equity ratio |
| eps_growth_yoy | DECIMAL(5,2) | EPS growth YoY |
| dividend_yield | DECIMAL(5,2) | Dividend yield |
| market_cap | BIGINT | Market capitalization |

### instrument_scores
| Column | Type | Description |
|--------|------|-------------|
| isin | VARCHAR(20) | Instrument |
| as_of_date | DATE | Score date |
| quality_zscore | DECIMAL(5,2) | Quality pillar Z-score |
| value_zscore | DECIMAL(5,2) | Value pillar Z-score |
| momentum_zscore | DECIMAL(5,2) | Momentum pillar Z-score |
| growth_zscore | DECIMAL(5,2) | Growth pillar Z-score |
| risk_zscore | DECIMAL(5,2) | Risk pillar Z-score |
| overall_health_score | DECIMAL(5,2) | Aggregated score (0-100) |

### portfolio_scores
| Column | Type | Description |
|--------|------|-------------|
| portfolio_id | UUID | Portfolio |
| as_of_date | DATE | Score date |
| overall_health_score | DECIMAL(5,2) | Portfolio health score |
| quality/value/momentum/growth/risk_score | DECIMAL(5,2) | Pillar scores |
| hhi_index | DECIMAL(5,4) | Herfindahl-Hirschman Index |
| hhi_penalty | DECIMAL(5,2) | Concentration penalty |
| fee_drag_penalty | DECIMAL(5,2) | Expense ratio penalty |

## Migration Strategy

### Phase 1: Initial Setup
1. Apply Layer 1 (Core Domain)
2. Apply Layer 2 (Time-Series)
3. Apply Layer 3 (Scoring)

### Phase 2: Data Population
1. Seed instruments table
2. Backfill historical market data (5 years)
3. Backfill historical fundamentals (5 years)

### Phase 3: Future RAG
1. Apply Layer 4 (RAG Schema)
2. Ingest fund documents
3. Generate embeddings

## Performance Considerations

### Indexing Strategy
- Composite primary keys for time-series tables
- B-tree indexes on foreign keys
- Descending indexes on date columns

### Partitioning
- TimescaleDB automatic partitioning by time
- Retention policies for old data

### Query Optimization
- Materialized views for complex aggregations
- Redis caching for frequent queries

## Acceptance Criteria
- [ ] All 4 layers defined
- [ ] Data dictionary complete
- [ ] Migration strategy documented
- [ ] Performance considerations addressed
- [ ] SQL scripts tested

## Dependencies
- SPEC-01-03: System Architecture

## Tasks
1. Create SQL migration files for each layer
2. Generate data dictionary documentation
3. Define indexing strategy
4. Create seed data scripts
5. Test migrations on development database
