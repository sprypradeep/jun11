---
id: SPEC-06-03
title: AI Insights Panel
status: draft
phase: 6
sequence: 3
dependencies: [SPEC-05-03]
---

# AI Insights Panel

## Overview
This specification defines the user interface for consuming the AI-generated portfolio narratives. It must transform the structured `NarrativeResponse` from the backend into an engaging, easy-to-read format, leveraging Server-Sent Events (SSE) for a premium "streaming" user experience.

## Goals
1. Implement a robust SSE client to handle token-by-token streaming of the AI narrative.
2. Render the structured `NarrativeResponse` (summary, risks, strengths, actions) in distinct, visually appealing UI blocks.
3. Provide clear feedback on credit consumption and handle AI service unavailability gracefully.

## Requirements

### 6.1 Streaming Implementation
- **Endpoint**: Connect to `GET /api/v1/portfolios/{portfolio_id}/narrative/stream` using the native `EventSource` API or a robust wrapper (e.g., `sse.js` or custom `fetch` with `ReadableStream`).
- **UX**: Display a "Generating insights..." skeleton or typing indicator while the stream is active.
- **Parsing**: Accumulate incoming SSE chunks and parse the final JSON payload once the stream closes.

### 6.2 Structured Rendering
Once the full `NarrativeResponse` is received, render it in dedicated sections:
- **Executive Summary**: Prominent text block at the top.
- **Key Strengths**: Green-tinted badge list.
- **Key Risks**: Red/Amber-tinted badge list.
- **Action Items**: Checkbox-style list for the user to track.
- **Disclaimer**: A subtle, standardized footer: "AI-generated insights are for informational purposes only and do not constitute financial advice."

### 6.3 Credit Consumption & Error Handling
- **Credit UI**: Display a small "Cost: X Credits" badge next to the "Generate Insights" button.
- **503 Handling**: If the backend returns a 503 (Local LLM unavailable), display a friendly, non-technical message: "Our AI analyst is taking a brief rest. Please try again in a few minutes." Do not expose backend infrastructure details.
- **Caching**: If a valid, fresh narrative exists in the backend cache, skip the streaming UI and render the cached result instantly with a "Last updated: X mins ago" timestamp.

## Acceptance Criteria
- [ ] SSE connection successfully establishes and streams data without dropping, rendering a smooth typing effect or progressive reveal.
- [ ] The final structured JSON is correctly parsed and mapped to the distinct UI sections (Strengths, Risks, Actions).
- [ ] The UI gracefully handles and displays the custom 503 error message without crashing.
- [ ] Credit deduction is visually acknowledged (e.g., a toast notification: "15 credits used for AI analysis").
- [ ] The component is fully responsive and accessible (screen readers can read the final structured output).

## Out of Scope
- Chatbot-style conversational interface (this is a one-shot narrative generation per MVP spec).
- User editing of the AI-generated text.

## Technical Details
- **Libraries**: Native `EventSource` or `fetch` with `ReadableStream`, `framer-motion` (optional, for smooth reveal animations).
- **State**: Local component state for `isStreaming`, `streamedText`, and `finalParsedResponse`.
