---
spec_id: SPEC-01-03
title: System Architecture
phase: 1
sequence: 3
status: Approved
owner: Chief Technology Officer
project: INIVESTEC
last_updated: 2023-10-27
---

# SPEC-01-03: System Architecture

## Purpose
Define the high-level architecture of Nivesh Pulse, including component interactions, data flows, and technology choices.

## Architecture Overview

### Micro-Modular Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                        │
│  Next.js 15 (App Router, TypeScript, React 19)          │
│  - Dashboard │ CAS Upload │ AI Insights │ AdvisorOS     │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS
┌────────────────────▼────────────────────────────────────┐
│                 API GATEWAY (Nginx)                      │
│  - Rate Limiting (100/60s)                              │
│  - SSL Termination                                      │
│  - Load Balancing                                       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              BACKEND LAYER (FastAPI)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ API Routes   │  │ PydanticAI   │  │ Middleware   │  │
│  │ (JWT/APIKey) │  │ Agents       │  │ (PII Filter) │  │
│  └──────────────┘  └──────┬───────┘  └──────────────┘  │
│                           │                              │
│  ┌────────────────────────▼───────────────────────────┐ │
│  │         DATA CLASSIFIER (PII Detection)            │ │
│  └────────────────────────┬───────────────────────────┘ │
│            ┌──────────────┴──────────────┐              │
│            ▼                             ▼              │
│  ┌─────────────────┐           ┌─────────────────┐     │
│  │ PublicDataAgent │           │ PrivateDataAgent│     │
│  │ (Gemini)        │           │ (Ollama/Local)  │     │
│  └─────────────────┘           └─────────────────┘     │
└─────────────────────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌──────────┐
│ PostgreSQL   │ │  Redis   │ │ Logfire  │
│ +TimescaleDB │ │ (Cache)  │ │ (Logs)   │
│ +pgvector    │ │ (Taskiq) │ │          │
└──────────────┘ └──────────┘ └──────────┘
```

## Component Specifications

### 1. Frontend (Next.js 15)
**Responsibilities**:
- User interface rendering
- State management
- API communication
- Real-time updates (SSE/WebSocket)

**Key Pages**:
- `/dashboard` - Portfolio overview
- `/portfolio/[id]` - Portfolio detail
- `/cas/upload` - CAS file upload
- `/advisor/clients` - AdvisorOS dashboard

### 2. Backend (FastAPI)
**Responsibilities**:
- REST API endpoints
- Business logic execution
- Task orchestration
- AI agent coordination

**Key Modules**:
```
backend/app/
├── api/routes/v1/       # API endpoints
├── services/            # Business logic
│   ├── scoring/         # Scoring engine
│   ├── ingestion/       # CAS parsing
│   └── scrapers/        # Data scrapers
├── repositories/        # Data access
├── schemas/             # Pydantic models
├── agents/              # PydanticAI agents
├── tasks/               # Taskiq tasks
└── middleware/          # PII filter, etc.
```

### 3. Database Layer
**PostgreSQL + TimescaleDB**:
- Relational data (users, portfolios, holdings)
- Time-series data (market_data, fundamentals)
- Vector data (pgvector for future RAG)

**Redis**:
- Caching (instrument scores, user sessions)
- Rate limiting
- Taskiq message broker

### 4. Background Tasks (Taskiq)
**Task Categories**:
```
tasks/
├── market_data/         # Data scraping
├── scoring/             # Score calculations
├── ingestion/           # CAS parsing
├── rag/                 # Future RAG tasks
└── reporting/           # PDF generation
```

### 5. AI Layer
**Hybrid LLM Strategy**:
- **Tier 1 (Public Data)**: Google Gemini via PydanticAI
- **Tier 2 (PII Data)**: Local LLM via Ollama

**Data Classification**:
| Data Type | PII Status | LLM Tier |
|-----------|-----------|----------|
| Market data | None | Tier 1 |
| Financial ratios | None | Tier 1 |
| CAS statements | HIGH | Tier 2 |
| Portfolio holdings | HIGH | Tier 2 |

## Data Flow Diagrams

### Flow 1: Market Data Ingestion
```
NSE/BSE API → Scraper → Taskiq → PostgreSQL → Scoring Engine → Redis Cache
```

### Flow 2: CAS Upload
```
User Upload → API → Taskiq → CAS Parser → Holdings → Portfolio Score → AI Narrative
```

### Flow 3: AI Narrative Generation
```
Portfolio Scores → Data Classifier → [PII?] → Local LLM → Narrative → User
```

## Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | Next.js 15, React 19, TypeScript | SSR, type safety, ecosystem |
| Backend | FastAPI, Python 3.12 | Async-native, performance |
| Database | PostgreSQL + TimescaleDB | Relational + time-series |
| Cache | Redis | Speed, Taskiq broker |
| Tasks | Taskiq | Async-native, modern |
| AI | PydanticAI, Gemini, Ollama | Flexibility, privacy |
| Observability | Logfire | Integrated monitoring |

## Security Architecture

### Authentication
- **B2C**: JWT + Google OAuth
- **B2B**: API Key + JWT

### Authorization
- Role-based access control (RBAC)
- Row-level security for multi-tenancy

### Data Protection
- PII sanitization middleware
- Encryption at rest (PostgreSQL)
- Encryption in transit (TLS)

## Scalability Considerations

### Horizontal Scaling
- Stateless FastAPI workers
- Redis cluster for caching
- PostgreSQL read replicas

### Vertical Scaling
- GPU instance for local LLM
- High-memory instances for TimescaleDB

## Deployment Architecture

### Development
```
Docker Compose:
- FastAPI (port 8000)
- Next.js (port 3000)
- PostgreSQL (port 5432)
- Redis (port 6379)
- Ollama (port 11434)
```

### Production
```
- Next.js → Vercel
- FastAPI + Workers → Railway/Render
- PostgreSQL + TimescaleDB → Managed DB
- Redis → Managed Redis
- Ollama → GPU VPS (RunPod)
```

## Acceptance Criteria
- [ ] Architecture diagram complete
- [ ] All components specified
- [ ] Data flows documented
- [ ] Technology choices justified
- [ ] Security architecture defined
- [ ] Deployment strategy outlined

## Dependencies
- SPEC-01-01: Project Constitution
- SPEC-01-02: Documentation System

## Tasks
1. Create architecture diagrams
2. Define component specifications
3. Document data flows
4. Specify technology stack
5. Define security architecture
6. Outline deployment strategy
