from agno.tools import tool
from sympy import sympify, SympifyError


def evaluate(expression: str) -> str:
    """Evaluate a mathematical expression and return the exact result.

    Supports arithmetic (+, -, *, /, **, //, %), symbolic simplification,
    factoring, differentiation, integration, trigonometric functions,
    and constants (pi, E, oo).

    Args:
        expression: A mathematical expression as a string
                   (e.g., "128 * 46", "factor(x^2 - 4)").

    Returns:
        The exact result as a string, or an error message if evaluation fails.
    """
    try:
        result = sympify(expression)
        return str(result)
    except (SympifyError, SyntaxError, TypeError, ValueError):
        return f'Error: invalid expression — "{expression}"'
    except Exception as e:
        return f"Error: could not evaluate expression — {e}"


@tool(name="calculator")
def calculator_tool(expression: str) -> str:
    """Evaluate a mathematical expression and return the exact result.

    Supports arithmetic (+, -, *, /, **, //, %), symbolic simplification,
    factoring, differentiation, integration, trigonometric functions,
    and constants (pi, E, oo).

    Args:
        expression: A mathematical expression as a string
                   (e.g., "128 * 46", "factor(x^2 - 4)").

    Returns:
        The exact result as a string, or an error message if evaluation fails.
    """
    return evaluate(expression)
