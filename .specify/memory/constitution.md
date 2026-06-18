# Project Constitution v0.1
## Sync Impact Report
Version change: N/A → 0.1
Modified Principles: All core principles defined by the project's architecture and development workflow are consolidated into this document for maximum clarity and agentic adherence.
Added sections: None (Consolidation of existing best practices).
Removed sections: None.

Templates requiring updates: ✅ updated (`AGENTS.md` was also updated to reflect these new standards).

Follow-up TODOs: No critical placeholders were deferred; all principles are concrete requirements for the project's operation and development lifecycle.


# 📜 Project Constitution of proj2
## Governance & Versioning
**Version:** 0.1 (Initial consolidation)
**Ratification Date:** 2026-06-19
**Last Amended Date:** 2026-06-19

### Amendment Procedure and Compliance Review
*   Any change to this Constitution must be preceded by a formal update to the project's `AGENTS.md` file, documenting the new rule set.
*   All major architectural shifts or principle additions require consensus from core team members (TODO: Define approval process).
*   The current development workflow is strictly governed by the **SPEC-KIT Workflow** outlined below; deviations are prohibited.

## Core Development Principles (MUST ADHERE)

### 1. Specification and Planning Discipline
All code implementation MUST be preceded by a successful run of the `speckit` command sequence: `/speckit.specify` $\rightarrow$ `/speckit.plan` $\rightarrow$ `/speckit.tasks`. Code must only address tasks defined in the resulting `tasks.md`.

### 2. Architectural Layering (Backend)
The backend MUST strictly adhere to a layered architecture for separation of concerns:
*   **API Routes (`api/routes`)**: Handles HTTP requests, authentication, and request validation using FastAPI dependencies. It is the only layer permitted to interact with external services or raw input data.
*   **Services (`services`)**: Contains all core business logic (the "what"). Services must orchestrate domain operations and raise specific custom exceptions (`NotFoundError`, `AlreadyExistsError`). They MUST NOT contain direct database access code.
*   **Repositories (`repositories`)**: Data Access Objects (DAO). This layer is responsible for translating domain objects into persistence mechanisms. **Constraint:** All state changes MUST use the repository's dedicated flush method (`db.flush()`), never raw transaction commits or general commit methods.

### 3. Modularity and Context Minimization
To ensure high agentic efficiency, all code must adhere to strict modularity rules:
*   **File Size**: No file should exceed **150 lines** of functional code (including type definitions). If a unit exceeds this limit, it MUST be refactored into smaller modules.
*   **Single Responsibility Principle (SRP)**: Each module/file must have one, and only one, reason to change. Logic components like validation, data fetching, business calculation, and UI presentation MUST reside in separate files or classes.
*   **Exports**: Use explicit **named exports** (`export const foo`) for all public APIs instead of default exports to enable clear dependency tracking (tree-shaking).

### 4. Workflow & Tooling Standards
The development cycle must follow a strict, sequential command order:
1.  `uv run alembic upgrade head`: Apply database migrations first.
2.  `pytest`: Run the comprehensive test suite against all components. Failures here block further progress.
3.  `ruff check . --fix && ruff format .`: Always perform linting and formatting *before* testing to ensure code quality standards are met across the board, fixing issues automatically where possible before running tests or committing changes.

## Technical Constraints (MUST ADHERE)
*   **Asynchronicity**: All I/O operations (DB calls, API requests, LLM interactions) MUST use `async/await`.
*   **Typing**: Use strict typing in both Python and TypeScript environments to enforce data contracts at compile time. Shared types should be defined centrally but grouped by domain.

## Conclusion
Adherence to these principles ensures the codebase remains navigable for automated tools while maintaining high standards of maintainability, testability, and scalability across all development phases.