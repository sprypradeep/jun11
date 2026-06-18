
# Phase 1 Master Execution Guide

**Objective**: Initialize the governance, architectural, and structural foundations of INIVESTEC before writing any business logic. This phase ensures the AI agent has strict boundaries, a single source of truth, and a clear map of the system.

**Execution Strategy**:
1. Initialize the `spec-kit` environment.
2. Execute the specifications sequentially (01-01 → 01-04).
3. Do not proceed to Phase 2 until all Phase 1 acceptance criteria are met and verified.

### Master Initialization Prompt
*Use this prompt to initialize the spec-kit environment and set the context for the AI agent before running individual specs.*

```text
Initialize the spec-kit environment for project INIVESTEC. 
Context: INIVESTEC is an AI-native wealthtech SaaS providing a 0-100 "Health Score" for investment portfolios. It uses a FastAPI/Next.js 15 scaffold, Taskiq for background tasks, TimescaleDB for time-series data, and a Hybrid LLM strategy (Google Gemini for public data, Local Ollama for PII data) to ensure DPDP Act compliance. 

Create the `.specify/` directory structure. 
Set the project constitution as the root context. 
Acknowledge that we are beginning Phase 1: Foundation. 
Await the first specification prompt (SPEC-01-01).
```

---

### **Prompt for SPEC-01-01**
```text
Execute SPEC-01-01: Project Constitution for INIVESTEC.
1. Create the file `.specify/specs/SPEC-01-01-project-constitution.md` using the exact markdown structure provided.
2. Update the project's root `README.md` to include a brief summary of INIVESTEC and a link to this constitution.
3. Update `AGENTS.md` and `CLAUDE.md` to explicitly state that INIVESTEC's core mandate is DPDP compliance via a Hybrid LLM strategy.
4. Mark SPEC-01-01 status as `active` in the spec-kit registry.
```

---

### **Prompt for SPEC-01-02**
```text
Execute SPEC-01-02: Documentation System for INIVESTEC.
1. Create the `/system_meta/` directory structure including `adr/`, `trace/`, and `scripts/`.
2. Write `/system_meta/master_governance_protocol.md` detailing the atomicity, spec-first, and traceability rules.
3. Initialize `/system_meta/trace/trace_log.json` and `state_of_build.json` with empty/zero states.
4. Open `AGENTS.md` and `CLAUDE.md`. Append the INIVESTEC Hybrid LLM and DPDP compliance rules using the `<!-- INIVESTEC-EXTENSION-START -->` convention.
5. Create `/system_meta/scripts/verify_specs.py` that scans the `backend/` and `frontend/` directories and flags any Python/TS files that do not have a corresponding spec in `.specify/specs/`.
6. Mark SPEC-01-02 as `active`.
```

---

### **Prompt for SPEC-01-03**
```text
Execute SPEC-01-03: System Architecture for INIVESTEC.
1. Update `/docs/architecture.md` with the micro-modular architecture diagram and component mapping defined in the spec.
2. Create `/system_meta/adr/001_hybrid_llm_strategy.md` explaining the PII-based routing between Google Gemini and Local Ollama.
3. Create `/system_meta/adr/002_teams_for_advisoros.md` explaining how the scaffold's Teams/Billing features are repurposed for the B2B AdvisorOS module.
4. Modify the root `docker-compose.yml` to add an `ollama` service (image: `ollama/ollama`) mapped to port 11434, ensuring it shares a network with the FastAPI backend.
5. Mark SPEC-01-03 as `active`.
```

---

### **Prompt for SPEC-01-04**
```text
Execute SPEC-01-04: Database Schema for INIVESTEC.
1. Generate an Alembic migration file `backend/alembic/versions/001_add_inivestec_schema.py` that creates all tables for Layers 1, 2, and 3.
2. Ensure the migration includes the SQL commands to enable TimescaleDB and convert `market_data_daily` and `fundamentals_daily` into hypertables.
3. Generate SQLAlchemy ORM models for all new tables in `backend/app/models/` (e.g., `instrument.py`, `portfolio.py`, `market_data.py`). Ensure they use `asyncpg` compatible syntax.
4. Create `/docs/domain/data_dictionary.md` documenting every table, column, data type, and its business purpose.
5. Run the migration against the local development database to verify no syntax errors exist.
6. Mark SPEC-01-04 as `active`.
```

