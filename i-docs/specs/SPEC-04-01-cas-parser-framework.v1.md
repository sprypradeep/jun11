---
id: SPEC-04-01
title: CAS Parser Framework
status: draft
phase: 4
sequence: 1
dependencies: [SPEC-01-04, SPEC-02-03]
---

# CAS Parser Framework

## Overview
This specification defines the foundational architecture, interfaces, and asynchronous orchestration for parsing Consolidated Account Statements (CAS). It establishes a plugin-style framework to support multiple registrar formats without tightly coupling the core logic, ensuring DPDP-compliant, idempotent processing.

## Goals
1. Provide a secure, asynchronous file upload and processing pipeline with strict validation.
2. Define a strict abstract base class (`BaseCASParser`) that all specific registrar parsers must implement.
3. Ensure robust error handling, Redis-backed progress tracking, and idempotent database upserts.

## Requirements

### 4.1 File Upload & Validation
- **Endpoint**: `POST /api/v1/portfolios/{portfolio_id}/cas/upload`
- **Validation**: 
  - Allowed extensions: `.pdf`, `.xlsx`, `.csv` only.
  - Max size: 25MB (enforced via FastAPI `File` size limit).
  - MIME type verification: Use `python-magic` to verify the file signature matches the extension (prevents spoofed extensions).
- **Storage**: Temporarily store uploaded files in a secure, ephemeral local directory (`/tmp/cas_uploads/`) with a randomized UUID filename (e.g., `{uuid4()}.pdf`). The original filename must be discarded immediately to prevent PII leakage via filenames.

### 4.2 Abstract Parser Interface
- All specific parsers must inherit from `BaseCASParser` (ABC).
- **Required Methods**:
  - `detect_format(file_path: str) -> bool`: Heuristic check (e.g., searching for "CAMS", "Computer Age Management Services", or specific PDF metadata) to confirm the file matches this parser's expected format.
0
  - `extract_holdings(file_path: str) -> List[HoldingExtractionDTO]`: Core logic to extract ISIN, quantity, avg cost, and current value.
  - `extract_metadata(file_path: str) -> CASMetadataDTO`: Extract statement date and registrar name. **PII must be explicitly ignored/masked here.**

### 4.3 Taskiq Orchestration & Idempotency
- Upload endpoint triggers a Taskiq task: `process_cas_upload(task_id: str, portfolio_id: UUID, file_path: str)`.
- The task iterates through registered parsers, calling `detect_format()`. The first parser returning `True` processes the file.
- **State Management**: Update task status in Redis (`PENDING` → `PROCESSING` → `COMPLETED` or `FAILED`) with a 10-minute TTL.
- **Idempotency**: Re-processing the same `task_id` must not create duplicate holdings. The repository layer must use `INSERT ... ON CONFLICT (portfolio_id, isin) DO UPDATE` logic.
- **Cleanup**: A daily Taskiq cron job must delete files in `/tmp/cas_uploads/` older than 24 hours.

## Acceptance Criteria
- [ ] Upload endpoint correctly validates file type, size, and MIME signature, rejecting invalid files with `400 Bad Request`.
- [ ] `BaseCASParser` abstract class is defined with strict typing and raises `NotImplementedError` for unimplemented methods.
- [ ] Taskiq successfully routes the upload, updates Redis state, and handles retries (max 2) on transient file I/O errors.
- [ ] A mock parser implementation can be registered, detected, and executed end-to-end in integration tests.
- [ ] Original filenames are never logged or stored; only UUIDs are used in `trace_log.json` and Logfire.

## Technical Details
- **Libraries**: `python-multipart`, `aiofiles`, `python-magic`, `pydantic`, `taskiq`, `redis`.
- **Security**: Temporary files must have `600` (owner read/write only) permissions.
