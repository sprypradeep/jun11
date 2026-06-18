**Project Codename:** Nivesh Pulse
**Product Concept:** An AI-native wealthtech platform providing a "Health Score" (0–100) for investment portfolios. The system translates complex market signals—Quality, Value, Momentum, Growth, and Risk—into an actionable score for retail and professional investors in the Indian fintech ecosystem.

**Technical Architecture:**
*   **Backend/Frontend:** A micro-modular architecture utilizing Python/FastAPI (async-first) and Next.js 15 with TypeScript.
*   **Data Layer:** PostgreSQL + TimescaleDB for time-series data, Redis for caching, and Qdrant/pgvector for RAG-based vector search.
*   **AI Strategy:** A "Privacy-First" infrastructure using local LLMs (via vLLM/Ollama) to ensure DPDP Act compliance. The system employs a Retrieval-Augmented Generation (RAG) pipeline to transform quantitative scores into human-readable narratives.
*   **Data Pipeline:** A multi-modal ingestion engine capable of parsing complex consolidated financial statements (CAS), real-time market feeds, and historical backtesting modules.
*   **B2B Layer:** An "AdvisorOS" API suite for multi-tenant integration by investment advisors.

**Primary Objective:** Develop a robust, scalable system that automates portfolio health analysis while ensuring zero PII leakage to external cloud AI providers.
