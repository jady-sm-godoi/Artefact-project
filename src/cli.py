import argparse

from agno.run.agent import RunOutput
from dotenv import load_dotenv

from src.agent import create_agent, route_query
from src.tools.calculator import evaluate

AI_UNAVAILABLE_TOKENS = (
    "api_key",
    "api key",
    "not set",
    "auth",
    "unavailable",
    "connection refused",
)


def _is_ai_unavailable(content: str) -> bool:
    lower = content.lower()
    return any(t in lower for t in AI_UNAVAILABLE_TOKENS)


def _get_content(response: RunOutput | str) -> str:
    return response.content if hasattr(response, "content") else str(response)


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

    calculator_only = False

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

        print("Processing...")

        if calculator_only:
            result = evaluate(user_input)
            print(result)
        else:
            response = route_query(agent, user_input)
            content = _get_content(response)

            if _is_ai_unavailable(content):
                if not calculator_only:
                    print(
                        "Warning: AI knowledge source unavailable."
                        " Switching to calculator-only mode."
                    )
                    print()
                    calculator_only = True
                result = evaluate(user_input)
                print(result)
            else:
                print(content)

        print()


if __name__ == "__main__":
    main()
