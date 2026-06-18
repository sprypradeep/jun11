---
id: SPEC-10-02
title: CI/CD Pipeline & Automated Governance
status: draft
phase: 10
sequence: 2
dependencies: [SPEC-01-02, SPEC-08-03, SPEC-10-01]
---

# CI/CD Pipeline & Automated Governance

## Overview
This specification defines the GitHub Actions workflows that automate testing, governance enforcement, and zero-downtime deployment. It ensures that the Spec-Driven Development (SDD) mandate is technically enforced before any code reaches production.

## Goals
1. Automate the execution of unit, integration, and security tests on every Pull Request.
2. Enforce the `verify_specs.py` and PII leakage checks as hard blockers for merging to `main`.
3. Automate the building, pushing, and deployment of Docker images upon merging to `main`.

## Requirements

### 10.1 Pull Request Validation (The Governance Gate)
- **Workflow**: `.github/workflows/pr-validation.yml`
- **Steps**:
  1. **Lint & Typecheck**: `ruff` (Python), `eslint` + `tsc` (TypeScript).
  2. **Spec-Kit Verification**: Run `python system_meta/scripts/verify_specs.py`. *Fail the build if orphan code is detected.*
  3. **Security Audit**: Run `pip-audit`, `npm audit`, and `bandit`.
  4. **Test Suite**: Run `pytest` (backend) and Playwright (frontend E2E). *Specifically assert that `test_pii_leakage.py` and `test_prompt_injection.py` pass.*

### 10.2 Automated Deployment (Continuous Delivery)
- **Workflow**: `.github/workflows/deploy.yml` (Triggers on push to `main`).
- **Steps**:
  1. **Build & Push**: Build Docker images and push to GitHub Container Registry (GHCR) or Docker Hub.
  2. **Database Migrations**: Run `alembic upgrade head` against the production database (using a secure, ephemeral runner environment).
  3. **Deploy Control Plane**: Trigger deployment webhooks for the PaaS (e.g., Railway/Render) to pull the new backend/frontend images.
  4. **Deploy AI Plane**: SSH into the GPU VPS, pull the new Ollama configuration (if changed), and restart the service.

### 10.3 Rollback Mechanism
- Maintain the previous stable Docker image tags.
- Include a manual `workflow_dispatch` trigger in GitHub Actions to instantly revert the PaaS deployment to the `latest-1` image tag in case of a critical post-deployment failure.

## Acceptance Criteria
- [ ] PR validation workflow successfully blocks a mock PR that introduces a Python file without a corresponding `.spec` entry.
- [ ] PR validation workflow successfully blocks a mock PR that fails the `test_pii_leakage.py` test.
- [ ] Deployment workflow successfully builds, pushes, and triggers the PaaS deployment webhook upon merging to `main`.
- [ ] Alembic migrations run automatically in the CI pipeline without manual intervention.
- [ ] A manual rollback workflow is present and tested.

## Technical Details
- **Secrets Management**: All production credentials (DB URLs, Stripe Keys, PaaS Webhooks) must be stored in GitHub Encrypted Secrets.
- **Runner Environment**: Use GitHub-hosted Ubuntu runners. Ensure the runner has access to the production DB *only* during the migration step via IP whitelisting or secure tunnels.
