# Research: FastAPI Agent API

**Branch**: `002-fastapi-agent-api` | **Date**: 2026-05-27

## Decisions

### Web Framework

- **Decision**: FastAPI
- **Rationale**: Async-first, Pydantic validation built-in, auto-generated
  OpenAPI docs (`/docs`), minimal boilerplate. Already the de facto standard
  for Python REST APIs.
- **Alternatives considered**: Flask (more boilerplate, no native async, no
  auto-docs), Django REST (too heavy for a single-endpoint API)

### ASGI Server

- **Decision**: uvicorn
- **Rationale**: Standard ASGI server for FastAPI. Used in production at
  scale. Minimal config required.
- **Alternatives considered**: hypercorn (equivalent, less ecosystem
  adoption)

### HTTP Client for Testing

- **Decision**: httpx via FastAPI TestClient
- **Rationale**: FastAPI ships TestClient wrapping httpx. No extra
  dependency needed beyond pytest.
- **Alternatives considered**: requests (synchronous, incompatible with
  FastAPI's async test pattern)

### Session Storage

- **Decision**: In-memory dict keyed by `session_id` (UUID string)
- **Rationale**: Stateless across restarts is acceptable for v1. No
  persistence dependencies. Simpler than SQLite for this use case.
- **Alternatives considered**: SQLite (adds complexity, no benefit for v1),
  Redis (infrastructure overhead)

### Error Response Format

- **Decision**: FastAPI default `{"detail": "<message>"}`
- **Rationale**: Zero config, auto-documented by Swagger, standard HTTP
  error handling via HTTPException.
- **Alternatives considered**: Custom error schema (more code, same outcome
  for v1)

### Observability

- **Decision**: Request logging only (method, path, status, duration) via
  middleware
- **Rationale**: Adequate for debugging and basic monitoring v1. No
  metrics endpoint, no tracing.
- **Alternatives considered**: Structured JSON logging + `/metrics`
  (overkill for internal API with 50 concurrent users)

### Query Routing

- **Decision**: Reuse `run_with_context` and `_is_pure_math` from
  `src.agent` directly
- **Rationale**: Thin API layer — no duplicate logic. The agent already
  handles routing between knowledge and calculator.
- **Alternatives considered**: Duplicate routing logic in API (violates
  DRY)
