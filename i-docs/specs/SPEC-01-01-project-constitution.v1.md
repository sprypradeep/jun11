---
id: SPEC-01-01
title: Project Constitution
status: draft
phase: 1
sequence: 1
dependencies: []
---

# Project Constitution

## Overview
This document defines the foundational purpose, objectives, constraints, and success criteria for INIVESTEC. It serves as the ultimate source of truth for all product and technical decisions.

## Project Identity
- **Codename**: INIVESTEC
- **Type**: B2C & B2B Fintech SaaS (WealthTech)
- **Target Market**: Indian retail and institutional investors, Investment Advisors.

## Core Objective
Build an AI-native platform that translates complex market signals into a simplified 0–100 "Health Score" for investment portfolios, reducing choice paralysis through objective, multi-factor analysis while ensuring zero PII leakage to external cloud AI providers.

## Key Objectives & Phasing
1. **Phase 1-3 (Months 1-2)**: Core scoring engine, financial data scraping, and basic portfolio dashboard (MVP).
2. **Phase 4-6 (Months 2-3)**: CAS ingestion, AI narratives (Hybrid LLM), and Next.js frontend.
3. **Phase 7-9 (Months 3)**: AdvisorOS (B2B multi-tenancy), billing, compliance, and launch.
4. **Post-MVP**: RAG-based deep dives, multi-lingual support, real-time broker sync.

## Technical Constraints
- **Scaffold**: Must strictly utilize the existing FastAPI + Next.js 15 boilerplate (Taskiq, PydanticAI, Teams/Billing, Logfire).
- **Privacy**: DPDP Act compliance. PII (CAS data, portfolio holdings) must ONLY be processed by Local LLMs (Ollama). Public data (market ratios) can use Google Gemini.
- **Database**: PostgreSQL with TimescaleDB (time-series) and pgvector (future RAG).
- **Background Tasks**: Taskiq (async-native) for all heavy processing.

## Success Criteria (MVP)
- **Data**: Successfully scrape and ingest 5 years of historical fundamentals for Nifty 500 equities and all active mutual funds.
- **Performance**: Portfolio health score calculation completes in < 2 seconds.
- **Compliance**: Zero PII leakage to Tier 1 (Cloud) LLMs, verified by automated middleware tests.
- **Reliability**: 95% success rate on CAS (Consolidated Account Statement) parsing.

## Non-Goals (MVP)
- Retrieval-Augmented Generation (RAG) for narrative context (deferred to Post-MVP).
- Real-time WebSocket broker synchronization (deferred to Post-MVP).
- Execution/trading capabilities (platform is strictly analytics).

## Acceptance Criteria
- [ ] Document is saved to `.specify/specs/SPEC-01-01-project-constitution.md`.
- [ ] Document is approved and status changed to `active`.
- [ ] All subsequent specs reference this document for core objectives.
