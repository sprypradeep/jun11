---
id: SPEC-04-03
title: PII Sanitization Middleware
status: draft
phase: 4
sequence: 3
dependencies: [SPEC-01-03, SPEC-04-01]
---

# PII Sanitization Middleware

## Overview
To ensure strict compliance with the DPDP Act, this specification defines the middleware and utility functions required to detect, mask, and prevent the leakage of Personally Identifiable Information (PII) into logs, external services, or cloud-based AI agents.

## Goals
1. Automatically detect and mask PII in all incoming CAS payloads and outgoing API responses.
2. Ensure zero PII is ever written to Logfire traces, standard output, or Taskiq logs.
3. Enforce a "Privacy by Design" architecture where PII is isolated to the local database and local LLM (Ollama) only.

## Requirements

### 4.1 PII Detection Patterns
Implement a `PIISanitizer` utility class with pre-compiled Regex patterns for:
- **PAN**: `r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'`
- **Email**: `r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'`
- **Phone**: `r'\b(?:\+?91[-.\s]?)?[6-9]\d{9}\b'`
- **Folio Numbers**: `r'\b\d{4,6}/?\d{2,4}\b'` (Context-dependent, typical CAMS/KFintech format).
- **Names**: Heuristic detection is avoided in raw text to prevent false positives; instead, rely on structural masking (e.g., masking the entire "Investor Name:" line).

### 4.2 Masking Logic
- **PAN**: `ABCDE1234F` → `XXXXX1234F`
- **Email**: `user@domain.com` → `u***@domain.com`
- **Phone**: `9876543210` → `98765***10`
- **Folio**: `123456/78` → `XXXXXX/78`

### 4.3 Middleware & Logfire Integration
- **FastAPI Middleware**: Intercept all requests to `/api/v1/portfolios/*/cas/*`. Sanitize the request body (if logging is enabled) and the response body before it leaves the server.
- **Logfire Scrubbing**: Configure Logfire's `scrubbing` feature (`logfire.configure(scrubbing=True)`) and provide custom scrubbing rules matching the above regex patterns to automatically drop or mask any span attributes.
- **Taskiq Context**: Ensure Taskiq task arguments (e.g., file paths, user IDs) do not contain raw PII. Pass only UUID references.

### 4.4 Local LLM Enforcement
- If any future feature routes CAS text to an LLM for parsing fallback, the `PIISanitizer` must be applied *before* the prompt is constructed. The system must strictly route this to the `PrivateDataAgent` (Ollama), never the `PublicDataAgent` (Gemini).

## Acceptance Criteria
- [ ] `PIISanitizer` correctly identifies and masks all defined PII patterns in unit tests.
- [ ] FastAPI middleware successfully masks PII in a mock response payload.
- [ ] Logfire configuration is verified to drop/mask PII patterns in trace spans.
- [ ] A dedicated `test_pii_leakage.py` suite attempts to inject mock PII into the CAS upload flow and asserts that no raw PII appears in the generated `trace_log.json` or mock Logfire output.
- [ ] Documentation in `/docs/domain/dpdp_compliance.md` is updated to reflect these sanitization rules.

## Technical Details
- **Libraries**: `re` (compiled regex), `fastapi.middleware`, `logfire.scrubbing`.
- **Performance**: Regex compilation must happen once at module load time to avoid overhead on every request.
