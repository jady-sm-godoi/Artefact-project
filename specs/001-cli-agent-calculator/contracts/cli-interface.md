# CLI Interface Contract

## Invocation

```bash
# Default mode
uv run python src/cli.py

# Verbose mode
uv run python src/cli.py --verbose
```

## Input Protocol

User types free-form text and presses Enter.

| Input | Behavior |
|-------|----------|
| `"Who was Albert Einstein?"` | Knowledge query → agent responds from internal knowledge |
| `"128 * 46"` | Calculation → agent invokes calculator tool, returns exact result |
| `"x^2 + 2x + 1 factored"` | Symbolic math → agent invokes calculator tool |
| `"exit"` or `"quit"` | Cleanly terminates the session |
| Empty/whitespace | Ignored, re-prompts |
| Non-factual, non-math | Conversational response (joke, opinion, etc.) |

## Output Protocol

- **Knowledge response**: Plain text answer
- **Calculation response**: Plain text exact result
- **Error**: Human-readable error message (invalid expression, tool failure)
- **Verbose mode**: Tool invocations prefixed with `[Tool: calculator]` and
  reasoning steps
- **AI offline**: Warning message emitted once, then calculator-only mode
- **Prompt**: `> ` with `Processing...` during computation
