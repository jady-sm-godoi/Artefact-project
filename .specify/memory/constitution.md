<!--
  Sync Impact Report

  Version change: N/A (initial) → 1.0.0
  Modified principles: N/A (all new)
  Added sections: Core Principles (I-V), Technology Stack, Development Workflow, Governance
  Removed sections: N/A
  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ updated (Constitution Check gates aligned)
    - .specify/templates/spec-template.md ✅ no changes needed
    - .specify/templates/tasks-template.md ✅ no changes needed
  Follow-up TODOs: None
-->

# Artefact Constitution

## Core Principles

### I. Code Craftsmanship

- Line length MUST NOT exceed 79 characters per line.
- Ruff MUST lint (`ruff check`) before every commit.
- Ruff MUST format (`ruff format`) before every push.
- Every `.py` file MUST end with a trailing newline.
- Import order MUST be: stdlib → third-party → local.
- Use `HTTPStatus` enum from `http` module for HTTP status codes.
  No magic numbers allowed.
- Rationale: Consistent style reduces cognitive overhead and enforces
  discipline across the codebase.

### II. Conventional Commits

- Commit messages MUST follow Conventional Commits format with one of:
  `feat:`, `fix:`, `chore:`, `refact:`, `docs:`.
- Subject line SHOULD be ≤50 characters (~80% adherence target).
- Body MUST only be included when the "why" is non-obvious.
- Rationale: Machine-readable history enables automated changelogs
  and release notes.

### III. Test-First (NON-NEGOTIABLE)

- Tests MUST be written before implementation code (Red phase).
- Tests MUST fail before implementation begins.
- Red-Green-Refactor cycle MUST be strictly followed.
- Every user story MUST have independently testable acceptance criteria.
- Rationale: Guarantees coverage, drives design, prevents regressions.

### IV. Git Workflow

- Active branches: `dev` (development work), `main` (stable releases).
- Feature branches MUST be created off `dev` with prefix `###-feature-name`.
- Commits SHOULD represent logical units of work.
- Rationale: Clear branching strategy enables parallel work and clean
  release management.

### V. Architecture & Stack

- **Language**: Python 3.12.
- **Package manager**: `uv` (not pip/poetry).
- **Agent framework**: Agno for AI agent orchestration.
- **LLM**: OpenAI API.
- **Symbolic math**: SymPy via `sympify`.
- **Persistence**: SQLite.
- All features MUST use the above stack unless explicitly justified.
- Rationale: Fixed stack eliminates dependency debates and ensures
  platform consistency.

## Technology Stack

**Runtime**: Python ≥3.12, managed by uv's own Python.
**Dependencies**: Agno (agent framework), OpenAI (LLM provider),
SymPy (symbolic math).
**Database**: SQLite (embedded, zero-config).
**Dev tooling**: Ruff (linter + formatter), uv (package management).
**AI Integration**: OpenAI API via Agno agent framework.

## Development Workflow

1. Create feature branch off `dev`: `###-feature-name`.
2. Write tests FIRST (Red phase) — they MUST fail.
3. Implement feature (Green phase) — tests MUST pass.
4. Refactor as needed (Refactor phase) — tests MUST still pass.
5. Run `ruff check .` before every commit.
6. Run `ruff format .` before every push.
7. Commit with Conventional Commit message (subject ≤50 chars).
8. Merge to `dev` — verify integration.
9. Release from `dev` → `main`.

## Governance

This Constitution supersedes all other project practices and conventions.
Amendments require:
- Documentation of the proposed change.
- Approval from the project lead or team consensus.
- A migration plan for existing code (if applicable).

Complexity MUST be justified against simpler alternatives.
All PRs and reviews MUST verify compliance with this Constitution.

**Version**: 1.0.0 | **Ratified**: 2026-05-26 | **Last Amended**: 2026-05-26
