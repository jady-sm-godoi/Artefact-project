from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools import Function

from src.tools.calculator import calculator_tool


def create_agent(verbose: bool = False) -> Agent:
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
    ]
    if verbose:
        instructions.append("Show tool invocations and reasoning steps.")

    return Agent(
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=tools,
        description=(
            "A CLI agent that answers questions and performs calculations."
        ),
        instructions=instructions,
        markdown=False,
        tool_call_limit=1,
    )
