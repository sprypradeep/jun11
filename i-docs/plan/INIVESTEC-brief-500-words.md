### Project Overview: Nivesh Pulse (Internal Reference)
**Project Type:** B2C & B2B Fintech Ecosystem (SaaS)
**Core Objective:** A "Health Score" platform that translates complex market signals into a simplified 0–100 metric for retail and institutional investors. The goal is to reduce "choice paralysis" by providing objective, multi-factor analysis on portfolios.

#### 1. Core Functional Logic (The Engine)
The system evaluates investment instruments based on five primary pillars: **Quality, Value, Momentum, Growth, and Risk.** 
*   **Requirement:** Develop a normalization engine that converts raw financial metrics into Z-scores relative to a peer universe (e.g., Nifty 500).
*   **Portfolio Logic:** The system must aggregate individual instrument scores into an overall portfolio score, incorporating "penalty factors" for high concentration in specific sectors (using the Herfindahl-Hirschman Index) and calculating "fee drag" for mutual fund holdings.

#### 2. Technical Architecture & Stack
The platform follows a **micro-modular architecture** designed for high concurrency and scalability:
*   **Backend:** Python/FastAPI (Asynchronous design).
*   **Frontend:** Next.js 15 / React 19 with TypeScript.
*   **Database Layer:** PostgreSQL + TimescaleDB (for time-series data) and a Vector Database (Qdrant or pgvector) for RAG implementation.
*   **Caching/Task Management:** Redis for real-time data caching; Celery/RQ for background processing of heavy calculation tasks and report generation.

#### 3. Data Pipeline & Integration
The system must handle three primary data streams:
*   **User Portfolio Ingestion:** A parsing engine to process Consolidated Account Statements (CAS) in various formats (CAMS, KFintech, CDSL/NSDL).
*   **Market Data:** Integration with NSE/BSE feeds and AMFI data for mutual funds.
*   **Alternative Data:** Scrapers or API connectors for fundamental data analysis (e.g., quarterly earnings, macro-economic indicators).

#### 4. AI & Privacy Architecture
To comply with regional data protection regulations (DPDP Act), the platform adopts a **Privacy-First Inference Model**:
*   **Local LLM Strategy:** Utilization of local inference engines (vLLM/Ollama) to ensure PII (Personally Identifiable Information) never leaves the secure environment.
*   **RAG Integration:** A Retrieval-Augmented Generation pipeline for "Narrative Engineering," translating quantitative scores into human-readable insights using a vector database of fund documents.

#### 5. Development Roadmap & Scalability
The project moves through four phases: 
1. **MVP:** Core scoring engine and basic portfolio dashboard.
2. **Growth:** Real-time broker sync and advanced analytics.
3. **Expansion:** Localized AI models (multi-lingual support) and RAG-driven deep dives.
4. **B2B Scale:** An "AdvisorOS" module providing multi-tenant APIs for financial advisors.

***

> *"I am developing a fintech SaaS called 'Nivesh Pulse.' Below is a condensed functional specification of the project. I want you to act as a Senior Software Architect and Product Manager. Based on these requirements, help me create a detailed 3-month development roadmap, a database schema for the portfolio engine, and a list of required API endpoints."*
