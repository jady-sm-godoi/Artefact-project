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
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
<!-- SPECKIT END -->
