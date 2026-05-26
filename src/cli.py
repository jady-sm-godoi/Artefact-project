import argparse

from agno.models.message import Message
from agno.run.agent import RunOutput
from dotenv import load_dotenv

from src.agent import create_agent, run_with_context
from src.tools.calculator import evaluate

AI_UNAVAILABLE_TOKENS = (
    "api_key",
    "api key",
    "not set",
    "auth",
    "unavailable",
    "connection refused",
    "rate limit",
)


def _is_ai_unavailable(response: RunOutput | str) -> bool:
    if hasattr(response, "status") and response.status == "ERROR":
        return True
    if hasattr(response, "content"):
        content = response.content
    else:
        content = str(response)
    lower = content.lower()
    return any(t in lower for t in AI_UNAVAILABLE_TOKENS)


def _get_content(response: RunOutput | str) -> str:
    return response.content if hasattr(response, "content") else str(response)


def _display_tool_calls(response: RunOutput) -> None:
    if not response.tools:
        return
    for tool in response.tools:
        args = tool.tool_args or {}
        expr = args.get("expression", "")
        print(f'[Tool: calculator] "{expr}" → {tool.result}')


def main(argv: list[str] | None = None) -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="CLI Question-Answer Agent with Calculator"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show tool invocations and reasoning steps",
    )
    args = parser.parse_args(argv)

    agent = create_agent(verbose=args.verbose)

    print("Artefact Agent — type 'exit' or 'quit' to stop.")
    print()

    messages: list[Message] = []
    calculator_only = False
    last_input: str | None = None
    last_response: str | None = None

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            break

        if user_input == last_input and last_response is not None:
            print(last_response)
            print()
            continue

        print("Processing...")

        if calculator_only:
            result = evaluate(user_input)
            last_input = user_input
            last_response = result
            if args.verbose:
                print(f'[Tool: calculator] "{user_input}" → {result}')
            print(result)
        else:
            response, messages = run_with_context(agent, messages, user_input)
            content = _get_content(response)

            if _is_ai_unavailable(response):
                if not calculator_only:
                    print(
                        "Warning: AI knowledge source unavailable."
                        " Switching to calculator-only mode."
                    )
                    print()
                    calculator_only = True
                result = evaluate(user_input)
                last_input = user_input
                last_response = result
                if args.verbose:
                    print(f'[Tool: calculator] "{user_input}" → {result}')
                print(result)
            else:
                if args.verbose:
                    if isinstance(response, RunOutput):
                        _display_tool_calls(response)
                    else:
                        print(
                            f'[Tool: calculator] "{user_input}" → {response}'
                        )
                last_input = user_input
                last_response = content
                print(content)

        print()


if __name__ == "__main__":
    main()
