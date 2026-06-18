# Documentation Collision Audit

I have audited all three documentation sources. Here is the definitive, collision-free structure.

## 1 Files Created by Boilerplate (DO NOT OVERWRITE)

```
Root Level (Boilerplate-Owned):
├── README.md                    # Project overview
├── MANUAL_STEPS.md              # External setup steps
├── AGENTS.md                    # AI agent guidance (EXTEND, don't replace)
├── ENV_VARS.md                  # Env var reference (EXTEND)
├── CONTRIBUTING.md              # Contribution guidelines
├── SECURITY.md                  # Security model (EXTEND)
├── CLAUDE.md                    # Deep technical reference (EXTEND)
├── docker-compose.yml           # Docker orchestration
├── pyproject.toml               # Python dependencies
├── .env.example                 # Environment template
└── .github/workflows/           # CI/CD pipelines

/docs/ (Boilerplate-Owned):
├── architecture.md              # System architecture (EXTEND)
├── deploy.md                    # Deployment guide
├── testing.md                   # Testing guide
├── commands.md                  # CLI reference
├── permissions.md               # RBAC documentation
├── configuration.md             # Configuration guide
├── file-processing.md           # File handling patterns
├── patterns.md                  # Code patterns
├── adding_features.md           # Feature addition guide (EXTEND)
└── howto/
    ├── add-background-task.md   # Taskiq patterns (CANONICAL)
    ├── customize-agent-prompt.md
    ├── add-api-endpoint.md
    ├── use-ratings.md
    ├── configure-sync-sources.md
    ├── add-agent-tool.md
    ├── add-sync-connector.md
    └── add-rag-source.md        # RAG setup (ENABLE & EXTEND)

/frontend/
└── README.md                    # Frontend-specific docs
```

## 2 New Files to Create (NO COLLISION)

```
/docs/ (New Nivesh Pulse-Specific):
├── dpdp_compliance.md           # DPDP Act compliance
├── scoring_model.md             # Health Score mathematics
├── rag_pipeline.md              # RAG narrative engineering
├── data_dictionary.md           # Financial data fields
├── tiered_llm_strategy.md       # Gemini + Local LLM routing
└── howto/
    ├── add-scoring-pillar.md    # New: Add a scoring factor
    ├── add-cas-parser.md        # New: Add CAS format support
    ├── add-data-scraper.md      # New: Add financial data source
    └── configure-local-llm.md   # New: Setup Ollama for PII tasks

/system_meta/ (Governance Layer — Entirely New):
├── master_governance_protocol.md
├── core_architecture.spec
├── specs/
│   ├── portfolio_engine.spec
│   ├── scoring_engine.spec
│   ├── cas_parser.spec
│   ├── data_ingestion.spec      # NEW: Financial scrapers
│   ├── rag_pipeline.spec
│   ├── advisor_os.spec
│   └── local_llm.spec
├── adr/
│   ├── 001_timescaledb_choice.md
│   ├── 002_pgvector_choice.md
│   ├── 003_taskiq_over_celery.md
│   ├── 004_hybrid_llm_strategy.md
│   └── 005_teams_for_advisoros.md
├── trace/
│   ├── trace_log.json
│   ├── state_of_build.json
│   └── sync_errors.log
├── templates/
│   ├── feature.spec.template
│   ├── adr.template.md
│   └── scraper.spec.template    # NEW
└── scripts/
    ├── verify_specs.py
    ├── generate_changelog.py
    └── update_trace.py
```

## 3 Extension Protocol (How to Safely Modify Boilerplate Docs)

When extending a boilerplate file, use this convention:

```markdown
<!-- NIVESH_PULSE_EXTENSION_START -->
## Nivesh Pulse: Domain-Specific Additions

[Your additions here]
<!-- NIVESH_PULSE_EXTENSION_END -->
```

This ensures that if the boilerplate is updated, your additions are clearly demarcated and merge-conflicts are minimized.
