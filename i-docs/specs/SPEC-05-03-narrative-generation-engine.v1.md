---
id: SPEC-05-03
title: Narrative Generation Engine
status: draft
phase: 5
sequence: 3
dependencies: [SPEC-03-04, SPEC-05-02]
---

# Narrative Generation Engine

## Overview
This specification defines the service that orchestrates the translation of quantitative portfolio scores (5 pillars, HHI, fee drag) into human-readable, actionable insights using the `PrivateDataAgent`.

## Goals
1. Construct a rich, context-aware prompt that includes the portfolio's quantitative metrics without exposing raw PII.
2. Generate and cache the narrative to minimize redundant Local LLM inference costs.
3. Provide a streaming API endpoint for a responsive frontend user experience.

## Requirements

### 5.1 Context Construction
- The `NarrativeService` will fetch the latest `portfolio_scores` for a given `portfolio_id`.
- It will construct a sanitized context string: 
  "Portfolio Health Score: {score}/100. Pillars: Quality={q}, Value={v}, Momentum={m}, Growth={g}, Risk={r}. Concentration Penalty (HHI): {hhi_penalty} points due to sector concentration. Fee Drag Penalty: {fee_penalty} points due to high expense ratios."
- **Crucial**: No instrument names, ISINs, or quantities are passed to the LLM in the MVP. Only the aggregated, anonymized metrics are provided.

### 5.2 Generation & Caching
- Call the `PrivateDataAgent` with the constructed context.
- Cache the resulting `NarrativeResponse` in Redis with a 7-day TTL, or until the portfolio holdings change (cache invalidation via Redis pub/sub or simple TTL).
- Deduct the appropriate number of credits from the user's/team's ledger (per SPEC-08-01).

### 5.3 Streaming API Endpoint
- **Endpoint**: `GET /api/v1/portfolios/{portfolio_id}/narrative/stream`
- **Implementation**: Use FastAPI's `StreamingResponse` with Server-Sent Events (SSE) to stream the generated text token-by-token to the Next.js frontend, providing a "typing" effect.

## Acceptance Criteria
- [ ] `NarrativeService` correctly constructs the sanitized context string from the `portfolio_scores` table.
- [ ] The `PrivateDataAgent` successfully generates a structured `NarrativeResponse` based on the context.
- [ ] The generated narrative is cached in Redis, and subsequent calls within the TTL return the cached version without invoking the LLM.
- [ ] The SSE streaming endpoint successfully delivers the narrative to a test client.
- [ ] Logfire traces show the end-to-end latency of the narrative generation pipeline.

## Technical Details
- **Libraries**: `fastapi.responses.StreamingResponse`, `redis`, `pydantic_ai`.
- **Credit Metering**: Integrate with the scaffold's credit ledger to deduct credits upon successful generation.
