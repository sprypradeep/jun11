# Solopreneur Execution Checklist & Golden Rules

## Overview
As a solopreneur leveraging AI agents, your greatest risks are scope creep, hallucinated code, and silent security failures. This checklist distills the critical, non-negotiable actions and "gotchas" for each phase of building **INIVESTEC**.

### Phase 1: Foundation
- [ ] **Spec-First Mandate**: Refuse to let the AI write a single line of business logic until `SPEC-01-01` through `SPEC-01-04` are marked `active`.
- [ ] **Migration Verification**: Manually inspect the generated Alembic migration file. Ensure TimescaleDB `create_hypertable` commands are present and correctly ordered after table creation.

### Phase 2: Data Pipeline
- [ ] **Mock Data First**: Before running scrapers against live websites, create static HTML/CSV fixtures in `tests/fixtures/`. Have the AI write and pass tests against these fixtures first.
- [ ] **Regex Validation**: Do not trust the AI's first attempt at financial Regex. Verify PAN, ISIN, and ratio patterns manually on Regex101 before committing.

### Phase 3: Scoring Engine
- [ ] **Trust but Verify Math**: AI agents are notoriously bad at complex financial math. Manually calculate the expected Z-score and HHI penalty for 2-3 mock portfolios. Write `pytest` assertions that *exactly* match your manual calculation.
- [ ] **Performance Watch**: If the Taskiq Z-score job takes > 5 seconds for 500 instruments, force the AI to optimize Pandas operations (e.g., use `groupby().transform()` instead of `apply()`).

### Phase 4: CAS Ingestion
- [ ] **Fixture Preparation**: Manually sanitize 2-3 real CAMS and CDSL PDFs/Excel files and place them in `tests/fixtures/cas/`. The AI needs these to write accurate parsing logic.
- [ ] **The Ultimate Gate**: The `test_pii_leakage.py` test is your most critical security control. Run it after *every* code change in the CAS module. If it fails, halt all development until the leak is plugged.

### Phase 5: AI & Narratives
- [ ] **Mock LLM Responses**: Use `pydantic_ai.models.test` to verify the agents correctly parse mock LLM responses into the structured `NarrativeResponse` schema before connecting to real Ollama/Gemini endpoints.
- [ ] **Isolation Check**: Verify that the `LLMRouter` throws a hard `PIIRoutingError` (returning 503) when Ollama is down, rather than silently falling back to Gemini with PII data.

### Phase 6: Frontend
- [ ] **Build Against Mocks**: Create a `frontend/mocks/` directory with JSON responses matching the backend specs. Build and test the UI against these mocks for rapid iteration before wiring up the real API.
- [ ] **SSE Resilience**: Test the narrative streaming hook by intentionally throttling the network in Chrome DevTools. Ensure the UI doesn't freeze and handles partial chunks gracefully.

### Phase 7: AdvisorOS
- [ ] **Leverage the Scaffold**: Do not write custom multi-tenancy. Rigorously use the scaffold's `teams` and `team_members` tables. The `get_current_team_context` dependency is your primary security control.
- [ ] **PDF Rendering Quirks**: WeasyPrint does not support modern CSS (Flexbox/Grid) perfectly. Use simple, table-based or block-based layouts with inline styles for the PDF template. Test locally first.

### Phase 8: Billing & Compliance
- [ ] **Atomic Transactions**: Ensure the `CreditManager` uses strict database transactions. If a Taskiq job crashes, the `refund_credits` logic *must* execute, or users will churn due to "phantom" deductions.
- [ ] **Consent is a Legal Shield**: Do not skip the explicit consent checkbox. Under the DPDP Act, explicit, auditable consent for financial data processing is your primary legal defense.
- [ ] **Rate Limit Your Wallet**: Ensure rate limits are tight on AI and upload endpoints. A malicious actor could otherwise spin up thousands of tasks, crippling your server.

### Phase 9: Admin & Operations
- [ ] **Admin Route Protection**: Ensure Next.js middleware *and* FastAPI dependencies strictly check for the `ADMIN` role. Frontend-only checks are easily bypassed.
- [ ] **Beware "God Mode"**: Changing scoring parameters on the fly (SPEC-09-04) must be logged in the `audit_logs`. If a user's score drops, you must be able to prove it was due to a config change, not a bug.
- [ ] **Cache Invalidation**: When testing the CMS, verify that `revalidateTag` or `revalidatePath` is correctly targeting the exact route segment, or changes won't appear on the public site.

### Phase 10: Deployment & Readiness
- [ ] **The GPU Cost Trap**: Ensure your GPU VPS (for Ollama) is monitored for VRAM utilization. Running an A10G or RTX 4090 24/7 will drain your runway if it silently OOM-crashes or idles unnecessarily.
- [ ] **Test the Rollback**: Before opening the beta, intentionally deploy a broken image via CI/CD, and execute the `rollback.yml` GitHub Action. You must know your exact Recovery Time Objective (RTO).
- [ ] **DPDP Breach Protocol**: Do not skip writing the `dpdp_breach_protocol.md` runbook. Have the legal templates for user/board notification pre-drafted and stored offline.
- [ ] **Feature Flags are Your Safety Net**: If the Local LLM hallucinates or the CAS parser breaks, use the Redis-backed feature flags to instantly disable the feature. It is better to show "Temporarily Unavailable" than to deliver broken financial insights.

---

## The Solopreneur's Golden Rules for AI-Led SDLC

1. **The Spec is the Master, Code is the Slave**: If the AI writes code that deviates from the spec, do not just accept the code. Update the spec first to reflect the new reality, then regenerate the code.
2. **Atomic Context Injection**: AI agents fail when given too much context. Do not ask OpenCode to "build the portfolio feature." Inject *only* the specific `.spec` file, the relevant database models, and the specific `howto` guide.
3. **No Orphan Code**: Enforce the `verify_specs.py` pre-commit hook religiously. If a function or route exists without a corresponding `.spec` entry, the build must fail.
4. **Test-Driven Verification**: Force the AI to write `pytest` tests based on the spec *before* it writes the implementation. If the tests pass, the implementation is mathematically aligned with the spec.
5. **Update-as-you-go Docs**: Treat documentation as code. If you change a Taskiq queue name or a scoring threshold, update the relevant `.spec` and `/docs/` file in the exact same commit. Never let documentation lag behind the codebase.
