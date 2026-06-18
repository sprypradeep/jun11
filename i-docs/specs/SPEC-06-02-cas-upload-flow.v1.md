---
id: SPEC-06-02
title: CAS Upload Flow
status: draft
phase: 6
sequence: 2
dependencies: [SPEC-04-01, SPEC-04-02]
---

# CAS Upload Flow

## Overview
This specification defines the end-to-end user experience for uploading Consolidated Account Statements (CAS). It must be frictionless, provide real-time feedback on the asynchronous backend processing, and gracefully handle parsing errors or unmapped holdings.

## Goals
1. Provide a secure, intuitive drag-and-drop file upload interface with strict client-side validation.
2. Implement real-time progress tracking by polling the backend Taskiq task status.
3. Present a clear, actionable summary post-parsing, including a dedicated UI for resolving "unmapped holdings."

## Requirements

### 6.1 Upload Interface & Client-Side Validation
- **Component**: A drag-and-drop zone (`react-dropzone`).
- **Validation**: 
  - Accept only `.pdf`, `.xlsx`, `.csv`.
  - Enforce 25MB max file size.
  - Display clear, user-friendly error messages for invalid files *before* network request.
- **Security**: File is sent via `multipart/form-data` to the backend. No client-side PII extraction occurs.

### 6.2 Progress Tracking (Polling)
- Upon successful upload, the backend returns a `task_id`.
- The frontend initiates a polling mechanism (using React Query's `refetchInterval`) against `GET /api/v1/tasks/{task_id}/status`.
- **UI States**:
  - `PENDING`: "Upload successful. Queuing for processing..."
  - `PROCESSING`: Animated progress bar or spinner. "Analyzing your statement securely..."
  - `COMPLETED`: Success state, redirect to portfolio view or show summary.
  - `FAILED`: Error state with a generic message ("Parsing failed. Please ensure the file is an unlocked CAS.") and a retry button.

### 6.3 Post-Parsing Summary & Unmapped Holdings
- If parsing succeeds but yields `unmapped_holdings`, display a dedicated "Review Required" modal or section.
- **UI**: A table listing the unrecognized scheme names, allowing the user to manually search and select the correct ISIN from a dropdown (fetched from `GET /api/v1/instruments/search?q=...`).
- Once resolved, the user clicks "Save & Recalculate Score," triggering a portfolio score refresh.

## Acceptance Criteria
- [ ] Drag-and-drop zone correctly rejects files >25MB or wrong extensions with inline UI errors.
- [ ] Polling mechanism accurately reflects state transitions (`PENDING` → `PROCESSING` → `COMPLETED`) without excessive network spam (e.g., poll every 2 seconds).
- [ ] Failed tasks display a user-friendly error message and do not crash the application.
- [ ] The "Unmapped Holdings" UI successfully allows a user to search, select, and map a missing instrument, triggering a backend update.
- [ ] All upload interactions are wrapped in Error Boundaries to prevent full-page crashes.

## Out of Scope
- Client-side PDF password decryption (users must upload unlocked files as per backend SPEC-04-02).

## Technical Details
- **Libraries**: `react-dropzone`, `@tanstack/react-query`, `lucide-react` (for icons).
- **Performance**: Abort polling if the component unmounts. Limit max polling attempts to 30 (1 minute) before showing a "Still processing, check back later" message.
