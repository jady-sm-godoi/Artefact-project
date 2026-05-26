from __future__ import annotations

import re

from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.message import Message
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
) -> Agent:
    if model is None:
        model = Groq(id="llama-3.3-70b-versatile")

    tools: list[Function] = [calculator_tool]

    instructions = [
        "You are a helpful CLI assistant that answers user questions.",
        (
            "When the user asks a mathematical question or calculation,"
            " use the calculator tool to compute the exact result."
        ),
        (
            "When the user asks a factual or knowledge-based question,"
            " answer from your own knowledge without using any tool."
        ),
        "Be concise and direct in your responses.",
        "If you are unsure about an answer, communicate your uncertainty.",
        (
            "IMPORTANT: Only use the calculator tool when the user input"
            " is a clear mathematical expression or calculation request."
            " Do NOT use it for conceptual questions, definitions,"
            " or explanations."
        ),
    ]
    if verbose:
        instructions.append("Show tool invocations and reasoning steps.")

    return Agent(
        model=model,
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
    messages: list[Message],
    user_input: str,
) -> tuple[RunOutput | str, list[Message]]:
    if _is_pure_math(user_input):
        result = evaluate(user_input)
        messages.append(Message(role="user", content=user_input))
        messages.append(Message(role="assistant", content=str(result)))
        return result, messages

    user_msg = Message(role="user", content=user_input)
    messages.append(user_msg)

    response = agent.run(messages)
    messages.extend(response.messages[-1:])

    return response, messages