---

### **Prompt for SPEC-02-01**
```text
Implement SPEC-02-01: Financial Data Scrapers for INIVESTEC. 
1. Create a `BaseScraper` abstract class in `backend/app/services/scrapers/base.py` with async httpx, exponential backoff, and Logfire tracing.
2. Implement `ScreenerScraper` to parse equity fundamentals (PE, PB, ROE, etc.) from Screener.in HTML pages. Include a mechanism to detect HTML schema drift.
3. Implement `AMFIScraper` to download and parse AMFI's daily NAV text file and portfolio disclosure Excel files.
4. Write comprehensive pytest unit tests using static HTML/CSV fixtures in `tests/test_scrapers/`.
5. Update `docs/howto/add-data-scraper.md` with instructions on how to add a new scraper.
Ensure all code is async-native and follows the project's dependency injection patterns.
```

---

### **Prompt for SPEC-02-02**
```text
Implement SPEC-02-02: Market Data Ingestion Pipeline for INIVESTEC.
1. Create Taskiq tasks in `backend/app/tasks/market_data/` for downloading and parsing NSE/BSE daily bhav copies.
2. Create Taskiq tasks in `backend/app/tasks/fundamentals/` to orchestrate the Screener and AMFI scrapers.
3. Implement repository methods in `backend/app/repositories/market_data.py` and `fundamentals.py` using asyncpg for high-performance bulk upserts into TimescaleDB hypertables.
4. Configure Taskiq queues and dead-letter queues (DLQ) for failed parsing jobs.
5. Write integration tests using `pytest-asyncio` to verify the end-to-end flow from mock CSV download to database insertion.
6. Update `docs/howto/add-background-task.md` with the specific queue configurations for INIVESTEC.
```

---

### **Prompt for SPEC-02-03**
```text
Implement SPEC-02-03: Data Quality & Validation for INIVESTEC.
1. Create strict Pydantic V2 models in `backend/app/schemas/data_validation.py` with custom validators for OHLC logic, ratio bounds, and volume checks.
2. Integrate these validators into the ingestion pipeline (SPEC-02-02) so invalid records are rejected and logged before DB insertion.
3. Create a Taskiq reconciliation task in `backend/app/tasks/quality/reconcile.py` that checks for missing trading days using an NSE holiday calendar and performs cross-source verification (AMFI ETF NAV vs NSE Close).
4. Implement anomaly detection logic to flag ±20% daily price jumps and stale fundamental data (>90 days).
5. Configure Logfire metrics to track parsing success rates, validation failures, and reconciliation mismatches.
6. Write pytest tests to ensure all validation rules correctly accept valid data and reject invalid data.
```

---

### Prompt for SPEC-03-01
```text
Execute SPEC-03-01: Z-Score Normalization Engine for INIVESTEC.
1. Create `backend/app/services/scoring/zscore_calculator.py` implementing vectorized Pandas/NumPy logic for peer-group grouping, Winsorization (1st/99th percentiles), and Z-score calculation.
2. Implement edge-case handling for StdDev=0, NULL values, and insufficient history.
3. Create a Taskiq task `backend/app/tasks/scoring/calculate_zscores.py` that fetches the latest `fundamentals_daily` data, runs the calculator, and upserts results into the `instrument_scores` table.
4. Implement Redis caching for the calculated Z-scores (24h TTL).
5. Write comprehensive `pytest` unit tests using synthetic DataFrames to verify Winsorization and edge-case handling.
6. Mark SPEC-03-01 as `active`.
```

---

