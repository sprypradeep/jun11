---
id: SPEC-01-02
title: Documentation System
status: draft
phase: 1
sequence: 2
dependencies: [SPEC-01-01]
---

# Documentation System

## Overview
This specification establishes the "Single Source of Truth" documentation and governance framework for INIVESTEC. It defines how documentation is structured, updated, and enforced to support Specification-Driven Development (SDD).

## Directory Structure
The documentation is split into three distinct layers to prevent collision with the boilerplate scaffold:

### 1. User/Developer Facing (Boilerplate Extended)
Located at the root and `/docs/`. We extend, do not replace, boilerplate files.
- `AGENTS.md`, `CLAUDE.md`, `ENV_VARS.md`, `SECURITY.md` (Extended with INIVESTEC specifics).
- `/docs/architecture.md`, `/docs/deploy.md`, `/docs/testing.md`.
- `/docs/howto/` (Extended with domain-specific guides like `add-data-scraper.md`).

### 2. Domain Knowledge
Located at `/docs/domain/`.
- `scoring_model.md`: Mathematical formulas for Z-scores, HHI, Fee Drag.
- `dpdp_compliance.md`: PII handling rules and data classification.
- `tiered_llm_strategy.md`: Routing logic for Gemini vs. Local LLM.

### 3. Governance & Traceability (The SDD Layer)
Located at `/system_meta/`.
- `master_governance_protocol.md`: The 12-point SDD mandate.
- `/system_meta/adr/`: Architecture Decision Records.
- `/system_meta/trace/`: `trace_log.json`, `state_of_build.json`.
- `/system_meta/scripts/`: Automation for spec verification.

## Documentation Update Protocol
1. **Atomicity**: Code changes and documentation updates must occur in the same commit.
2. **Spec-First**: No code is written without a corresponding `.specify/specs/` entry.
3. **Traceability**: All AI agent executions that modify code must append to `trace_log.json`.
4. **Verification**: A pre-commit hook runs `verify_specs.py` to ensure no orphan code exists.

## Extension Convention
When modifying boilerplate files (e.g., `AGENTS.md`), use HTML comments to demarcate additions:
```html
<!-- INIVESTEC-EXTENSION-START -->
[Additions here]
<!-- INIVESTEC-EXTENSION-END -->
```

## Acceptance Criteria
- [ ] `/system_meta/` directory structure is created with all subdirectories.
- [ ] `master_governance_protocol.md` is written and saved.
- [ ] `AGENTS.md` and `CLAUDE.md` are extended using the HTML comment convention.
- [ ] `verify_specs.py` script is created and functional.
- [ ] `trace_log.json` and `state_of_build.json` are initialized.
