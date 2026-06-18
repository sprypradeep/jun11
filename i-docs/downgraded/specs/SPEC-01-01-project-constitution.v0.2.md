---
spec_id: SPEC-01-01
title: Project Constitution
phase: 1
sequence: 1
status: Approved
owner: Core Architecture Team
project: INIVESTEC
last_updated: 2023-10-27
---

# SPEC-01-01: Project Constitution

## 1. Context & Background
**INIVESTEC** is an AI-powered, privacy-first portfolio analysis and AdvisorOS platform tailored for the Indian mutual fund ecosystem. It ingests Consolidated Account Statements (CAS), normalizes financial data, applies a proprietary 5-Pillar scoring logic, and generates AI-driven narratives for both retail investors and SEBI-Registered Investment Advisors (RIAs).

## 2. Goals & Non-Goals
### 2.1 Goals
- Establish a single source of truth for project vision, principles, and boundaries.
- Ensure foundational alignment with India's Digital Personal Data Protection (DPDP) Act.
- Define the core technology stack to support scalable CAS ingestion and AI narrative generation.

### 2.2 Non-Goals
- Direct execution of trades or brokerage integrations (out of scope for MVP).
- Support for non-MF asset classes (e.g., direct equity, crypto) in Phase 1-3.

## 3. Core Principles
1. **Privacy by Design**: PII must be sanitized *before* reaching any LLM or non-essential storage (see SPEC-04-03).
2. **Deterministic Scoring**: The 5-Pillar scoring engine (SPEC-03-02) must be 100% reproducible and auditable.
3. **Multi-Tenant First**: All data models and APIs must natively support `tenant_id` segregation (SPEC-07-01).

## 4. High-Level Technology Stack
- **Backend**: Python 3.11+, FastAPI (async, high-performance).
- **Frontend**: Next.js 14+ (App Router), TailwindCSS, Shadcn/UI.
- **Database**: PostgreSQL 15+ (with `pgvector` for future RAG capabilities).
- **Cache/Queue**: Redis (for job queuing and caching market data).
- **AI/LLM**: Hybrid strategy (Open-source local models for PII-safe tasks, premium APIs for narrative refinement) via PydanticAI (SPEC-05-02).

## 5. Success Metrics
- CAS parsing success rate > 95%.
- PII leakage incidents = 0.
- API response time for portfolio scoring < 2 seconds (post-ingestion).