### Prompt for SPEC-03-02
```text
Execute SPEC-03-02: 5-Pillar Scoring Logic for INIVESTEC.
1. Create `backend/app/config/scoring_config.py` defining the metric-to-pillar mappings and directional inversion flags.
2. Implement `backend/app/services/scoring/pillar_calculator.py` to aggregate Z-scores, apply inversions, and scale the result to a 0-100 clamped range.
3. Update the Taskiq scoring pipeline to calculate all 5 pillar scores and the `overall_health_score`, then upsert into `instrument_scores`.
4. Write `pytest` tests validating the math: ensure a mock instrument with Z-scores of [0, 0, 0, 0, 0] yields exactly 50 for all pillars and overall.
5. Update `/docs/domain/scoring_model.md` with the exact formulas and metric mappings defined here.
6. Mark SPEC-03-02 as `active`.
```

---

### Prompt for SPEC-03-03
```text
Execute SPEC-03-03: Portfolio Aggregation for INIVESTEC.
1. Create `backend/app/services/scoring/portfolio_aggregator.py` implementing the value-weighted average logic for holdings.
2. Implement the fallback logic for missing `last_valuation_price` and the >50% unscored weight `UNRELIABLE` flag.
3. Create a Taskiq task `backend/app/tasks/scoring/aggregate_portfolios.py` that fetches all active portfolios, runs the aggregator, and bulk upserts into `portfolio_scores`.
4. Write `pytest` tests verifying the weighted average math and the unscored holding exclusion logic.
5. Ensure the repository method uses efficient async SQLAlchemy queries to fetch holdings and instrument scores in a single batch per portfolio.
6. Mark SPEC-03-03 as `active`.
```

---

### Prompt for SPEC-03-04
```text
Execute SPEC-03-04: Penalty Calculations (HHI, Fee Drag) for INIVESTEC.
1. Create `backend/app/services/scoring/penalty_calculator.py` implementing the HHI sector concentration logic and the weighted Expense Ratio logic with the exact tiered penalty formulas specified.
2. Integrate this calculator into the `portfolio_aggregator.py` Taskiq flow, ensuring penalties are subtracted and the final score is clamped to >= 0.
3. Update the `portfolio_scores` upsert logic to include `hhi_index`, `hhi_penalty`, and `fee_drag_penalty`.
4. Write rigorous `pytest` tests for the penalty formulas, specifically testing the boundary conditions (0.15, 0.25 HHI; 1.0%, 1.5% ER).
5. Update the API schema in `backend/app/schemas/portfolio.py` to expose these penalty breakdowns to the frontend.
6. Update `/docs/domain/scoring_model.md` with the penalty formulas.
7. Mark SPEC-03-04 as `active`.
```

---

### Prompt for SPEC-04-01
```text
Execute SPEC-04-01: CAS Parser Framework for INIVESTEC.
1. Create `backend/app/schemas/cas.py` defining `HoldingExtractionDTO` (isin, quantity, avg_cost, current_value) and `CASMetadataDTO` (statement_date, registrar) with strict Pydantic validation.
2. Create `backend/app/services/cas/base_parser.py` defining the `BaseCASParser` ABC with `detect_format`, `extract_holdings`, and `extract_metadata` methods.
3. Implement the `POST /api/v1/portfolios/{portfolio_id}/cas/upload` endpoint using `python-magic` for MIME verification, enforcing a 25MB limit, and saving to `/tmp/cas_uploads/` with a UUID filename.
4. Create the Taskiq task `backend/app/tasks/ingestion/process_cas.py` that orchestrates parser detection, execution, Redis state updates, and idempotent upserts.
5. Create a daily Taskiq cron task `backend/app/tasks/ingestion/cleanup_temp_files.py` to delete files older than 24 hours.
6. Write integration tests verifying the upload validation, Taskiq routing, and idempotent upsert logic using a mock parser.
7. Mark SPEC-04-01 as `active`.
```

---

