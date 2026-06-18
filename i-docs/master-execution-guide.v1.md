# Master Execution Guide

## Overview
This document serves as the unified, phase-by-phase execution blueprint for building **INIVESTEC**, an AI-native wealthtech SaaS. It enforces a strict Specification-Driven Development (SDD) methodology, ensuring zero ambiguity, DPDP Act compliance, and architectural coherence from day one to beta launch.

## Overarching AI-Led SDLC Workflow
For every feature across all phases, the AI agent must follow this strict loop:
1. **Plan**: Review `state_of_build.json` and select the next task from `.specify/specs/`.
2. **Spec**: Create or update the `.spec` file. No code is written without a spec.
3. **Contextualize**: Inject the `.spec`, relevant boilerplate `howto` guides, and domain docs into the AI agent's context.
4. **Implement**: Execute via OpenCode (complex architecture) or Mistral Vibe (rapid feature building), adhering strictly to scaffold patterns.
5. **Verify**: Run `pytest` and `system_meta/scripts/verify_specs.py`. Halt on any sync error.
6. **Sync**: Atomically commit code, updated specs, and `trace_log.json` in a single commit.

---

### Phase 1: Foundation
* **Objective**: Initialize governance, architectural boundaries, and the layered database schema before writing business logic.
* **Execution Strategy**: Establish the `/system_meta/` governance layer. Extend, do not replace, the boilerplate's baseline docs. Map the scaffold's existing features to INIVESTEC's domain.
* **Technical Details**: 
  - Use `spec-kit` to initialize the `.specify/` directory.
  - Database: PostgreSQL with `timescaledb` and `pgvector` extensions enabled via Alembic migrations.
  - Architecture: Document the Hybrid LLM strategy (Gemini for public data, Local Ollama for PII) in an Architecture Decision Record (ADR).

### Phase 2: Data Pipeline
* **Objective**: Build resilient, asynchronous web scrapers and ingestion pipelines for Indian market data (NSE/BSE, AMFI, Screener.in).
* **Execution Strategy**: Build deterministic parsers first. Rely on robust error handling and schema drift detection rather than fragile AI-based scraping.
* **Technical Details**: 
  - Use `httpx` with exponential backoff and `python-magic` for MIME validation.
  - Parse using `pdfplumber` and `pandas`.
  - Ingest via Taskiq workers into TimescaleDB hypertables (`market_data_daily`, `fundamentals_daily`).
  - Enforce strict Pydantic V2 validators for data quality (e.g., OHLC logic, ratio bounds).

### Phase 3: Scoring Engine
* **Objective**: Transform raw financial data into the standardized 0–100 Health Score across 5 pillars, including portfolio aggregation and risk penalties.
* **Execution Strategy**: Prioritize vectorized operations (Pandas/NumPy) for performance. Calculate Z-scores against dynamic peer groups, not the entire market.
* **Technical Details**: 
  - Apply Winsorization (1st/99th percentiles) before Z-score calculation to cap outliers.
  - Aggregate using value-weighted averages for portfolios.
  - Apply deterministic penalties: Herfindahl-Hirschman Index (HHI) for sector concentration, and weighted Expense Ratio for fee drag.
  - Cache daily instrument scores in Redis (24h TTL).

### Phase 4: CAS Ingestion
* **Objective**: Build a privacy-first ingestion engine for Consolidated Account Statements (CAMS, KFintech, CDSL) with strict DPDP compliance.
* **Execution Strategy**: Use deterministic Regex/structured extraction. AI (Local LLM) is reserved *only* as a fallback for highly unstructured edge cases, never for primary parsing.
* **Technical Details**: 
  - Abstract base class `BaseCASParser` for plugin-style registrar support.
  - Fuzzy matching (`thefuzz`, cutoff=90) to map extracted scheme names to internal ISINs.
  - **Critical**: `PIISanitizationMiddleware` with pre-compiled Regex to mask PAN, Email, Phone, and Folio numbers before they hit logs or Taskiq queues.

