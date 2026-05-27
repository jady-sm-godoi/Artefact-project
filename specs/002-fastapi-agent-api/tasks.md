# Tasks: FastAPI Agent API

**Input**: Design documents from `specs/002-fastapi-agent-api/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included per Constitution III (Test-First non-negotiable).

**Organization**: Tasks grouped by user story for independent implementation
and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single project: `src/`, `tests/` at repository root
- New package: `src/api/` for FastAPI application

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and package structure

- [X] T001 Create `src/api/` package with `src/api/__init__.py`
- [X] T002 Create `tests/api/` package with `tests/api/__init__.py`
- [X] T003 Add `fastapi`, `uvicorn[standard]`, `httpx` to `pyproject.toml`
      dependencies and run `uv sync`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure needed before ANY user story

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create FastAPI app in `src/api/app.py` with lifespan
      (agent init/shutdown), logging middleware (method, path, status,
      duration), and include router from routes
- [X] T005 Create Pydantic request/response schemas in `src/api/routes.py`:
      QueryRequest, QueryResponse, ToolCall, HealthResponse (per
      data-model.md and contracts/api-contracts.md)

**Checkpoint**: Foundation ready — user stories can begin in parallel

---

## Phase 3: User Story 1 — Send query and receive response (Priority: P1) 🎯 MVP

**Goal**: POST `/query` accepts a question or calculation and returns agent
answer.

**Independent Test**: Send 3 different queries (factual, calculation, mixed)
via HTTP POST and verify each returns correct response.

### Tests for User Story 1

> Write these tests FIRST, ensure they FAIL before implementation
> (Red-Green-Refactor per Constitution III).

- [X] T006 [P] [US1] Test POST /query with factual question returns 200 +
      correct response in `tests/api/test_query.py`
- [X] T007 [P] [US1] Test POST /query with calculation "128 * 46" returns
      "5888" in `tests/api/test_query.py`
- [X] T008 [US1] Test POST /query with empty query returns 422 validation
      error in `tests/api/test_query.py`

### Implementation for User Story 1

- [X] T009 [US1] Implement POST /query route in `src/api/routes.py`:
      validate QueryRequest, call agent from `src.agent`, return
      QueryResponse
- [X] T010 [US1] Wire route into FastAPI app in `src/api/app.py`

**Checkpoint**: US1 fully functional and independently testable 🎯

---

## Phase 4: User Story 2 — Check API health (Priority: P1)

**Goal**: GET `/health` returns service status (ok/degraded with mode).

**Independent Test**: Send GET request to `/health`, verify 200 with status
JSON.

### Tests for User Story 2

- [X] T011 [P] [US2] Test GET /health returns `{"status": "ok",
      "mode": "full"}` in `tests/api/test_health.py`
- [X] T012 [P] [US2] Test GET /health returns degraded status when AI
      unavailable in `tests/api/test_health.py`

### Implementation for User Story 2

- [X] T013 [US2] Implement GET /health route in `src/api/routes.py`:
      check agent availability, return HealthResponse

**Checkpoint**: US1 and US2 both independently functional

---

## Phase 5: User Story 3 — Multi-turn conversation (Priority: P2)

**Goal**: POST /query with `session_id` maintains conversation context for
follow-up questions.

**Independent Test**: Send query with session_id, then send follow-up
with same session_id — verify context preserved.

### Tests for User Story 3

- [ ] T014 [P] [US3] Test follow-up query with same session_id maintains
      context in `tests/api/test_query.py`
- [ ] T015 [P] [US3] Test new session_id creates new session automatically
      in `tests/api/test_query.py`

### Implementation for User Story 3

- [ ] T016 [US3] Add in-memory session storage dict in `src/api/app.py`
      (lifespan)
- [ ] T017 [US3] Implement session_id lookup/create logic in POST /query
      in `src/api/routes.py`

**Checkpoint**: US3 independently functional — conversation context works

---

## Phase 6: User Story 4 — Verbose response with tool details (Priority: P3)

**Goal**: POST /query with `verbose: true` includes tool invocation details
in response.

**Independent Test**: Send calculation query with `verbose: true`, verify
response includes tool_calls array.

### Tests for User Story 4

- [ ] T018 [P] [US4] Test verbose=true includes tool_calls in response in
      `tests/api/test_query.py`
- [ ] T019 [P] [US4] Test verbose=false (default) omits tool_calls in
      `tests/api/test_query.py`

### Implementation for User Story 4

- [ ] T020 [US4] Capture tool call details from agent response in POST /query
      in `src/api/routes.py`
- [ ] T021 [US4] Include tool_calls in QueryResponse when verbose=true in
      `src/api/routes.py`

**Checkpoint**: All user stories independently functional

---

## Phase 7: Polish and Cross-Cutting Concerns

**Purpose**: Quality and edge-case hardening

- [ ] T022 [P] Add max query length validation (10k chars) in POST /query
      in `src/api/routes.py`
- [ ] T023 [P] Add agent timeout handling (504 Gateway Timeout after 30s)
      in `src/api/routes.py`
- [ ] T024 Run `ruff check .` and fix any lint issues
- [ ] T025 Run `uv run pytest tests/api/` and verify all tests pass
- [ ] T026 [P] Run quickstart.md validation — verify server starts and
      curl examples work

---

## Dependencies and Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational — MVP core
- **US2 (Phase 4)**: Depends on Foundational — can run parallel with US1
- **US3 (Phase 5)**: Depends on US1 (adds session to /query) + Foundational
- **US4 (Phase 6)**: Depends on US1 (adds verbose to /query) + Foundational
- **Polish (Phase 7)**: Depends on all desired stories complete

### User Story Dependencies

- **US1 (P1)**: No dependencies on other stories — start after Foundational
- **US2 (P1)**: No dependencies on other stories — start after Foundational
- **US3 (P2)**: Depends on US1 (modifies /query handler) but independently
  testable with session_id
- **US4 (P3)**: Depends on US1 (modifies /query response) but independently
  testable with verbose flag

### Within Each User Story

- Tests MUST be written and FAIL before implementation (Red-Green-Refactor)
- Schemas before routes
- Routes before edge-case hardening

### Parallel Opportunities

- T004 and T005 (Foundational) can run in parallel
- All test tasks marked [P] can run in parallel within a story
- US1 and US2 can be implemented in parallel (different endpoints)
- T022 and T023 (Polish) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Test POST /query with factual question in tests/api/test_query.py"
Task: "Test POST /query with calculation in tests/api/test_query.py"
Task: "Test POST /query with empty query in tests/api/test_query.py"

# After tests pass, implement:
Task: "Implement POST /query route in src/api/routes.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2 — both P1)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (POST /query)
4. Complete Phase 4: User Story 2 (GET /health)
5. **STOP and VALIDATE**: Test both P1 stories independently
6. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 + US2 → Test independently → Deploy/Demo (MVP!)
3. Add US3 (session support) → Test independently → Deploy
4. Add US4 (verbose mode) → Test independently → Deploy
5. Polish phase → Final quality pass

### Parallel Team Strategy

With multiple developers:
1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (POST /query)
   - Developer B: User Story 2 (GET /health)
3. Developer A continues with US3 (session) + US4 (verbose)
4. Stories integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story independently completable and testable
- Verify tests fail before implementing (Red phase)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies
