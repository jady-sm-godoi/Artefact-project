# Research: CLI Question-Answer Agent with Calculator

## Technology Decisions

### Language & Runtime

- **Decision**: Python 3.12 via uv
- **Rationale**: Defined by project constitution. Python has mature AI/LLM
  ecosystem and SymPy integration.
- **Alternatives considered**: N/A (constitution constraint)

### Agent Framework

- **Decision**: Agno
- **Rationale**: Lightweight agent framework with native tool registration,
  OpenAI integration, and conversation memory support. Aligns with project
  dependency.
- **Alternatives considered**: LangChain (heavier, more complex for single-tool
  agent), plain OpenAI API (loses agent abstractions)

### Calculator Tool

- **Decision**: SymPy via `sympify()`
- **Rationale**: SymPy is already a project dependency. `sympify()` parses
  string expressions safely and supports both arithmetic and symbolic math
  (simplification, factoring, differentiation, integration).
- **Alternatives considered**: `eval()` (unsafe), custom parser (rewrite work
  already done by SymPy)

### LLM Provider

- **Decision**: OpenAI API
- **Rationale**: Defined by project constitution. Standard API, wide
  compatibility with Agno.
- **Alternatives considered**: N/A (constitution constraint)

### CLI Interaction Model

- **Decision**: Interactive REPL loop with `>` prompt and `Processing...`
  indicator
- **Rationale**: Natural for multi-turn Q&A sessions. Defined during
  clarification (Q3).
- **Alternatives considered**: One-shot command per question (loses context)

### Error Handling Strategy

- **Decision**: Graceful degradation (calculator-only fallback when AI offline)
- **Rationale**: Defined during clarification (Q1). Maximizes utility even in
  degraded mode.
- **Alternatives considered**: Hard failure (useless when offline)

### Debug Mode

- **Decision**: Optional `--verbose` flag showing tool invocations and reasoning
- **Rationale**: Defined during clarification (Q2). Keeps default UX clean
  while enabling debugging.
- **Alternatives considered**: Always-verbose (noisy), no debug (hard to
  troubleshoot)

## Testing Strategy

- **Framework**: pytest
- **Unit tests**: Calculator tool (arithmetic, symbolic, error cases), agent
  routing logic
- **Integration tests**: Full CLI session simulation (factual question,
  calculation question, verbose mode, graceful degradation)
