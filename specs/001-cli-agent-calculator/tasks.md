---

description: "Task list for CLI Question-Answer Agent with Calculator feature"

---

# Tasks: CLI Question-Answer Agent with Calculator

**Input**: Design documents from `specs/001-cli-agent-calculator/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED per Constitution (III. Test-First NON-NEGOTIABLE).
Write tests FIRST (Red phase), ensure they FAIL, then implement (Green phase).

**Organization**: Tasks are grouped by user story to enable independent
implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure: `src/`, `src/tools/`, `tests/unit/`,
      `tests/integration/` directories
- [X] T002 Initialize Python project with `uv` — ensure `pyproject.toml` has
      agno, openai, sympy dependencies
- [X] T003 [P] Configure Ruff linting and formatting in `pyproject.toml`
      (79-char line length, trailing newline, import ordering)
- [X] T004 [P] Create `src/__init__.py` and `src/tools/__init__.py` package
      files
- [X] T005 [P] Create `tests/__init__.py`, `tests/unit/__init__.py`,
      `tests/integration/__init__.py` package files

**Checkpoint**: Setup complete — foundational phase can begin

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story
can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create Agno agent base with OpenAI integration in
      `src/agent.py` — configure API key, model, and tool registry
- [X] T007 [P] Create calculator tool function using SymPy `sympify()` in
      `src/tools/calculator.py` — parse expression, return string result
- [X] T008 [P] Create CLI REPL loop in `src/cli.py` — read-eval-print loop
      with `>` prompt and `Processing...` indicator
- [X] T009 Implement graceful degradation: detect AI API unavailability,
      warn user, switch to calculator-only mode
- [X] T010 Implement `--verbose` flag parsing in `src/cli.py` — show tool
      invocations and reasoning steps when enabled

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 - Ask a factual question (Priority: P1) 🎯 MVP

**Goal**: User asks a factual question, agent answers from its knowledge

**Independent Test**: Ask three factual questions from different domains
(history, science, geography) and verify each receives a relevant, coherent
answer

### Tests for User Story 1 (Test-First per Constitution) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Write unit test for agent knowledge response in
      `tests/unit/test_agent.py` — verify agent returns answer for factual
      questions
- [ ] T012 [P] [US1] Write unit test for agent uncertainty in
      `tests/unit/test_agent.py` — verify agent communicates uncertainty
      when answer is not known
- [ ] T013 [P] [US1] Write integration test for full factual Q&A session
      in `tests/integration/test_cli.py`

### Implementation for User Story 1

- [ ] T014 [US1] Implement knowledge-only query routing in `src/agent.py` —
      route factual questions to LLM without tool invocation
- [ ] T015 [US1] Wire agent knowledge response to CLI output in `src/cli.py`
      — display answer text to user

**Checkpoint**: User Story 1 functional — agent answers factual questions

---

## Phase 4: User Story 2 - Perform a calculation (Priority: P1)

**Goal**: User asks a calculation, agent uses SymPy tool and returns exact
result

**Independent Test**: Ask three arithmetic questions (multiplication, division,
mixed expression) and verify mathematically exact answers

### Tests for User Story 2 (Test-First per Constitution) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T016 [P] [US2] Write unit test for arithmetic operations in
      `tests/unit/test_calculator.py` — test `+`, `-`, `*`, `/`
- [ ] T017 [P] [US2] Write unit test for symbolic math in
      `tests/unit/test_calculator.py` — test `simplify`, `factor`,
      `diff`, `integrate`
- [ ] T018 [P] [US2] Write unit test for calculator error handling in
      `tests/unit/test_calculator.py` — invalid syntax, undefined symbols
- [ ] T019 [P] [US2] Write integration test for calculation query flow in
      `tests/integration/test_cli.py` — user types expression, gets exact
      result

### Implementation for User Story 2

- [ ] T020 [P] [US2] Implement `sympify()` expression parsing in
      `src/tools/calculator.py` — handle string-to-expression conversion
- [ ] T021 [P] [US2] Implement basic arithmetic operations in
      `src/tools/calculator.py` — evaluate `+`, `-`, `*`, `/`, `**`
- [ ] T022 [P] [US2] Implement symbolic math operations in
      `src/tools/calculator.py` — simplify, factor, diff, integrate
- [ ] T023 [US2] Implement calculator tool error handling in
      `src/tools/calculator.py` — catch SymPy exceptions, return
      human-readable messages
- [ ] T024 [US2] Register calculator tool with Agno agent in `src/agent.py`
      — add as a FunctionTool
- [ ] T025 [US2] Implement calculation detection and routing in
      `src/agent.py` — agent detects math query and invokes calculator
      tool

**Checkpoint**: User Story 2 functional — agent answers calculation queries
with exact results

---

## Phase 5: User Story 3 - Follow-up conversation (Priority: P2)

**Goal**: User asks follow-up questions, agent maintains conversation context

**Independent Test**: Ask a question, then a follow-up referencing the
previous answer (e.g., "What is 2 + 2?" then "Now multiply that by 5")

### Tests for User Story 3 (Test-First per Constitution) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T026 [P] [US3] Write unit test for conversation context in
      `tests/unit/test_agent.py` — verify follow-up queries use prior
      context
- [ ] T027 [P] [US3] Write integration test for follow-up query flow in
      `tests/integration/test_cli.py`

### Implementation for User Story 3

- [ ] T028 [US3] Enable Agno conversation memory in `src/agent.py` —
      configure session-based message history
- [ ] T029 [US3] Implement follow-up context handling in `src/agent.py` —
      pass conversation history to LLM for context-aware responses

**Checkpoint**: User Story 3 functional — agent maintains session context

---

## Phase 6: User Story 4 - Handle ambiguous/mixed input (Priority: P3)

**Goal**: User asks something that blends knowledge and calculation, agent
makes reasonable decision

**Independent Test**: Ask "How many seconds in a day?" and verify agent uses
calculator tool correctly

### Tests for User Story 4 (Test-First per Constitution) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T030 [P] [US4] Write unit test for mixed query detection in
      `tests/unit/test_agent.py` — "How many seconds in a day?" should
      trigger calculator
- [ ] T031 [P] [US4] Write integration test for calculation-via-text
      queries in `tests/integration/test_cli.py`

### Implementation for User Story 4

- [ ] T032 [US4] Implement mixed/ambiguous query routing in `src/agent.py`
      — detect implicit calculations in natural language
- [ ] T033 [US4] Implement non-factual non-computational response in
      `src/cli.py` — handle jokes, opinions, etc.

**Checkpoint**: User Story 4 functional — agent handles edge cases

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T034 [P] Implement empty input handling in `src/cli.py` — ignore and
      re-prompt
- [ ] T035 [P] Implement exit command handling in `src/cli.py` — "exit",
      "quit" cleanly terminate session
- [ ] T036 [P] Implement graceful degradation display in `src/cli.py` —
      show AI offline warning, allow calculator-only usage
- [ ] T037 [P] Implement verbose mode display formatting in `src/cli.py` —
      show `[Tool: calculator]` and tool input/output
- [ ] T038 [P] Implement repeated query response in `src/agent.py` — reuse
      previous answer or ask for clarification
- [ ] T039 Run `ruff check .` and fix all linting issues
- [ ] T040 Run `uv sync` and verify all imports work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user
  stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — No dependencies on
  other stories
- **User Story 2 (P1)**: Can start after Foundational — No dependencies on
  other stories
- **User Story 3 (P2)**: Depends on US1 (needs agent + conversation context)
- **User Story 4 (P3)**: Depends on US1 + US2 (needs both routing paths)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- US1 and US2 can run in parallel (both P1, no cross-dependencies)
- All tests for a user story marked [P] can run in parallel
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "T011 [US1] test_agent.py: knowledge response"
Task: "T012 [US1] test_agent.py: uncertainty"
Task: "T013 [US1] test_cli.py: full Q&A session"

# Parallel implementation tasks:
Task: "T014 [US1] agent.py: knowledge-only routing"
Task: "T015 [US1] cli.py: wire response to output"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 (factual questions)
4. Complete Phase 4: User Story 2 (calculations)
5. **STOP and VALIDATE**: Test both stories independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo
3. Add User Story 2 → Test independently → Deploy/Demo (MVP!)
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (factual questions)
   - Developer B: User Story 2 (calculation tool)
3. After P1 stories complete:
   - Developer A: User Story 3 (follow-up context)
   - Developer B: User Story 4 (ambiguous routing)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
