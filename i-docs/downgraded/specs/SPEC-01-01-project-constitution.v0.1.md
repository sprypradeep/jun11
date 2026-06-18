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

## Purpose
This document defines the foundational purpose, objectives, constraints, and success criteria for Nivesh Pulse.

## Project Identity
- **Name**: Nivesh Pulse
- **Type**: B2C & B2B Fintech SaaS
- **Domain**: WealthTech / Investment Analytics
- **Target Market**: Indian retail and institutional investors

## Core Objective
Build an AI-native wealthtech platform that provides a "Health Score" (0-100) for investment portfolios, translating complex market signals into actionable insights while ensuring zero PII leakage to external cloud AI providers.

## Problem Statement
Retail investors face "choice paralysis" when evaluating portfolios. They lack objective, multi-factor analysis that combines quantitative metrics with qualitative insights in a privacy-compliant manner.

## Solution Overview
A scoring engine that evaluates investment instruments across 5 pillars (Quality, Value, Momentum, Growth, Risk) and aggregates them into portfolio-level health scores with AI-generated narratives.

## Key Objectives
1. **MVP (Month 1-2)**: Core scoring engine + basic portfolio dashboard
2. **Growth (Month 2-3)**: CAS ingestion + AI narratives + real-time broker sync
3. **Expansion (Month 4-5)**: Multi-lingual AI + RAG deep dives
4. **B2B Scale (Month 6)**: AdvisorOS multi-tenant API

## Success Criteria
- **Technical**: 99.5% uptime, <2s API response time, 95% CAS parse success rate
- **Business**: 1000 beta users in Month 3, 10 pilot advisors in Month 6
- **Compliance**: Zero DPDP violations, zero PII leakage to cloud LLMs

## Constraints
- **Regulatory**: DPDP Act compliance (India's data protection law)
- **Technical**: Must use scaffold boilerplate (FastAPI + Next.js + Taskiq)
- **Privacy**: Hybrid LLM strategy (Gemini for public data, Local LLM for PII)
- **Timeline**: 3-month MVP delivery

## Non-Goals (MVP)
- RAG-based narrative generation (deferred to Phase 3)
- Real-time broker sync (deferred to Phase 2)
- Multi-lingual support (deferred to Phase 3)

## Stakeholders
- **Primary**: Retail investors (B2C), Investment advisors (B2B)
- **Secondary**: Financial institutions (white-label)
- **Internal**: Solopreneur developer + AI agents

## Guiding Principles
1. **Spec-Driven**: No code without a spec
2. **Privacy-First**: PII never leaves secure environment
3. **Async-First**: All heavy operations via Taskiq
4. **Test-Driven**: Every spec includes test criteria
5. **Document-Driven**: Single source of truth, update as you go

## Dependencies
- **Scaffold**: vstorm-co/full-stack-ai-agent-template
- **Data Sources**: NSE/BSE, AMFI, Screener.in, CAMS/KFintech
- **Infrastructure**: PostgreSQL + TimescaleDB, Redis, vLLM/Ollama
- **AI**: PydanticAI, Google Gemini, Local LLMs

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|-----------|
| Data source API changes | High | Multi-source fallback, robust error handling |
| LLM hallucination in narratives | Medium | Structured output, human review loop |
| DPDP compliance gaps | Critical | PII sanitization middleware, audit trails |
| Performance bottlenecks | Medium | TimescaleDB, Redis caching, async processing |

## Approval
- **Author**: [Your Name]
- **Date**: 2026-06-12
- **Status**: Draft
