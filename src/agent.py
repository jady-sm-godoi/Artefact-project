import re

from agno.agent import Agent
from agno.models.groq import Groq
from agno.run.agent import RunOutput
from agno.tools import Function
from dotenv import load_dotenv

from src.tools.calculator import calculator_tool, evaluate

load_dotenv()

_MATH_PATTERN = re.compile(r"^[\d\s+\-*/%^().,xXa-zA-Z_=!<>]+$")


def _is_pure_math(expression: str) -> bool:
    stripped = expression.strip()
    if not stripped:
        return False
    return bool(_MATH_PATTERN.fullmatch(stripped))


def route_query(agent: Agent, user_input: str) -> RunOutput | str:
    if _is_pure_math(user_input):
        return evaluate(user_input)
    return agent.run(user_input)


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
