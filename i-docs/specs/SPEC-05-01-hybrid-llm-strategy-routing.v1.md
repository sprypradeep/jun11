---
id: SPEC-05-01
title: Hybrid LLM Strategy & Routing
status: draft
phase: 5
sequence: 1
dependencies: [SPEC-01-03, SPEC-04-03]
---

# Hybrid LLM Strategy & Routing

## Overview
This specification defines the routing logic that directs AI inference requests to the appropriate LLM tier based on data classification, ensuring strict DPDP Act compliance while optimizing for cost and performance.

## Goals
1. Implement a robust `DataClassifier` that inspects payloads for PII before routing.
2. Route non-sensitive, public market data to the cloud-based `PublicDataAgent` (Google Gemini).
3. Route PII-bearing data (portfolio holdings, CAS text, personalized narratives) exclusively to the `PrivateDataAgent` (Local Ollama).

## Requirements

### 5.1 Data Classification Rules
- **Tier 1 (Public Data)**: Market commentary, sector analysis, general financial education, instrument-level fundamental summaries. (No user-specific context).
- **Tier 2 (PII Data)**: Any payload containing user names, PANs, folio numbers, specific portfolio holdings, or personalized health score narratives.

### 5.2 Routing Middleware
- Create a `LLMRouter` service that wraps PydanticAI agent calls.
- Before invoking an agent, the `LLMRouter` runs the payload through the `PIISanitizer` (from SPEC-04-03).
- If PII is detected (or if the context explicitly contains `portfolio_id` or `user_id`), the request is routed to `PrivateDataAgent` (Ollama endpoint: `http://ollama:11434`).
- If no PII is detected and the task is generic, route to `PublicDataAgent` (Gemini via scaffold's default PydanticAI config).

### 5.3 Fallback & Degradation
- If the local Ollama service is unreachable (HTTP 503), the system must **not** fall back to Gemini for PII data. Instead, it must return a graceful error: "AI insights are temporarily unavailable. Please try again later." This is a hard DPDP compliance requirement.

## Acceptance Criteria
- [ ] `LLMRouter` correctly classifies and routes mock payloads based on PII presence.
- [ ] Unit tests verify that a payload containing a mock PAN is strictly routed to the Ollama endpoint.
- [ ] Unit tests verify that a generic market query is routed to the Gemini endpoint.
- [ ] System gracefully degrades (returns 503) when Ollama is down, without leaking PII to Gemini.
- [ ] Logfire traces show the routing decision (e.g., `llm.route: private_ollama`) without logging the actual PII payload.

## Technical Details
- **Libraries**: `pydantic_ai`, `httpx` (for Ollama API calls).
- **Configuration**: Ollama endpoint URL must be configurable via `ENV_VARS.md` (default: `http://localhost:11434`).
