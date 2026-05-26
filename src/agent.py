from __future__ import annotations

import os
import re

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run.agent import RunOutput
from agno.tools import Function
from dotenv import load_dotenv

from src.tools.calculator import calculator_tool, evaluate

load_dotenv()

_MATH_PATTERN = re.compile(r"^[\d\s+\-*/%^().,xXa-zA-Z_=!<>]+$")
_WORD_PATTERN = re.compile(r"[a-zA-Z]+")

_MATH_WORDS = {
    "sin",
    "cos",
    "tan",
    "cot",
    "sec",
    "csc",
    "asin",
    "acos",
    "atan",
    "acot",
    "asec",
    "acsc",
    "sinh",
    "cosh",
    "tanh",
    "coth",
    "sech",
    "csch",
    "asinh",
    "acosh",
    "atanh",
    "acoth",
    "asech",
    "acsch",
    "log",
    "ln",
    "exp",
    "sqrt",
    "abs",
    "simplify",
    "factor",
    "expand",
    "collect",
    "together",
    "apart",
    "cancel",
    "diff",
    "integrate",
    "limit",
    "re",
    "im",
    "arg",
    "conjugate",
    "trigsimp",
    "powsimp",
    "radsimp",
    "ratsimp",
    "nsimplify",
    "pi",
    "e",
    "i",
    "x",
    "y",
    "z",
    "t",
    "n",
    "a",
    "b",
    "c",
    "j",
    "k",
    "alpha",
    "beta",
    "gamma",
    "theta",
    "phi",
    "delta",
}

DB_DIR = "sessions"
DB_PATH = os.path.join(DB_DIR, "agent.db")


def _is_pure_math(expression: str) -> bool:
    stripped = expression.strip()
    if not stripped:
        return False
    if not _MATH_PATTERN.fullmatch(stripped):
        return False
    words = _WORD_PATTERN.findall(stripped)
    return all(w.lower() in _MATH_WORDS for w in words)


def create_agent(
    verbose: bool = False,
    model=None,
    session_id: str | None = None,
) -> Agent:
    if model is None:
        model = OpenAIChat(id="gpt-4o-mini")

    os.makedirs(DB_DIR, exist_ok=True)
    db = SqliteDb(db_file=DB_PATH)

    if session_id is None:
        session_id = "default-session"

    tools: list[Function] = [calculator_tool]

    instructions = [
        "You are a helpful CLI assistant that answers user questions.",
        (
            "When the user asks a factual or knowledge-based question,"
            " answer from your own knowledge without using any tool."
        ),
        (
            "When the user asks a question that involves any numerical"
            " calculation, arithmetic, or mathematical concept (e.g.,"
            " 'how many seconds in a day', 'volume of a sphere',"
            " 'distance traveled at 60 mph for 2 hours'), you MUST use"
            " the calculator tool to compute the result."
        ),
        "Be concise and direct in your responses.",
        "If you are unsure about an answer, communicate your uncertainty.",
        (
            "Do NOT use LaTeX math formatting (like \\(...\\) or \\[...\\])."
            " Always output math results in plain text — e.g., '1/2' instead"
            " of '\\frac{1}{2}', 'sqrt(2)' instead of '\\sqrt{2}'."
        ),
        (
            "IMPORTANT: Only use the calculator tool when the user input"
            " is a clear mathematical expression, calculation request,"
            " or involves numerical computation. Do NOT use it for"
            " conceptual questions, definitions, explanations, jokes,"
            " or opinions."
        ),
        (
            "IMPORTANT: When calling the calculator tool for trigonometric"
            " functions, always use radians — not degrees."
            " For example, use sin(pi/6) NOT sin(30 degrees)."
            " Convert degrees to radians yourself before calling the tool."
        ),
    ]
    if verbose:
        instructions.append("Show tool invocations and reasoning steps.")

    return Agent(
        model=model,
        db=db,
        session_id=session_id,
        add_history_to_context=True,
        num_history_runs=5,
        tools=tools,
        description=(
            "A CLI agent that answers questions and performs calculations."
        ),
        instructions=instructions,
        markdown=False,
        tool_call_limit=1,
    )


def run_with_context(
    agent: Agent,
    user_input: str,
) -> RunOutput | str:
    if _is_pure_math(user_input):
        return evaluate(user_input)

    response = agent.run(user_input)
    if response.messages is not None:
        return response
    content = (
        response.content if hasattr(response, "content") else str(response)
    )
    return content
