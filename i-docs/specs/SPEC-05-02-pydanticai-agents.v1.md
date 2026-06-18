---
id: SPEC-05-02
title: PydanticAI Agents
status: draft
phase: 5
sequence: 2
dependencies: [SPEC-05-01]
---

# PydanticAI Agents

## Overview
This specification defines the structure, prompts, and tooling for the two core PydanticAI agents in INIVESTEC: the `PublicDataAgent` (Gemini) and the `PrivateDataAgent` (Ollama).

## Goals
1. Define strict, structured output schemas for all AI responses to ensure frontend compatibility.
2. Craft system prompts that enforce a professional, objective, and cautious financial tone.
3. Leverage PydanticAI's native tool-calling capabilities for structured data retrieval (if needed in the future).

## Requirements

### 5.1 Agent Definitions
- **PublicDataAgent**:
  - **Model**: `gemini-2.5-flash` (via scaffold config).
  - **System Prompt**: "You are an expert financial analyst. Provide concise, objective, and data-driven insights. Do not give financial advice. Base your responses strictly on the provided market data."
- **PrivateDataAgent**:
  - **Model**: `llama3:8b-instruct` or `mistral` (via Ollama).
  - **System Prompt**: "You are a privacy-first financial assistant. You are analyzing a specific user's portfolio. NEVER mention the user's name, PAN, or specific account numbers in your output. Refer to the portfolio generically as 'your portfolio'. Provide clear, actionable, and cautious insights."

### 5.2 Structured Output (Result Type)
- All agent calls must return a Pydantic model, not raw text.
- Example: `NarrativeResponse` (summary: str, key_risks: list[str], key_strengths: list[str], action_items: list[str]).
- This ensures the frontend can render the AI response in structured UI components (e.g., bullet points, risk badges) rather than a wall of text.

### 5.3 Tooling (Optional but Prepared)
- Disable the scaffold's default chart-generation tool (per project config), but prepare a `get_instrument_details(isin: str)` tool for the `PrivateDataAgent` to fetch real-time context from the database during narrative generation (Post-MVP RAG prep).

## Acceptance Criteria
- [ ] `PublicDataAgent` and `PrivateDataAgent` are instantiated with their respective models and system prompts.
- [ ] Both agents enforce the `NarrativeResponse` Pydantic schema, raising a `ModelRetry` error if the LLM returns malformed JSON.
- [ ] Unit tests mock the LLM providers and verify that the agents return valid `NarrativeResponse` objects.
- [ ] Logfire traces capture the token usage and latency of each agent call.

## Technical Details
- **Libraries**: `pydantic_ai`, `pydantic`.
- **Prompt Management**: System prompts should be loaded from a dedicated `backend/app/agents/prompts/` directory to allow easy iteration without code redeployment.
