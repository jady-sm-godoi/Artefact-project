# Quickstart: CLI Question-Answer Agent with Calculator

## Prerequisites

- Python 3.12
- uv (package manager)

## Setup

```bash
# Install dependencies
uv sync

# Verify installation
uv run python -c "import agno; import openai; import sympy; print('OK')"
```

## Run

```bash
# Default mode
uv run python src/cli.py

# Verbose mode (shows tool invocations and reasoning)
uv run python src/cli.py --verbose
```

## Usage Examples

```
> Who was Albert Einstein?
Albert Einstein was a German-born theoretical physicist...

> 128 * 46
5888

> simplify(x^2 + 2*x + 1)
(x + 1)^2

> What's the capital of France?
Paris

> exit
Goodbye!
```

## Testing

```bash
# Run all tests
uv run pytest tests/

# Run with coverage
uv run pytest --cov=src tests/
```

## Project Structure

```
src/
├── agent.py           # Agno agent setup and tool registration
├── tools/
│   └── calculator.py  # SymPy calculator tool
└── cli.py             # REPL entry point

tests/
├── unit/
│   ├── test_calculator.py
│   └── test_agent.py
└── integration/
    └── test_cli.py
```
