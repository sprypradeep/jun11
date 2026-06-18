# AGENTS.md

This file provides high-signal instructions for AI agents working in proj2 (FastAPI/Pydantic v2). Only include facts that an agent would likely miss without help or are non-obvious workflow constraints.

## 🚀 Key Commands & Workflow
*   **Run Server:** `cd backend && uv run uvicorn app.main:app --reload`
*   **Full Test/Lint Cycle (Required Order):** Always perform linting and formatting before running tests to ensure code quality is maintained across the board.
    ```bash
    pytest # Runs comprehensive test suite
    ruff check . --fix && ruff format . 
    ```

## 🏗️ Project Structure & Entrypoints
*   `backend/app/api/routes/v1`: Contains all API endpoints (FastAPI routers). Modification here requires careful handling of request validation and dependency injection.
*   `backend/app/services`: Core business logic layer. Services should handle domain operations and raise specific exceptions (`NotFoundError`, `AlreadyExistsError`).
*   `backend/app/repositories`: Data access objects (DAO). **Constraint:** Use `db.flush()` for state changes, never raw SQL commit methods within the repository layer.

## 💡 Core Conventions & Constraints
*   **Schema Design:** Always use separate Pydantic schemas: `Create`, `Update`, and a final `Response` schema to enforce clear data boundaries.
*   **Database Operations:** Use `.flush()` in repositories, not general database commit methods (e.g., avoid raw transaction commits).
*   **Error Handling:** Services must raise specific custom exceptions (`NotFoundError`, `AlreadyExistsError`) rather than generic Python errors.

## ⚙️ Tooling & Setup Notes
*   Use the following commands for standard maintenance tasks:
    ```bash
    # Run Migrations (When updating DB schema)
    uv run alembic upgrade head # Apply migrations to the database
    uv run alembic revision --autogenerate -m "Description" # Generate new migration file 
    ```