### Prompt for SPEC-04-02
```text
Execute SPEC-04-02: CAMS/KFintech/CDSL Parsers for INIVESTEC.
1. Create `backend/app/services/cas/cams_parser.py` and `backend/app/services/cas/cdsl_parser.py` inheriting from `BaseCASParser`.
2. Implement `pdfplumber` table extraction and Regex fallback logic for ISIN, units, and avg cost.
3. Implement a fuzzy-matching service in `backend/app/services/cas/mapping_service.py` using `thefuzz` to map extracted scheme names to the `instruments` table (cutoff=90).
4. Update the `portfolios` SQLAlchemy model to include an `unmapped_holdings` JSONB column.
5. Create static test fixtures in `tests/fixtures/cas/` (mock PDFs/Excel) and write `pytest` tests verifying >95% extraction accuracy and correct ISIN mapping.
6. Add Logfire alerting for `CAS_SCHEMA_DRIFT` when extraction yields zero valid holdings.
7. Mark SPEC-04-02 as `active`.
```

---

### Prompt for SPEC-04-03
```text
Execute SPEC-04-03: PII Sanitization Middleware for INIVESTEC.
1. Create `backend/app/middleware/pii_sanitizer.py` with pre-compiled Regex patterns and masking logic for PAN, Email, Phone, and Folio.
2. Implement a FastAPI middleware `PIISanitizationMiddleware` that applies this sanitization to request/response bodies for CAS-related endpoints.
3. Configure Logfire scrubbing in `backend/app/core/logfire_config.py` to automatically mask these patterns in all traces.
4. Write a rigorous `tests/test_security/test_pii_leakage.py` that injects mock PII into the CAS parsing flow and asserts that the `trace_log.json` and mock logs contain ZERO raw PII.
5. Update `/docs/domain/dpdp_compliance.md` with the exact masking rules and the "Local LLM Only" mandate for PII-bearing data.
6. Mark SPEC-04-03 as `active`.
```

---

