# Quickstart: FastAPI Agent API

## Prerequisites

- Python 3.12
- uv (package manager)
- OPENAI_API_KEY in `.env`

## Setup

```bash
# Install dependencies
uv sync

# Verify installation
uv run python -c "import fastapi; import uvicorn; print('OK')"
```

## Run

```bash
# Development server with auto-reload
uv run uvicorn src.api.app:app --reload --port 8000

# Production
uv run uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

## Usage Examples

```bash
# Ask a factual question
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of France?"}'
# → {"response":"Paris"}

# Perform a calculation
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "128 * 46"}'
# → {"response":"5888"}

# Verbose mode (show tool calls)
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "128 * 46", "verbose": true}'
# → {"response":"5888","tool_calls":[{"tool_name":"calculator",...}]}

# Multi-turn conversation
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "My favorite number is 42", "session_id": "abc-123"}'
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is my favorite number?", "session_id": "abc-123"}'
# → {"response":"42"}

# Health check
curl http://localhost:8000/health
# → {"status":"ok","mode":"full"}

# API docs
open http://localhost:8000/docs
```

## Testing

```bash
# Run API tests
uv run pytest tests/api/ -v

# Run all tests
uv run pytest tests/ -v
```

## Project Structure

```
src/
├── agent.py           # Existing — Agno agent setup
├── tools/
│   └── calculator.py  # Existing — SymPy calculator
├── cli.py             # Existing — CLI REPL
└── api/
    ├── __init__.py
    ├── app.py         # FastAPI app, lifespan, middleware
    └── routes.py      # /query and /health endpoints

tests/
├── api/
│   ├── __init__.py
│   ├── test_query.py  # /query endpoint tests
│   └── test_health.py # /health endpoint tests
```
