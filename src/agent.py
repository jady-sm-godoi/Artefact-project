from __future__ import annotations

import os

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run.agent import RunOutput
from agno.tools import Function
from dotenv import load_dotenv

from src.instructions import INSTRUCTIONS, VERBOSE_INSTRUCTION
from src.math_words import MATH_PATTERN, MATH_WORDS, WORD_PATTERN
from src.tools.calculator import calculator_tool, evaluate

load_dotenv()

DB_DIR = "sessions"
DB_PATH = os.path.join(DB_DIR, "agent.db")


def _is_pure_math(expression: str) -> bool:
    stripped = expression.strip()
    if not stripped:
        return False
    if not MATH_PATTERN.fullmatch(stripped):
        return False
    words = WORD_PATTERN.findall(stripped)
    return all(w.lower() in MATH_WORDS for w in words)


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

    instructions = list(INSTRUCTIONS)
    if verbose:
        instructions.append(VERBOSE_INSTRUCTION)

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
