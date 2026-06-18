---
id: SPEC-01-03
title: System Architecture
status: draft
phase: 1
sequence: 3
dependencies: [SPEC-01-01, SPEC-01-02]
---

# System Architecture

## Overview
This document defines the micro-modular architecture of INIVESTEC, mapping the boilerplate scaffold features to the specific domain requirements of the wealthtech platform.

## High-Level Architecture
```text
[Next.js 15 Frontend] <--> [Nginx Reverse Proxy] <--> [FastAPI Backend]
                                                         |
                           +-----------------------------+-----------------------------+
                           |                             |                             |
                    [PydanticAI Agents]          [Taskiq Workers]             [Middleware]
                           |                             |                             |
               +-----------+-----------+       +----------+----------+        [PII Classifier]
               |                       |       |                     |
        [PublicDataAgent]       [PrivateDataAgent]  [Scrapers]   [Scoring Engine]
        (Google Gemini)         (Local Ollama)
```

## Component Mapping (Scaffold to INIVESTEC)

### 1. Backend (FastAPI)
- **API Layer**: Standard REST endpoints for portfolios and scoring.
- **Task Orchestration**: Uses **Taskiq** (configured in scaffold) for all background jobs (scraping, CAS parsing, score calculation).
- **Observability**: **Logfire** (configured in scaffold) is used for tracing scraper latency, LLM inference times, and data quality alerts.

### 2. AI & LLM Strategy (Hybrid Model)
- **Data Classifier Middleware**: Inspects all payloads before they reach PydanticAI agents.
- **Tier 1 (Public Data)**: Routes market commentary, sector analysis, and general financial queries to **Google Gemini** (via scaffold's PydanticAI integration).
- **Tier 2 (PII Data)**: Routes CAS parsing results, personalized portfolio narratives, and client-specific reports to a **Local LLM (Ollama/Llama-3)** running in a separate Docker container.

### 3. Multi-Tenancy & B2B (AdvisorOS)
- **Scaffold Teams**: We will NOT build custom multi-tenancy. The scaffold's `Teams`, `Members`, and `Roles` will be directly mapped to Advisory Firms and Advisors.
- **Scaffold Billing/Credits**: The scaffold's Stripe and Credit system will be used to meter "Portfolio Analysis Units" (PAUs). 1 CAS parse = X credits, 1 AI Narrative = Y credits.

### 4. Database Architecture
- **Relational**: PostgreSQL (Users, Portfolios, Holdings).
- **Time-Series**: TimescaleDB extension for `market_data_daily` and `fundamentals_daily` hypertables.
- **Vector**: pgvector extension initialized for future RAG (Phase 3+).
- **Caching/Queue**: Redis (used for caching scores, rate limiting, and as the Taskiq broker).

## Acceptance Criteria
- [ ] Architecture diagram is finalized and saved to `/docs/architecture.md`.
- [ ] `system_meta/adr/001_hybrid_llm_strategy.md` is created documenting the Gemini vs. Ollama routing.
- [ ] `system_meta/adr/002_teams_for_advisoros.md` is created documenting the mapping of scaffold Teams to B2B concepts.
- [ ] Docker compose is verified to include an Ollama service alongside the scaffold's existing services.
