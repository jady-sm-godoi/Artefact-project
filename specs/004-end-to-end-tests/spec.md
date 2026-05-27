# Feature Specification: End-to-End Tests

**Created**: 2026-05-27

**Status**: Implemented

## User Scenarios & Testing

### User Story 1 - Verify frontend is served correctly (Priority: P1)

A developer or CI pipeline verifies the chat UI is accessible and all static
assets load without errors.

**Why this priority**: Core regression check. If the frontend stops serving,
the entire UI is broken.

**Independent Test**: GET / returns 200 with HTML containing expected elements;
GET /static/style.css returns CSS; GET /static/app.js returns JavaScript.

**Acceptance Scenarios**:

1. **Given** the API server is running,
   **When** a client makes a GET request to `/`,
   **Then** the response status is 200,
   **And** the content-type is text/html,
   **And** the body contains elements like "userInput", "sendBtn", "messages".

2. **Given** the API server is running,
   **When** a client requests `/static/style.css`,
   **Then** the response status is 200,
   **And** the content-type includes "css".

3. **Given** the API server is running,
   **When** a client requests `/static/app.js`,
   **Then** the response status is 200,
   **And** the content-type includes "javascript".

---

### User Story 2 - Verify frontend references correct paths (Priority: P1)

A developer checks that the HTML correctly links to static assets using the
proper URL paths.

**Why this priority**: Broken asset references cause silent failures — the
page loads but has no styling or interactivity.

**Independent Test**: Parse the HTML and verify it contains `/static/style.css`
and `/static/app.js`.

**Acceptance Scenarios**:

1. **Given** the API server is running,
   **When** a client requests `/`,
   **Then** the HTML contains a stylesheet link to `/static/style.css`.
2. **Given** the API server is running,
   **When** a client requests `/`,
   **Then** the HTML contains a script tag referencing `/static/app.js`.

---

### User Story 3 - Browser-based UI interaction (Priority: P2)

A developer runs automated browser tests that simulate real user interactions:
typing, clicking, waiting for responses, and verifying UI state changes.

**Why this priority**: HTTP-level tests cannot verify JavaScript execution,
DOM updates, or visual state transitions. Browser tests cover the real UX.

**Independent Test**: Open the page in a headed browser, type a query, verify
the user message appears, wait for the agent response, confirm loading dots
appear and disappear.

**Acceptance Scenarios**:

1. **Given** the page is loaded in a browser,
   **When** the user types a query and presses Enter,
   **Then** the user message is rendered with label "Você",
   **And** the agent message appears with label "Artefact",
   **And** typing dots are shown during loading and hidden after.

2. **Given** the page is loaded in a browser,
   **When** the user clicks a suggestion button,
   **Then** the query is sent automatically,
   **And** both user and agent messages appear in the chat.

---

### User Story 4 - API and frontend integration (Priority: P2)

A developer verifies the frontend and API work together under various server
states.

**Why this priority**: Integration bugs (e.g., frontend not handling degraded
mode) are hard to catch without end-to-end tests.

**Independent Test**: Set the API to degraded mode, verify the frontend still
serves while the health indicator reflects the degraded state.

**Acceptance Scenarios**:

1. **Given** the API is in degraded mode,
   **When** a client requests `/`,
   **Then** the page still loads with full content.
2. **Given** the API is in degraded mode,
   **When** a client requests `/health`,
   **Then** the response contains `"status": "degraded"`.

---

### Edge Cases

- **Unknown static file**: Requesting `/static/nonexistent.txt` returns 404.
- **Server not running**: Playwright tests fail with clear connection error
  (handled by test fixture starting the server).
- **Empty state**: Fresh page load shows suggestions and no messages.
- **Send button initial state**: Button is disabled when input is empty.

## Requirements

### Functional Requirements

- **FR-001**: E2E tests MUST verify the frontend HTML is served at `/`.
- **FR-002**: E2E tests MUST verify all static assets are served with correct
  content types.
- **FR-003**: E2E tests MUST verify the HTML references the correct static
  asset paths.
- **FR-004**: E2E tests MUST verify the frontend contains expected UI elements
  (input, send button, messages container, empty state).
- **FR-005**: E2E tests MUST verify the health endpoint works alongside the
  frontend.
- **FR-006**: E2E tests MUST verify the frontend handles degraded API mode.
- **FR-007**: E2E tests in headed mode MUST verify browser interactions:
  typing, button state, message rendering, loading states.
- **FR-008**: E2E tests MUST handle a non-running server case gracefully.

### Key Entities

- **TestClient**: FastAPI test client used for HTTP-level E2E tests (no browser
  required).
- **Playwright browser**: Chromium instance in headed mode for visual UI
  interaction tests.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All E2E tests pass in under 30 seconds on a development machine.
- **SC-002**: Frontend serving tests detect regression in asset paths or
  content types within 2 seconds.
- **SC-003**: Headed browser tests simulate real user flow (type → send →
  receive) without manual intervention.
- **SC-004**: E2E tests cover all functional requirements of the Chat UI
  feature (FR-001 through FR-013).

## Assumptions

- Server is started automatically by test fixtures for headed tests.
- Playwright and Chromium are installed as dev dependencies.
- Tests do not require external network access (API runs locally).
- The headed tests require a display server (DISPLAY environment variable set).
- Test suite can be run alongside unit and API tests with a single command.
