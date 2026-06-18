# 3-Month Roadmap

## Month 1: Foundation, Data Pipeline & Scraping Engine

**Goal:** Core infrastructure, financial data ingestion (scraping), and the quantitative scoring engine.

### Week 1: Infrastructure Alignment & Schema
| Day | Task | Output |
|-----|------|--------|
| 1-2 | Audit scaffold, map to Nivesh Pulse needs | `system_meta/core_architecture.spec` |
| 2-3 | Setup TimescaleDB + pgvector extensions | Alembic migrations |
| 3-4 | Create governance layer `/system_meta/` | All governance files |
| 4-5 | Extend `AGENTS.md`, `CLAUDE.md`, `ENV_VARS.md` | Augmented baseline docs |
| 5 | Create ADRs: TimescaleDB, pgvector, Taskiq | `system_meta/adr/001-003` |

**Key Deliverables:**
- `specs/core_architecture.spec`
- `docs/dpdp_compliance.md` (initial)
- `system_meta/adr/001_timescaledb_choice.md`
- `system_meta/adr/002_pgvector_choice.md`
- `system_meta/adr/003_taskiq_over_celery.md`

### Week 2: Financial Data Scraping Engine (CRITICAL — Per Challenge C)
| Day | Task | Output |
|-----|------|--------|
| 1-2 | Build scraper framework (async, rate-limited) | `backend/app/services/scrapers/base.py` |
| 2-3 | NSE/BSE bhav copy scraper | `scrapers/nse_bhav.py` + Taskiq task |
| 3-4 | AMFI mutual fund NAV + fundamentals scraper | `scrapers/amfi.py` + Taskiq task |
| 4-5 | Financial ratios scraper (Screener.in / Trendlyne / Moneycontrol) | `scrapers/ratios.py` |
| 5 | Historical data backfill (5 years) | Backfill Taskiq task |

**Key Deliverables:**
- `specs/data_ingestion.spec` (scrapers section)
- `docs/howto/add-data-scraper.md`
- `docs/data_dictionary.md`
- Working scrapers for: NSE bhav, AMFI NAV, PE/PB/ROE/Debt-to-Equity, EPS growth
- Data flowing into TimescaleDB hypertables
- `system_meta/adr/006_data_sources.md` (documenting scraper sources & reliability)

**Scraper Architecture:**
```python
# Async, rate-limited, retry-enabled
class BaseScraper:
    - Async HTTP client (httpx)
    - Rate limiter (per-domain, respects robots.txt)
    - Retry with exponential backoff
    - Logfire integration for observability
    - Fallback to cached data on failure
    
class NSERatesScraper(BaseScraper):
    - Daily bhav copy download
    - Parse CSV → insert into market_data_daily
    
class FinancialRatiosScraper(BaseScraper):
    - Quarterly fundamentals from multiple sources
    - Cross-validation between sources
    - Insert into fundamentals_daily
```

### Week 3: The 5-Pillar Scoring Engine
| Day | Task | Output |
|-----|------|--------|
| 1-2 | Z-score normalization engine | `services/scoring/zscore.py` |
| 2-3 | Quality + Value pillar calculations | `services/scoring/pillars/quality_value.py` |
| 3-4 | Momentum + Growth + Risk pillars | `services/scoring/pillars/` |
| 4-5 | Daily scoring cron via Taskiq | `tasks/scoring/calculate_daily.py` |
| 5 | Redis caching layer for scores | Cache invalidation strategy |

**Key Deliverables:**
- `specs/scoring_engine.spec`
- `docs/scoring_model.md` (complete)
- `docs/howto/add-scoring-pillar.md`
- Working scoring engine producing daily instrument scores
- Logfire traces for all scoring operations

### Week 4: Portfolio Engine & Aggregation
| Day | Task | Output |
|-----|------|--------|
| 1-2 | Portfolio CRUD (leverage scaffold Teams) | API endpoints |
| 2-3 | Portfolio aggregation logic | AUM-weighted scores |
| 3-4 | HHI concentration penalty | `services/scoring/penalties/hhi.py` |
| 4-5 | Fee drag penalty for MFs | `services/scoring/penalties/fee_drag.py` |
| 5 | End-to-end test: Data → Score → Portfolio | Integration tests |

**Key Deliverables:**
- `specs/portfolio_engine.spec`
- Complete scoring pipeline working end-to-end
- Month 1 milestone: **Backend can ingest market data, score instruments, and aggregate portfolio health**

---

## Month 2: CAS Ingestion, AI Narratives & Frontend

**Goal:** User-facing portfolio ingestion, RAG-powered narratives, and the Next.js dashboard.

### Week 5: Multi-Modal CAS Parsing
| Day | Task | Output |
|-----|------|--------|
| 1-2 | CAS PDF parser (CAMS format) | `services/ingestion/cas/cams.py` |
| 2-3 | CAS parsers (KFintech, CDSL, NSDL) | `services/ingestion/cas/` |
| 3-4 | Excel/CSV CAS parser | `services/ingestion/cas/excel.py` |
| 4-5 | PII sanitization middleware | `middleware/pii_sanitizer.py` |
| 5 | Taskiq CAS parsing pipeline | `tasks/ingestion/parse_cas.py` |

