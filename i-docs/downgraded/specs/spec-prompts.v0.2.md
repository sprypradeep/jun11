# INIVESTEC: Master Specification Prompts

## 🌍 Global Context (Inject into every prompt)
> **Project Name**: INIVESTEC
> **Domain**: AI-powered Mutual Fund Portfolio Analysis, CAS (Consolidated Account Statement) Parsing, and AdvisorOS.
> **Core Constraints**: Strict adherence to India's DPDP Act (PII sanitization), high-accuracy financial data handling, scalable multi-tenant architecture, and hybrid LLM narrative generation.
> **Formatting Standard**: All outputs MUST adhere to `github/spec-kit` Software Design Document (SDD) formatting, including YAML frontmatter, clear hierarchical headings, Mermaid diagrams, and explicit Functional/Non-Functional Requirements.

---

## 📌 Phase 1: Foundation Prompts

### Prompt for SPEC-01-01: Project Constitution
```text
Act as a Principal Software Architect and Product Manager for INIVESTEC. 
Generate the "SPEC-01-01-project-constitution.md" document adhering strictly to github/spec-kit SDD formatting. 
Include YAML frontmatter (status, phase, owner, spec-id). 
Cover the following comprehensively:
1. Vision & Mission: AI-driven, privacy-first mutual fund portfolio analysis and AdvisorOS.
2. Core Principles: Data accuracy, DPDP compliance, scalability, and modularity.
3. Target Personas: Retail Investors, SEBI-RIAs (Registered Investment Advisors), and MF Distributors.
4. High-Level Tech Stack: Python/FastAPI (Backend), Next.js (Frontend), PostgreSQL (DB), Redis (Cache), Hybrid LLMs.
5. Out of Scope (for MVP): Direct brokerage execution, non-MF asset classes (unless specified).
Ensure no critical context regarding the 5-Pillar Scoring, CAS ingestion, or Multi-tenancy is lost.
```

---

### Prompt for SPEC-01-02: Documentation System
```text
Act as a DevOps/Platform Engineer for INIVESTEC. 
Generate "SPEC-01-02-documentation-system.md" adhering to github/spec-kit SDD formatting with YAML frontmatter.
Define the documentation architecture to support the 29-spec chain. Include:
1. Tooling: MkDocs Material or Docusaurus, integrated with github/spec-kit templates.
2. Directory Structure: `/docs`, `/specs` (with phase folders), `/adrs` (Architecture Decision Records).
3. Workflow: How specs are proposed, reviewed, and merged (e.g., RFC process).
4. Automation: CI/CD checks for markdown linting, broken links, and spec-chain validation.
5. Maintenance: Rules for updating specs when downstream dependencies (e.g., Database Schema) change.
```

---

### Prompt for SPEC-01-03: System Architecture
```text
Act as a Chief Technology Officer for INIVESTEC. 
Generate "SPEC-01-03-system-architecture.md" adhering to github/spec-kit SDD formatting with YAML frontmatter.
Detail the foundational architecture supporting all 9 phases. Include:
1. Architectural Style: Modular Monolith transitioning to Microservices (justification included).
2. Mermaid Diagram: High-level system context and container diagram showing: Client, API Gateway, CAS Parser, Data Pipeline, Scoring Engine, AI Narrative Service, and Database.
3. Component Breakdown: Responsibilities of each module (e.g., PII Sanitization Middleware must sit before any LLM or persistent storage).
4. Integration Points: External APIs (KFintech, CAMS, CDSL, Market Data providers).
5. Non-Functional Requirements: Latency targets, throughput for CAS parsing, and security boundaries.
```

---

### Prompt for SPEC-01-04: Database Schema
```text
Act as a Lead Database Architect for INIVESTEC. 
Generate "SPEC-01-04-database-schema.md" adhering to github/spec-kit SDD formatting with YAML frontmatter.
Define the foundational PostgreSQL schema. Include:
1. Design Principles: Normalization, PII segregation (DPDP compliance), and multi-tenancy (tenant_id on all core tables).
2. Core Entities (with fields, types, constraints, and indexes): 
   - `tenants` (AdvisorOS)
   - `users` (with role-based access)
   - `cas_uploads` (metadata, status, sanitization flags)
   - `holdings` & `transactions` (normalized MF data)
   - `portfolio_scores` (5-pillar scores, HHI, fee drag)
   - `narratives` (LLM outputs linked to portfolio snapshots)
3. Mermaid ER Diagram: Visual representation of relationships.
4. Data Lifecycle: Retention policies and soft-delete strategies.
```

---

*Note: Phase 2-9 prompts will be appended to this file as their respective specs are generated.*
