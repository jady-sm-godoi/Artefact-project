# Feature Specification: FastAPI Agent API

**Feature Branch**: `002-fastapi-agent-api`

**Created**: 2026-05-27

**Status**: Draft

**Input**: User description: "Agora vamos construir uma api fastapi para se comunicar com o agente que você criou no spec 001."

## Clarifications

### Session 2026-05-27

- Q: Error response format → A: FastAPI default `{"detail": "message"}`
- Q: API observability → A: Request logging (method, path, status, duration) + `/health` endpoint

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Send query and receive response (Priority: P1)

A developer sends an HTTP POST request containing a question or calculation
to the API. The API forwards it to the agent and returns the response.

**Why this priority**: This is the core functionality — exposing the agent via
HTTP. Everything else depends on this working.

**Independent Test**: Can be tested by sending three different queries
(factual, calculation, mixed) via HTTP and verifying each returns the correct
response.

**Acceptance Scenarios**:

1. **Given** the API server is running,
   **When** a client sends a POST request with `{"query": "What is the
   capital of France?"}`,
   **Then** the API returns a 200 response with `{"response": "Paris"}`.
2. **Given** the API server is running,
   **When** a client sends a POST request with `{"query": "128 * 46"}`,
   **Then** the API returns a 200 response with `{"response": "5888"}`.
3. **Given** the API server is running,
   **When** a client sends a POST request with an empty `query`,
   **Then** the API returns a 422 validation error.

---

### User Story 2 - Check API health (Priority: P1)

A developer or monitoring system checks whether the API is running and
ready to accept requests.

**Why this priority**: Health checks are essential for deployment, monitoring,
and container orchestration. Without this, operational reliability is unknown.

**Independent Test**: Can be tested by sending a GET request to the health
endpoint and verifying a 200 response with status information.

**Acceptance Scenarios**:

1. **Given** the API server is running,
   **When** a client sends a GET request to `/health`,
   **Then** the API returns a 200 response with `{"status": "ok"}`.
2. **Given** the AI knowledge source is unavailable,
   **When** a client sends a GET request to `/health`,
   **Then** the API returns a 200 response with `{"status": "degraded",
   "mode": "calculator-only"}`.

---

### User Story 3 - Multi-turn conversation via API (Priority: P2)

A developer sends a series of related queries in a session. The API maintains
conversation context so follow-up questions are understood in relation to
previous ones.

**Why this priority**: Multi-turn conversations improve the API's usefulness
but require session management, adding complexity. Not required for MVP.

**Independent Test**: Send a query, then a follow-up referencing the previous
answer, and verify the API maintains context correctly.

**Acceptance Scenarios**:

1. **Given** a session exists on the server,
   **When** a client sends a follow-up query with the same `session_id`,
   **Then** the API understands the context and responds correctly.
2. **Given** a client sends a query with a new `session_id`,
   **When** the API processes the request,
   **Then** a new session is created automatically.

---

### User Story 4 - Verbose response with tool details (Priority: P3)

A developer debugging the agent wants to see tool invocations and reasoning
steps in the API response.

**Why this priority**: Debugging support is valuable but not essential for
production use of the API.

**Independent Test**: Send a calculation query with `verbose: true` and
verify the response includes tool call information.

**Acceptance Scenarios**:

1. **Given** the API server is running,
   **When** a client sends a POST request with `{"query": "128 * 46",
   "verbose": true}`,
   **Then** the API returns a response that includes tool call details
   alongside the result.

---

### Edge Cases

- **Invalid JSON payload**: API returns 422 with `{"detail": "<message>"}`
  describing the malformed request.
- **Query too long**: API enforces a maximum query length and returns a 413
  error if exceeded.
- **Agent timeout**: If the agent takes too long to respond, the API returns a
  504 Gateway Timeout.
- **AI knowledge source unavailable**: API continues to respond to calculation
  queries while returning a clear indication that the knowledge source is
  offline for factual questions.
- **Concurrent requests**: API handles multiple simultaneous requests without
  session data corruption.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose a POST endpoint `/query` that accepts a JSON
  body with a `query` field (string, required).
- **FR-002**: System MUST return a 200 response with `{"response": "..."}`
  containing the agent's answer.
- **FR-003**: System MUST expose a GET endpoint `/health` that returns service
  status.
- **FR-004**: System MUST return 422 validation error with
  `{"detail": "<message>"}` for requests missing the `query` field or with
  empty `query`.
- **FR-005**: System MUST support an optional `session_id` field in the
  request to maintain conversation context.
- **FR-006**: System MUST support an optional `verbose` boolean field that
  includes tool invocation details in the response.
- **FR-007**: System MUST support an optional `/docs` endpoint (auto-generated
  by FastAPI) for interactive API documentation.
- **FR-008**: System MUST enforce a maximum query length of 10,000 characters.
- **FR-009**: System MUST degrade gracefully when the AI knowledge source is
  unavailable: return responses for calculation queries and indicate degraded
  mode in the health endpoint.
- **FR-010**: System MUST accept concurrent requests without data corruption
  for session state.
- **FR-011**: System MUST return a 504 Gateway Timeout if agent response
  exceeds 30 seconds.
- **FR-012**: System MUST log each request with method, path, status code,
  and duration.

### Key Entities

- **QueryRequest**: Incoming JSON payload with `query` (required), optional
  `session_id` and `verbose` fields.
- **QueryResponse**: Outgoing JSON payload with `response` (string) and
  optional `tool_calls` array (shown when verbose mode is enabled).
- **Session**: A conversation context identified by `session_id`, maintaining
  message history for follow-up queries.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: API responds to all valid queries with the correct agent
  response within 5 seconds (excluding agent processing time).
- **SC-002**: API correctly handles 50 concurrent requests without errors
  or session corruption.
- **SC-003**: Health endpoint returns accurate status (ok/degraded) in under
  100ms.
- **SC-004**: A developer can send their first successful API request within
  5 minutes of starting the server, with no external documentation beyond
  the `/docs` endpoint.

## Assumptions

- The API is consumed by other services or frontends, not directly by end
  users.
- No authentication or API key is required for v1 (internal network use).
- The API runs on a single machine, colocated with the agent.
- Session state is kept in memory (no persistence across server restarts).
- The server runs with uvicorn or similar ASGI server.
- Standard FastAPI auto-generated `/docs` (Swagger UI) is sufficient for API
  documentation.
