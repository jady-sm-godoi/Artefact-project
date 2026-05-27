# Calculator Tool Contract

## Interface

The calculator tool is an Agno tool (`FunctionTool`) that accepts a single
string parameter and returns a string.

### Input

```python
{
    "expression": str  # Math expression to evaluate (e.g., "128 * 46")
}
```

### Output (success)

```python
{
    "result": str  # Exact result (e.g., "5888")
}
```

### Output (error)

```python
{
    "error": str  # Human-readable error description
}
```

## Supported Operations

| Category | Examples |
|----------|----------|
| Basic arithmetic | `+`, `-`, `*`, `/`, `//`, `%`, `**` |
| Symbolic simplification | `simplify(x^2 + 2*x + 1)` |
| Factoring | `factor(x^2 - 4)` |
| Differentiation | `diff(sin(x)*x, x)` |
| Integration | `integrate(exp(-x), (x, 0, oo))` |
| Trigonometric | `sin(pi/2)`, `cos(0)` |
| Constants | `pi`, `E`, `oo` |

## Error Handling

- Invalid syntax → clear error message identifying the issue
- Undefined symbols → report which symbols are undefined
- Timeout → report calculation took too long
