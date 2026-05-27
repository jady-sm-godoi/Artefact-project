# Feature Specification: Chat UI Interface

**Created**: 2026-05-27

**Status**: Implemented

## User Scenarios & Testing

### User Story 1 - Send a query via chat (Priority: P1)

A user opens the Artefact chat UI in their browser, types a question or
calculation, and receives a response from the agent in conversational format.

**Why this priority**: Core functionality. Without this the UI has no purpose.

**Independent Test**: Open the page, type a query, press Enter, verify a
response appears below with both user message and agent message visible.

**Acceptance Scenarios**:

1. **Given** the chat page is loaded,
   **When** the user types "What is the capital of France?" and presses Enter,
   **Then** the user sees their message appear on the right side,
   **And** the agent response appears on the left side after loading.

2. **Given** the chat page is loaded,
   **When** the user types "128 * 46" and clicks the send button,
   **Then** the send button is disabled during loading,
   **And** a typing indicator is shown,
   **And** the response "5888" appears in the chat.

---

### User Story 2 - See tool calls in the response (Priority: P2)

A user sees when the agent uses a tool (calculator) along with the response.

**Why this priority**: Transparency about agent reasoning improves trust and
debuggability.

**Independent Test**: Send a calculation query, verify the response includes
a collapsible tool call section showing the calculator invocation.

**Acceptance Scenarios**:

1. **Given** the user sends a calculation query,
   **When** the response is rendered,
   **Then** a collapsible "calculator" section appears below the response text,
   **And** clicking it reveals the input and output of the calculation.

---

### User Story 3 - Multi-turn conversation (Priority: P2)

A user asks a follow-up question that references the previous answer,
and the agent maintains context.

**Why this priority**: Chat is expected to be conversational. Without context,
each query is isolated and the UX feels broken.

**Independent Test**: Ask a question, then ask "what was my first question?"
and verify the agent recalls it.

**Acceptance Scenarios**:

1. **Given** the user asked "My favorite number is 42,"
   **When** the user then asks "What is my favorite number?,"
   **Then** the agent responds with "42."

---

### User Story 4 - Health status visible in header (Priority: P3)

A user sees whether the API is online or degraded without leaving the page.

**Why this priority**: Operational feedback prevents confusion when the agent
is unavailable.

**Independent Test**: Check that a green dot and "online" text appear when the
server is healthy, and an indicator changes when status degrades.

**Acceptance Scenarios**:

1. **Given** the server is running normally,
   **When** the page loads,
   **Then** the header shows a green dot and "online" label.

2. **Given** the server enters degraded mode,
   **When** the health check updates,
   **Then** the indicator updates to reflect the degraded state.

---

### Edge Cases

- **Empty input**: Send button is disabled when input is empty, preventing
  submission of blank queries.
- **Long message**: Input is limited to prevent very long messages (API enforces
  10k char limit; UI shows error toast on 413 response).
- **Server offline**: Error toast with "Erro de conexão" message and an error
  message added to the chat.
- **Agent timeout**: Specific error message "O agente demorou muito para
  responder" shown in chat.
- **First-time user**: Empty state with suggestion buttons guides the user on
  what to ask.

## Requirements

### Functional Requirements

- **FR-001**: System MUST serve the chat UI at the root URL `/`.
- **FR-002**: System MUST serve static assets (CSS, JS) from `/static/`.
- **FR-003**: UI MUST display a text input for typing queries.
- **FR-004**: UI MUST display messages in conversational format (user right,
  agent left).
- **FR-005**: UI MUST disable the send button while a request is in-flight.
- **FR-006**: UI MUST show a typing indicator during agent response loading.
- **FR-007**: UI MUST display tool calls when present in the API response.
- **FR-008**: UI MUST persist session_id in localStorage for multi-turn
  conversations.
- **FR-009**: UI MUST show a health status indicator in the header.
- **FR-010**: UI MUST show suggestion buttons in the empty state.
- **FR-011**: UI MUST display error messages on network or server failures.
- **FR-012**: UI MUST auto-resize the text input as the user types.
- **FR-013**: UI MUST be responsive and usable on mobile viewports.

### Key Entities

- **Session**: Client-generated UUID persisted in localStorage, sent as
  `session_id` with every query to enable multi-turn conversation context.
- **ToolCall**: Represents a tool invocation (e.g., calculator) with tool name,
  input, output, and duration — displayed as a collapsible detail in the agent
  response.

## Success Criteria

### Measurable Outcomes

- **SC-001**: A user can load the chat UI, type a query, and see a response
  within 3 clicks: open browser, type, press Enter.
- **SC-002**: All three static assets (HTML, CSS, JS) are served in under 100ms
  from a cold start.
- **SC-003**: Chat UI renders correctly on viewports from 320px to 1920px
  without horizontal scroll or overlapping elements.
- **SC-004**: A user who has never used the app can send their first query
  within 10 seconds of loading the page, guided by the empty state.

## Assumptions

- UI is a single-page application (no routing, no multi-page navigation).
- No authentication required (same assumption as API v1).
- Dark theme is the only theme (no light mode toggle for v1).
- Session state lives in localStorage — clearing browser data resets the
  conversation.
- All communication with the API is via HTTPS in production, HTTP in
  development.
