# Operating Model

## 1 The Specification-Driven Development Loop (Aligned with Scaffold)

```
┌──────────────────────────────────────────────────────────────────┐
│ STEP 1: PLAN                                                     │
│ • Review state_of_build.json                                     │
│ • Select task from system_meta/specs/                            │
│ • Check docs/howto/ for relevant boilerplate patterns            │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ STEP 2: SPEC                                                     │
│ • Create/update .spec in system_meta/specs/                      │
│ • For new architectural decisions → create ADR                   │
│ • For new scrapers → use scraper.spec.template                   │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ STEP 3: CONTEXTUALIZE (spec-kit)                                 │
│ • Inject: .spec file + relevant boilerplate howto + CLAUDE.md    │
│ • Example: scoring_engine.spec + add-background-task.md          │
│   + docs/scoring_model.md                                        │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ STEP 4: IMPLEMENT                                                │
│ • Use Taskiq for async tasks (per scaffold)                      │
│ • Use PydanticAI agents (per scaffold)                           │
│ • Follow boilerplate patterns in docs/patterns.md                │
│ • For PII tasks → route to local LLM via PrivateDataAgent        │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ STEP 5: VERIFY                                                   │
│ • pytest tests defined in .spec                                  │
│ • verify_specs.py for spec-code consistency                      │
│ • Logfire trace inspection for performance                       │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ STEP 6: SYNC (Atomic Commit)                                     │
│ • Update .spec with implementation details                       │
│ • Update trace_log.json                                          │
│ • Update state_of_build.json                                     │
│ • Commit: code + specs + trace in single commit                  │
└──────────────────────────────────────────────────────────────────┘
```

## 2 Data Classification & Routing Rules

Every data flow in Nivesh Pulse must be classified:

| Data Type | PII Status | LLM Tier | Example |
|-----------|-----------|----------|---------|
| Market prices (NSE/BSE) | None | Tier 1 (Gemini) | Daily bhav copies |
| Financial ratios | None | Tier 1 (Gemini) | PE, PB, ROE |
| Fund factsheets | None | Tier 1 (Gemini) | AMFI data |
| CAS statements | **HIGH PII** | Tier 2 (Local) | PAN, folio, name |
| Portfolio holdings | **HIGH PII** | Tier 2 (Local) | User's specific stocks |
| Health Score narratives | **MEDIUM PII** | Tier 2 (Local) | Personalized insights |
| General market commentary | None | Tier 1 (Gemini) | Sector analysis |

## 3 Taskiq Task Taxonomy

Based on the scaffold's Taskiq configuration, define these task categories:

```python
# backend/app/tasks/
├── market_data/          # Daily market data ingestion
│   ├── fetch_nse_bhav.py
│   ├── fetch_amfi_nav.py
│   └── update_fundamentals.py
├── scoring/              # Score calculations
│   ├── calculate_zscores.py
│   ├── aggregate_portfolio.py
│   └── apply_penalties.py
├── ingestion/            # User data parsing
│   ├── parse_cas.py      # PII-bearing → Local LLM if AI-assisted
│   └── map_holdings.py
├── rag/                  # RAG pipeline
│   ├── embed_documents.py
│   └── generate_narrative.py  # PII-bearing → Local LLM
└── reporting/            # Report generation
    ├── generate_pdf.py
    └── send_email.py     # Uses Resend (per scaffold)
```
