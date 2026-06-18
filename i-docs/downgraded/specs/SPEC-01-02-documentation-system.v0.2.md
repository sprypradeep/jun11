---
spec_id: SPEC-01-02
title: Documentation System
phase: 1
sequence: 2
status: Approved
owner: Platform Engineering
project: INIVESTEC
last_updated: 2023-10-27
---

# SPEC-01-02: Documentation System

## 1. Context & Background
To manage the 29-spec development chain of **INIVESTEC**, a rigorous, version-controlled documentation system is required. This ensures alignment across data engineering, AI, and frontend teams.

## 2. Goals & Non-Goals
### 2.1 Goals
- Implement a `github/spec-kit` compliant documentation workflow.
- Automate validation of specification chains and markdown formatting.
- Maintain a living record of Architecture Decision Records (ADRs).

### 2.2 Non-Goals
- Hosting external, customer-facing help center docs (handled separately post-MVP).

## 3. Tooling & Directory Structure
- **Engine**: MkDocs Material (with `mkdocs-spec-kit` plugin).
- **Repository Structure**:
  ```text
  /docs
    /specs
      /phase-01-foundation
        SPEC-01-01-project-constitution.md
        ...
      /phase-02-data-pipeline
    /adrs
      0001-record-architecture-decisions.md
      0002-choose-postgresql.md
    /api
      openapi.yaml
  ```

## 4. Workflow & Governance
1. **Drafting**: New specs are created as Drafts in a feature branch.
2. **Review**: Requires approval from at least one Domain Owner (e.g., Data Lead for SPEC-02-XX).
3. **Validation**: GitHub Actions will run `markdownlint` and a custom script to verify `spec_id` sequencing and YAML frontmatter validity.
4. **Amendments**: Post-approval changes require a minor version bump in the frontmatter and a changelog entry.

## 5. Non-Functional Requirements
- Documentation build time < 30 seconds.
- 100% of public/internal APIs must have auto-generated docs from code (e.g., FastAPI `/docs`).
