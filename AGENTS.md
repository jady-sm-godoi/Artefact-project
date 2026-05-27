## Communication

- **Mode**: caveman (sempre ativo). Falar de forma ultra-Concisa, sem artigos/filler/hedging. Técnico e direto.

## Toolchain

- **Package manager**: `uv` (not pip/poetry). Install deps: `uv sync`. Add dep: `uv add <pkg>`.
- **Python**: 3.12 (`.python-version`). Managed by uv's own Python.
- **Linter**: `ruff`. Run: `ruff check .` (no custom config yet).

## Dependencies

- `agno` — AI agent framework
- `openai` — LLM provider
- `sympy` — symbolic math

## Structure

- `main.py` — single entrypoint (stub).
- No tests, no CI, no git history (fresh repo, no commits yet).

## Notes

- This repo has zero tests or test framework configured. Any test work must add both.
- No Ruff config exists in `pyproject.toml` — defaults apply until configured.
- No pre-commit hooks, task runner, or dev scripts.

<!-- SPECKIT START -->
Current plan: specs/002-fastapi-agent-api/plan.md
Spec: specs/002-fastapi-agent-api/spec.md
Data model: specs/002-fastapi-agent-api/data-model.md
Quickstart: specs/002-fastapi-agent-api/quickstart.md
Contracts: specs/002-fastapi-agent-api/contracts/
<!-- SPECKIT END -->
