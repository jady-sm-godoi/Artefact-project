# Data Model: FastAPI Agent API

## Entities

### Session

An active conversation context identified by a client-provided ID.

| Field | Type | Description |
|-------|------|-------------|
| session_id | UUID string | Unique identifier, provided by client or auto-generated |
| messages | list[Message] | Ordered list of exchanged messages |
| created_at | datetime | Session creation timestamp |
| last_used | datetime | Last activity timestamp |

### Message

A single exchange in a session.

| Field | Type | Description |
|-------|------|-------------|
| role | enum (user, assistant, tool) | Who sent the message |
| content | str | The message text or tool result |
| timestamp | datetime | When the message was exchanged |

## API Schemas

### QueryRequest

Incoming JSON payload for POST `/query`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | str | yes | User question or math expression (max 10k chars) |
| session_id | str | no | Session UUID for context continuity |
| verbose | bool | no | Include tool call details in response |

### QueryResponse

Outgoing JSON payload from POST `/query`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| response | str | yes | Agent's answer or calculation result |
| tool_calls | list[ToolCall] | no | Tool invocations (only when verbose=true) |

### ToolCall

Record of a tool invocation (verbose mode only).

| Field | Type | Description |
|-------|------|-------------|
| tool_name | str | Name of the tool invoked (e.g., "calculator") |
| input | str | The expression passed to the tool |
| output | str | The result returned by the tool |
| duration_ms | int | How long the tool took to execute |

### HealthResponse

Outgoing JSON payload from GET `/health`.

| Field | Type | Description |
|-------|------|-------------|
| status | str | `"ok"` or `"degraded"` |
| mode | str | `"full"` or `"calculator-only"` (when AI unavailable) |

## State Transitions

```
API Start → Health check (GET /health) → Ready
                  ↓
         POST /query with session_id
                  ↓
     ┌── session exists? ──┐
     ↓                     ↓
   Reuse session      Create new session
     ↓                     ↓
     └──→ Agent processes query ←──┘
                  ↓
         Return QueryResponse
                  ↓
         Session stored in memory
```

- **API Start**: FastAPI app initializes, loads agent, starts uvicorn
- **Session lookup**: Matches `session_id` or creates new; stored in-memory
- **Agent call**: Delegates to `run_with_context` from `src.agent`
- **Response**: 200 with QueryResponse, or 422/504 on error