**Key Deliverables:**
- `specs/cas_parser.spec`
- `docs/howto/add-cas-parser.md`
- Working CAS parser for all major Indian formats
- PII sanitization verified via pytest

### Week 6: RAG Pipeline & Local LLM Setup
| Day | Task | Output |
|-----|------|--------|
| 1-2 | Enable RAG in scaffold, setup pgvector | Configuration changes |
| 2-3 | Document ingestion pipeline (SID, factsheets) | `services/rag/ingest.py` |
| 3-4 | Setup Ollama with Llama-3-8B locally | Docker config for Ollama |
| 4-5 | PrivateDataAgent (PydanticAI + Ollama) | `agents/private_agent.py` |
| 5 | Data classifier middleware | `middleware/data_classifier.py` |

**Key Deliverables:**
- `specs/rag_pipeline.spec`
- `specs/local_llm.spec`
- `docs/rag_pipeline.md`
- `docs/tiered_llm_strategy.md`
- `docs/howto/configure-local-llm.md`
- `system_meta/adr/004_hybrid_llm_strategy.md`
- Working RAG pipeline with local LLM for PII tasks

### Week 7: Narrative Generation & AI Insights
| Day | Task | Output |
|-----|------|--------|
| 1-2 | Prompt engineering for narratives | `agents/prompts/health_narrative.py` |
| 2-3 | Streaming endpoint (SSE) for narratives | API endpoint |
| 3-4 | Narrative quality testing | Test suite |
| 4-5 | PublicDataAgent for market commentary | `agents/public_agent.py` |
| 5 | Credit metering for AI calls | Integration with scaffold credits |

**Key Deliverables:**
- Working narrative generation (both tiers)
- Credit consumption tracking per narrative
- Logfire traces for all LLM calls

### Week 8: Next.js 15 Frontend Dashboard
| Day | Task | Output |
|-----|------|--------|
| 1-2 | Dashboard layout + score gauges | `frontend/app/dashboard/` |
| 2-3 | Portfolio detail view + charts | Radar charts, time-series |
| 3-4 | CAS upload flow (drag-drop + progress) | Upload UI + WebSocket |
| 4-5 | AI insights panel (streaming) | SSE integration |
| 5 | Billing/credits UI (leverage scaffold) | Stripe integration UI |

**Key Deliverables:**
- `specs/frontend_dashboard.spec`
- Complete B2C user journey working
- Month 2 milestone: **Users can upload CAS, see Health Score, read AI narratives**

---

## Month 3: AdvisorOS, Compliance & Launch

**Goal:** B2B multi-tenancy, DPDP compliance audit, and production launch.

### Week 9: AdvisorOS (Leveraging Scaffold Teams)
| Day | Task | Output |
|-----|------|--------|
| 1-2 | Map scaffold Teams → AdvisorOS concepts | `specs/advisor_os.spec` |
| 2-3 | Advisor dashboard (manage clients) | Frontend pages |
| 3-4 | Model portfolios feature | Clone portfolios to clients |
| 4-5 | White-label reports (PDF) | `services/reporting/pdf.py` |
| 5 | API keys for programmatic access | Extend scaffold API Key auth |

**Key Deliverables:**
- `system_meta/adr/005_teams_for_advisoros.md`
- Working B2B AdvisorOS
- White-labeled PDF reports

### Week 10: Billing, Credits & Usage Metering
| Day | Task | Output |
|-----|------|--------|
| 1-2 | Define credit consumption rules | 1 CAS parse = X credits, 1 narrative = Y credits |
| 2-3 | Integrate with scaffold Stripe billing | Plan configuration |
| 3-4 | Admin usage dashboard customization | `/admin/usage/nivesh-pulse` |
| 4-5 | Spike detection for AI usage | Configure scaffold feature |
| 5 | End-to-end billing test | Test suite |

**Key Deliverables:**
- Working credit-based billing
- Admin dashboard for usage monitoring

### Week 11: DPDP Compliance & Security Audit
| Day | Task | Output |
|-----|------|--------|
| 1-2 | PII leak audit (codebase scan) | Audit report |
| 2-3 | Data retention policy implementation | Auto-purge old CAS files |
| 3-4 | Consent management UI | User consent tracking |
| 4-5 | Penetration testing (AI-assisted) | Security report |
| 5 | Finalize `docs/dpdp_compliance.md` | Complete compliance doc |

**Key Deliverables:**
- DPDP compliance verified
- Security audit passed
- Data retention policies active

### Week 12: Production Deployment & Launch
| Day | Task | Output |
|-----|------|--------|
| 1-2 | Production Docker setup (Nginx + all services) | `docker-compose.prod.yml` |
| 2-3 | GPU instance setup for Ollama | Infrastructure |
| 3-4 | Logfire production configuration | Observability |
| 4-5 | Beta launch + monitoring | Go-live |
| 5 | Post-launch retrospective | `system_meta/trace/post_mortem.md` |

**Key Deliverables:**
- Production deployment
- Monitoring dashboards
- Month 3 milestone: **Nivesh Pulse live for beta users and pilot advisors**
