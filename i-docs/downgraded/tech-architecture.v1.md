# Technical Architecture (Aligned with Scaffold)

## 1 System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js 15)                     │
│   Dashboard │ CAS Upload │ AI Insights │ AdvisorOS │ Billing    │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTPS
┌──────────────────────────▼──────────────────────────────────────┐
│                    NGINX REVERSE PROXY                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                   FASTAPI BACKEND (Python 3.12)                  │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ API Routes  │  │ PydanticAI   │  │ PII Sanitization     │   │
│  │ (JWT/APIKey)│  │ Agents       │  │ Middleware           │   │
│  └─────────────┘  └──────┬───────┘  └──────────────────────┘   │
│                          │                                       │
│  ┌───────────────────────▼───────────────────────────────────┐  │
│  │              DATA CLASSIFIER (PII Detection)              │  │
│  └───────────────────────┬───────────────────────────────────┘  │
│            ┌─────────────┴─────────────┐                        │
│            ▼                           ▼                        │
│  ┌─────────────────┐         ┌─────────────────┐               │
│  │ PublicDataAgent │         │ PrivateDataAgent│               │
│  │ (Gemini)        │         │ (Ollama/Local)  │               │
│  └─────────────────┘         └─────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │    Redis     │  │   Logfire    │
│ +TimescaleDB │  │ (Cache+Rate  │  │ (Observabil- │
│ +pgvector    │  │  Limit+Taskiq)│  │  ity)        │
└──────────────┘  └──────────────┘  └──────────────┘
```

## 2 Key Integration Points with Scaffold

| Scaffold Feature | Nivesh Pulse Usage |
|-----------------|-------------------|
| **JWT + API Key + Google OAuth** | Retail users (JWT + Google), Advisors (API Key for programmatic access) |
| **Taskiq + Redis** | All background tasks: scraping, scoring, CAS parsing, RAG |
| **PydanticAI + Gemini** | PublicDataAgent for non-PII tasks |
| **Teams + Billing + Credits** | AdvisorOS multi-tenancy + credit-based AI usage |
| **Resend Email** | CAS parsing complete notifications, weekly reports |
| **Logfire** | End-to-end observability: scrapers → scoring → LLM calls |
| **Rate Limiting (100/60s)** | API protection; separate limits for AI endpoints |
| **Docker + Nginx** | Production deployment |
| **GitHub Actions** | CI/CD with spec verification step |

## 3 Credit Consumption Model

| Action | Credits Consumed | Rationale |
|--------|-----------------|-----------|
| CAS Upload & Parse | 10 | Heavy parsing, PII handling |
| Portfolio Health Score (one-time) | 5 | Quantitative calculation |
| AI Narrative Generation | 15 | LLM inference cost |
| Market Commentary (Gemini) | 3 | Cheaper cloud LLM |
| PDF Report Generation | 20 | Comprehensive analysis |
| Daily Score Refresh | 1 | Automated, lightweight |

**Plans (via Stripe):**
- **Free Tier:** 100 credits/month, 1 portfolio
- **Pro (₹999/month):** 1000 credits/month, 5 portfolios, AI narratives
- **AdvisorOS (₹4999/month):** 10,000 credits/month, unlimited clients, white-label reports