### Prompt for SPEC-05-01
```text
Execute SPEC-05-01: Hybrid LLM Strategy & Routing for INIVESTEC.
1. Create `backend/app/services/ai/llm_router.py` that integrates with `PIISanitizer` to classify payloads and route them to either `PublicDataAgent` or `PrivateDataAgent`.
2. Configure `PrivateDataAgent` in PydanticAI to use the local Ollama endpoint (`http://ollama:11434/v1`).
3. Implement strict fallback logic: if Ollama is unreachable, raise a `PIIRoutingError` that returns a 503 response, never falling back to Gemini for PII data.
4. Write `pytest` tests mocking the `PIISanitizer` and `httpx` to verify correct routing and degradation behavior.
5. Update `/docs/domain/tiered_llm_strategy.md` with the routing flowchart and compliance rules.
6. Mark SPEC-05-01 as `active`.
```

---

### Prompt for SPEC-05-02
```text
Execute SPEC-05-02: PydanticAI Agents for INIVESTEC.
1. Create `backend/app/agents/prompts.py` containing the system prompts for `PublicDataAgent` and `PrivateDataAgent`.
2. Create `backend/app/agents/schemas.py` defining the `NarrativeResponse` Pydantic model (summary, key_risks, key_strengths, action_items).
3. Implement `backend/app/agents/public_agent.py` and `backend/app/agents/private_agent.py` using PydanticAI, enforcing the `NarrativeResponse` result type.
4. Write `pytest` tests using `pydantic_ai.models.test` to verify the agents correctly parse mock LLM responses into the structured schema.
5. Configure Logfire to trace agent execution time and token usage.
6. Mark SPEC-05-02 as `active`.
```

---

### Prompt for SPEC-05-03
```text
Execute SPEC-05-03: Narrative Generation Engine for INIVESTEC.
1. Create `backend/app/services/ai/narrative_service.py` that fetches `portfolio_scores`, constructs the sanitized context string, and calls the `PrivateDataAgent`.
2. Implement Redis caching for the generated narrative (7-day TTL) with cache invalidation logic.
3. Create the `GET /api/v1/portfolios/{portfolio_id}/narrative/stream` endpoint using FastAPI's `StreamingResponse` for SSE.
4. Integrate credit deduction logic (mocked for now, per SPEC-08-01) upon successful narrative generation.
5. Write integration tests verifying the context construction, LLM call, caching behavior, and SSE endpoint.
6. Update `/docs/domain/rag_pipeline.md` (as a precursor) to note that MVP narratives are metric-driven, with RAG context to be added in Post-MVP.
7. Mark SPEC-05-03 as `active`.
```

---

### Prompt for SPEC-06-01
```text
Execute SPEC-06-01: Dashboard UI for INIVESTEC.
1. Set up the core Next.js 15 App Router layout (`frontend/app/layout.tsx`) with a responsive sidebar and top bar, integrating the scaffold's auth and team-switching components.
2. Create `frontend/app/dashboard/page.tsx` as a Server Component that fetches initial portfolio data, passing it to Client Components for interactivity.
3. Implement `frontend/components/dashboard/HealthScoreGauge.tsx` (animated radial progress), `PillarRadarChart.tsx` (using `recharts`), and `ScoreHistoryChart.tsx` (AreaChart).
4. Implement `frontend/components/dashboard/HoldingsTable.tsx` with sortable columns and color-coded Health Score badges.
5. Wrap the application in a `QueryClientProvider` and create custom React Query hooks (e.g., `usePortfolioScore`) with skeleton loading states.
6. Write Playwright or React Testing Library tests to verify the rendering of charts and conditional penalty callouts based on mock API data.
7. Mark SPEC-06-01 as `active`.
```

---

### Prompt for SPEC-06-02
```text
Execute SPEC-06-02: CAS Upload Flow for INIVESTEC.
1. Create `frontend/components/cas/CASUploadZone.tsx` using `react-dropzone` with strict client-side validation (25MB, pdf/xlsx/csv).
2. Implement the upload mutation using React Query, capturing the returned `task_id`.
3. Create a `useTaskStatus` custom hook that polls `GET /api/v1/tasks/{task_id}/status` every 2 seconds, handling `PENDING`, `PROCESSING`, `COMPLETED`, and `FAILED` states with appropriate UI feedback (spinners, progress bars, error toasts).
4. Build the `frontend/components/cas/UnmappedHoldingsResolver.tsx` component, featuring a searchable dropdown (using backend instrument search API) to manually map unrecognized schemes to valid ISINs.
5. Write React Testing Library tests simulating the drag-and-drop validation, polling state transitions, and the unmapped holdings resolution flow.
6. Mark SPEC-06-02 as `active`.
```

---

### Prompt for SPEC-06-03
```text
Execute SPEC-06-03: AI Insights Panel for INIVESTEC.
1. Create `frontend/hooks/useNarrativeStream.ts`, a custom hook that manages the `EventSource` or `ReadableStream` connection to the backend SSE endpoint, handling chunk accumulation and final JSON parsing.
2. Build `frontend/components/ai/NarrativePanel.tsx` with distinct, styled sections for Executive Summary, Key Strengths (green), Key Risks (red), and Action Items.
3. Implement a "Generate Insights" button that displays the credit cost, triggers the stream, and shows a typing/skeleton loader during `isStreaming`.
4. Add error handling to gracefully display the custom 503 "AI analyst resting" message if the backend Local LLM is unreachable.
5. Integrate a toast notification system to confirm credit deduction upon successful generation.
6. Write React Testing Library tests mocking the `ReadableStream` to verify the progressive state updates and final structured rendering.
7. Mark SPEC-06-03 as `active`.
```

---

### Prompt for SPEC-07-01
```text
Execute SPEC-07-01: Multi-Tenancy Configuration for INIVESTEC.
1. Create `/system_meta/adr/005_teams_for_advisoros.md` documenting the mapping of scaffold Teams to Advisory Firms.
2. Implement `backend/app/dependencies/tenant.py` containing the `get_current_team_context` dependency that validates the user's role and returns their active `team_id`.
3. Create `backend/app/api/routes/v1/advisor/__init__.py` and ensure all routes within it require the `get_current_team_context` dependency.
4. Extend the scaffold's API key validation logic to ensure keys are scoped to the `team_id` and respect the `scope` (read_only vs full_access).
5. Write `pytest` tests simulating a tenant leakage attempt (User from Team A trying to access Team B's portfolio via API) and assert it returns 403 Forbidden.
6. Mark SPEC-07-01 as `active`.
```

---

### Prompt for SPEC-07-02
```text
Execute SPEC-07-02: Advisor Dashboard for INIVESTEC.
1. Create `backend/app/api/routes/v1/advisor/metrics.py` with optimized SQLAlchemy aggregation queries for firm-wide AUM and average health scores.
2. Implement `backend/app/api/routes/v1/advisor/clients.py` for scoped client and portfolio CRUD operations.
3. Create `backend/app/services/advisor/model_portfolio_service.py` containing the `clone_model_portfolio` logic, which copies holdings to a new client portfolio and triggers a Taskiq scoring job.
4. Build `frontend/app/advisor/page.tsx` displaying firm metrics and a searchable client list with Health Score badges.
5. Implement a "Clone to Client" modal in the frontend that calls the clone API and shows a success toast.
6. Write integration tests verifying the cloning process and strict `team_id` scoping of all advisor endpoints.
7. Mark SPEC-07-02 as `active`.
```
---

### Prompt for SPEC-07-03
```text
Execute SPEC-07-03: White-Label Reports for INIVESTEC.
1. Update the `teams` SQLAlchemy model to include `brand_logo_url` and `brand_color_hex` fields.
2. Create `backend/app/templates/report.html` using Jinja2, designed to render the Health Score, 5 pillars, AI narrative, and dynamic brand settings.
3. Implement `backend/app/tasks/reporting/generate_report.py` using `weasyprint` to convert the rendered Jinja template to a PDF.
4. Integrate with the scaffold's Resend service to email the PDF as an attachment when `delivery_method='email'`.
5. Create the `POST /api/v1/advisor/reports/generate` endpoint that triggers this Taskiq job and returns a `task_id`.
6. Write integration tests mocking `weasyprint.HTML` and the Resend client to verify the task successfully processes the payload and "sends" the email.
7. Mark SPEC-07-03 as `active`.
```

---

### Prompt for SPEC-08-01
```text
Execute SPEC-08-01: Credit Consumption Model for INIVESTEC.
1. Create `backend/app/config/credit_config.py` defining the cost matrix for CAS, AI Narrative, and PDF Reports.
2. Implement `backend/app/services/billing/credit_manager.py` with `check_balance`, `reserve_credits`, `consume_credits`, and `refund_credits` methods, ensuring atomic SQLAlchemy transactions.
3. Update the CAS upload, narrative stream, and report generation endpoints to check the balance before queuing Taskiq jobs, returning 402 if insufficient.
4. Update the respective Taskiq tasks to call `consume_credits` on success and `refund_credits` on exception.
5. Update the Next.js frontend to display the user's credit balance in the top bar and show the credit cost on action buttons.
6. Write integration tests verifying the atomic reserve/consume/refund lifecycle, specifically testing the failure/refund path.
7. Mark SPEC-08-01 as `active`.
```

---

### Prompt for SPEC-08-02
```text
Execute SPEC-08-02: DPDP Compliance for INIVESTEC.
1. Update the `users` or `portfolios` SQLAlchemy model to include `consent_given_at` and `consent_version` fields.
2. Update the CAS upload endpoint and frontend to require and validate explicit consent before processing.
3. Create `backend/app/tasks/compliance/purge_stale_pii.py`, a monthly cron job that anonymizes old unmapped holdings and deletes stale parsing logs.
4. Implement `POST /api/v1/users/me/erase` to perform a secure, cascading soft-delete/anonymization of user data and invalidate sessions.
5. Implement `GET /api/v1/users/me/export` to generate a JSON data dump and email a secure download link via Resend.
6. Write integration tests verifying the consent gate, the anonymization logic, and the erasure cascade.
7. Update `/docs/domain/dpdp_compliance.md` to reflect these exact technical controls.
8. Mark SPEC-08-02 as `active`.
```

---

### Prompt for SPEC-08-03
```text
Execute SPEC-08-03: Security Audit for INIVESTEC.
1. Update `.github/workflows/ci.yml` to include steps for `pip-audit`, `npm audit`, and `gitleaks`.
2. Create `tests/test_security/test_prompt_injection.py` with mock payloads attempting to extract system prompts or PII, asserting safe refusal.
3. Expand `tests/test_security/test_pii_leakage.py` with fuzzed PII data to guarantee 100% masking in Logfire.
4. Write integration tests verifying that the CAS upload and Narrative Stream endpoints return `429 Too Many Requests` when the Redis rate limit is exceeded.
5. Create `/docs/security_audit_checklist.md` with the manual IDOR, file upload, and network isolation checks.
6. Verify and update `docker-compose.yml` / Nginx config to ensure the Ollama service (port 11434) is strictly internal and not exposed to the host network.
7. Mark SPEC-08-03 as `active`.
```

---

### Prompt for SPEC-09-01
```text
Execute SPEC-09-01: Admin Security & Compliance Audit Interface for INIVESTEC.
1. Create `backend/app/api/routes/v1/admin/audit.py` with endpoints for `/security`, `/compliance`, and `/data-quality`, ensuring they are protected by the admin role dependency.
2. Implement a response-sanitization wrapper for these endpoints that runs the output through `PIISanitizer` before returning to the client.
3. Create `backend/app/services/admin/audit_service.py` to aggregate data from the `audit_logs`, `data_erasure_logs`, and CAS parsing failure tables.
4. Build the Next.js admin pages: `frontend/app/admin/audit/security/page.tsx`, `compliance/page.tsx`, and `data-quality/page.tsx` using the scaffold's admin data table components.
5. Add a "Manual Erasure" button in the compliance UI that triggers the erasure workflow from SPEC-08-02 for a specific user ID.
6. Write `pytest` tests asserting that admin audit endpoints return 403 for standard users and that the response sanitizer successfully masks any accidental PII in the payload.
7. Mark SPEC-09-01 as `active`.
```

---

### Prompt for SPEC-09-02
```text
Execute SPEC-09-02: System Efficiency & Observability Dashboard for INIVESTEC.
1. Create `backend/app/api/routes/v1/admin/metrics.py` with endpoints for `/queues`, `/scrapers`, and `/ai-usage`.
2. Implement `backend/app/services/admin/metrics_service.py` to query Redis for Taskiq queue lengths and DLQ counts.
3. Implement TimescaleDB queries to aggregate scraper success/failure rates and determine the "Data Freshness" (latest timestamp in hypertables).
4. Implement logic to calculate AI token usage and cache hit rates from the `llm_usage_logs` and Redis cache stats.
5. Build `frontend/app/admin/observability/page.tsx` featuring visual gauges for queue depths, line charts for scraper reliability, and a prominent "Data Freshness" status indicator.
6. Write integration tests verifying the Redis and TimescaleDB aggregation queries return the expected mock metrics.
7. Mark SPEC-09-02 as `active`.
```

---

### Prompt for SPEC-09-03
```text
Execute SPEC-09-03: Content Management System (CMS) for Web Pages for INIVESTEC.
1. Create the `site_content` SQLAlchemy model and generate the Alembic migration. Seed it with default JSON values for 'hero_title', 'pricing_features', and 'faq_items'.
2. Implement `backend/app/api/routes/v1/admin/cms.py` with GET and PUT endpoints, including Pydantic validation to ensure the JSON payload matches the expected structure for each key.
3. Build `frontend/app/admin/cms/page.tsx` with dynamic forms (text inputs for strings, array builders for FAQs) to edit the content.
4. Update the public marketing pages (e.g., `frontend/app/(marketing)/pricing/page.tsx`) to fetch data from the `site_content` table.
5. Implement an `onRevalidate` API route or Server Action that calls Next.js `revalidateTag('cms-content')` when the admin saves changes.
6. Write tests verifying that updating a FAQ item in the admin UI reflects on the public page after cache revalidation.
7. Mark SPEC-09-03 as `active`.
```

---

### Prompt for SPEC-09-04
```text
Execute SPEC-09-04: Data Refinement & Scoring Configuration Engine for INIVESTEC.
1. Create the `scoring_parameters` and `instrument_aliases` SQLAlchemy models and run migrations.
2. Implement `backend/app/api/routes/v1/admin/data.py` to list unmapped holdings and process the `map-holding` endpoint, creating global aliases if requested.
3. Implement `backend/app/api/routes/v1/admin/config.py` to GET/PUT scoring parameters, ensuring updates invalidate the Redis cache for the scoring engine.
4. Modify `backend/app/services/scoring/penalty_calculator.py` and `pillar_calculator.py` to fetch thresholds and weights from the `scoring_parameters` Redis cache instead of hardcoded constants.
5. Implement `POST /api/v1/admin/scoring/recalculate` to trigger high-priority Taskiq jobs for manual re-scoring.
6. Build the Next.js admin interfaces: `frontend/app/admin/data/unmapped/page.tsx` and `frontend/app/admin/config/scoring/page.tsx`.
7. Write integration tests verifying that changing an HHI threshold via the admin API immediately affects the output of the `PenaltyCalculator`.
8. Mark SPEC-09-04 as `active`.
```

---

### Prompt for SPEC-10-01
```text
Execute SPEC-10-01: Production Infrastructure & Containerization for INIVESTEC.
1. Create optimized, multi-stage `Dockerfile.backend` (Python 3.12 slim) and `Dockerfile.frontend` (Next.js 15 standalone output).
2. Create `nginx/default.conf` implementing strict reverse proxy routing, security headers, and explicit `deny all` rules for ports 11434 (Ollama) and 6379 (Redis).
3. Create `docker-compose.prod.yml` that simulates the production split-topology locally, including health checks for all services.
4. Write a bash script `scripts/verify_network_isolation.sh` that uses `curl` and `nc` to assert that Ollama and Redis are unreachable from outside the internal Docker network.
5. Update `/docs/deploy.md` with the exact PaaS/GPU provisioning steps and the requirement for an internal tunnel (e.g., Tailscale) between the CPU and GPU nodes.
6. Mark SPEC-10-01 as `active`.
```

---

### Prompt for SPEC-10-02
```text
Execute SPEC-10-02: CI/CD Pipeline & Automated Governance for INIVESTEC.
1. Create `.github/workflows/pr-validation.yml` implementing the linting, `verify_specs.py` execution, security audits, and full test suite (highlighting the PII and prompt injection tests).
2. Create `.github/workflows/deploy.yml` that triggers on push to `main`, builds/pushes Docker images to GHCR, runs Alembic migrations, and triggers PaaS deployment webhooks.
3. Create `.github/workflows/rollback.yml` as a manual `workflow_dispatch` to revert the deployment to the previous image tag.
4. Add a step in the PR validation to generate a coverage report and fail if backend test coverage drops below 80%.
5. Update `/docs/deploy.md` with instructions on configuring the required GitHub Encrypted Secrets.
6. Mark SPEC-10-02 as `active`.
```

---

### Prompt for SPEC-10-03

```text
Execute SPEC-10-03: Beta Launch, Operational Readiness & Resilience for INIVESTEC.

1. Create `scripts/seed_production.py` to insert the definitive Nifty 500 and AMFI instrument lists, trigger the 5-year Taskiq backfill, and seed the CMS (`site_content`) and scoring parameters.
2. Implement a Redis-backed feature flag service in `backend/app/services/core/feature_flags.py`. Create FastAPI dependencies and Next.js middleware to check flags like `enable_ai_narratives`, `enable_cas_upload`, and `maintenance_mode`.
3. Create `tests/load/locustfile.py` defining the three load scenarios (Dashboard, Ingestion, AI). Run the tests locally, capture the results, and generate `/docs/performance_baseline.md`.
4. Configure Logfire alert rules (via API or dashboard documentation) for DLQ > 0, Ollama latency > 5s, and CAS failure rate > 10%.
5. Create the `/docs/runbooks/` directory and write `incident_response.md`, `dpdp_breach_protocol.md`, `database_recovery.md`, and `data_staleness.md`.
6. Integrate a simple `/api/v1/feedback` endpoint and corresponding frontend component for beta user bug reporting.
7. Create `LAUNCH_CHECKLIST.md` in the root directory with the final sequence steps (Stripe Live, DNS, SSL, Logfire alerts, Seed script, Welcome emails).
8. Mark SPEC-10-03 as `active`.
```

---
