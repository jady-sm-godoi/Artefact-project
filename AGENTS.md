## Communication

- **Mode**: caveman (sempre ativo). Falar de forma ultra-Concisa, sem artigos/filler/hedging. Técnico e direto.

## Toolchain

- **Package manager**: `uv` (not pip/poetry). Install deps: `uv sync`. Add dep: `uv add <pkg>`.
- **Python**: 3.12 (`.python-version`). Managed by uv's own Python.
- **Linter**: `ruff`. Run: `ruff check .`. Config in `pyproject.toml` (line-length=79, select=E/F/I/W).
- **Test**: `pytest`. Run: `uv run pytest`.

## Dependencies

- `agno` — AI agent framework
- `openai` — LLM provider
- `sympy` — symbolic math
- `fastapi` + `uvicorn` — REST API
- `httpx` — test client
- `groq` — alternative LLM
- `sqlalchemy` — session persistence

## Structure

- `src/cli.py` — CLI entrypoint
- `src/agent.py` — agent setup + routing logic
- `src/tools/calculator.py` — SymPy calculator tool
- `src/api/` — FastAPI app (app.py, routes.py)
- `tests/unit/` — calculator + agent tests (25 tests)
- `tests/integration/` — CLI flow tests (7 tests)
- `tests/api/` — FastAPI endpoint tests (12 tests)
- `specs/001-cli-agent-calculator/` — CLI spec
- `specs/002-fastapi-agent-api/` — API spec

## Notes

- Ruff config exists in `pyproject.toml` — line-length 79, isort known-first-party=src.
- 44 tests total across 5 test files.
- Git history with 12+ commits on `002-fastapi-agent-api` branch.

<!-- SPECKIT START -->
Current plan: specs/002-fastapi-agent-api/plan.md
Spec: specs/002-fastapi-agent-api/spec.md
Data model: specs/002-fastapi-agent-api/data-model.md
Quickstart: specs/002-fastapi-agent-api/quickstart.md
Contracts: specs/002-fastapi-agent-api/contracts/
<!-- SPECKIT END -->
