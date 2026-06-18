# ROLE & METHODOLOGY
Role: Expert Full-Stack AI Engineer.
Methodology: STRICT Specification-Driven Development (SDD) via `github/spec-kit`.
Rule: NEVER write implementation code without an approved spec and task list.

# STACK & TEMPLATE
- Stack: FastAPI (Python), Next.js 15 (TS, App Router), PostgreSQL, Redis.
- Template: `vstorm-co/full-stack-ai-agent-template`. Strictly adhere to its existing directory structure. Do not invent new architectural layers.

# SPEC-KIT WORKFLOW (MANDATORY)
Before coding, execute in order:
1. `/speckit.specify`: Define requirements -> outputs `specs/[branch]/spec.md`.
2. `/speckit.plan`: Define tech design -> outputs `plan.md`, `data-model.md`, `contracts/`.
3. `/speckit.tasks`: Break into steps -> outputs `tasks.md`.
4. Implement: Write code ONLY to satisfy a specific task. Mark tasks complete in `tasks.md` as you go.

# ARCHITECTURE RULES
- Backend: Strict layered pattern. `api/routes` (HTTP/Auth) -> `services` (Logic) -> `repositories` (DB only).
- AI Agents: Keep definitions and prompts strictly in `backend/app/agents/`.
- Frontend: Global state via Zustand (`src/stores/`). Data/WS via custom hooks (`src/hooks/`).
- Streaming: ALL LLM responses must stream via WebSockets.

# CODING STANDARDS
- Strict typing: Python (PEP 484) and TS (Strict).
- Async: Use `async/await` for all I/O, DB, and LLM calls.
- Testing: `pytest` for backend, Playwright for critical frontend flows.
- Errors: Never expose raw stack traces. Validate all LLM/external API responses.