### Phase 5: AI & Narratives
* **Objective**: Translate quantitative scores into human-readable, actionable insights using a privacy-compliant, hybrid LLM routing strategy.
* **Execution Strategy**: Enforce strict data classification. PII-bearing payloads must *never* route to cloud LLMs.
* **Technical Details**: 
  - `LLMRouter` middleware inspects payloads. Routes to `PublicDataAgent` (Google Gemini) or `PrivateDataAgent` (Local Ollama via `http://ollama:11434`).
  - PydanticAI agents must enforce structured output (`NarrativeResponse` schema) to ensure frontend compatibility.
  - Deliver narratives via FastAPI `StreamingResponse` (Server-Sent Events) for a premium UX.

### Phase 6: Frontend
* **Objective**: Build a world-class, responsive Next.js 15 UI that visualizes scores, facilitates secure CAS uploads, and streams AI insights.
* **Execution Strategy**: Leverage Next.js App Router patterns: Server Components for initial data fetching, Client Components for interactivity (charts, uploads, SSE).
* **Technical Details**: 
  - State/Data: `@tanstack/react-query` with skeleton loaders.
  - Charts: `recharts` (memoized to prevent unnecessary re-renders).
  - Uploads: `react-dropzone` with strict client-side validation, polling Taskiq status via custom hooks.

### Phase 7: AdvisorOS (B2B)
* **Objective**: Activate multi-tenant capabilities for investment advisors to manage clients, create model portfolios, and generate white-labeled reports.
* **Execution Strategy**: **Do not build custom multi-tenancy.** Strictly leverage the scaffold’s existing `Teams`, `Members`, and `Roles` infrastructure.
* **Technical Details**: 
  - Enforce application-level data scoping: All advisor queries must filter by `team_id` via a `get_current_team_context` dependency.
  - PDF Generation: `WeasyPrint` + `Jinja2` templates, injected with dynamic `brand_logo_url` and `brand_color_hex` from team settings.
  - Delivery: Asynchronous Taskiq job sending via Resend email or secure download link.

### Phase 8: Billing & Compliance
* **Objective**: Finalize commercial monetization and regulatory foundations prior to launch.
* **Execution Strategy**: Treat compliance as hard-coded constraints, not afterthoughts. Ensure atomic operations for financial transactions (credits).
* **Technical Details**: 
  - `CreditManager` service using PostgreSQL transactions for atomic reserve/consume/refund logic tied to Taskiq success/failure.
  - DPDP: Explicit consent gates, automated data retention/anonymization cron jobs, and secure erasure/export endpoints.
  - Security: CI/CD integration of `pip-audit`, `gitleaks`, and rigorous prompt injection/PII leakage test suites.

### Phase 9: Admin & Operations Command Center
* **Objective**: Augment boilerplate admin routes to provide the solopreneur with full operational control, monitoring, and dynamic configuration.
* **Execution Strategy**: Strictly separate admin data from tenant data. Admin views must show aggregated metrics or anonymized operational states, never raw PII.
* **Technical Details**: 
  - Audit UI: Paginated views for security logs, DPDP erasure requests, and CAS schema drift alerts.
  - Observability: Redis-backed Taskiq queue depth monitoring and TimescaleDB data freshness checks.
  - CMS: Database-backed `site_content` table with Next.js ISR `revalidateTag` for zero-downtime content updates.
  - Config Engine: Dynamic adjustment of scoring parameters (e.g., HHI thresholds) cached in Redis, with manual re-scoring triggers.

### Phase 10: Deployment & Operational Readiness
* **Objective**: Transition to a secure, highly available, and scalable production infrastructure with automated governance.
* **Execution Strategy**: Infrastructure as Code. Manual server configuration is prohibited. Enforce split-topology deployment to optimize costs.
* **Technical Details**: 
  - Containerization: Multi-stage Dockerfiles. Next.js `standalone` output (<150MB).
  - Topology: CPU PaaS (Web/Taskiq/DB) + Dedicated GPU VPS (Ollama), connected via secure internal tunnel (e.g., Tailscale). Nginx explicitly denies external access to port 11434.
  - CI/CD: GitHub Actions enforcing `verify_specs.py`, security scans, and automated Alembic migrations on merge to `main`.
  - Readiness: Locust load testing, Redis-backed feature flags (kill switches), and comprehensive operational runbooks.

---
---
