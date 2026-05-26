from unittest import mock

import pytest
from agno.run.agent import RunOutput

SESSION_ID = "test-session"


@pytest.fixture(autouse=True)
def _isolate_db(tmp_path):
    db_dir = tmp_path / "sessions"
    db_dir.mkdir()
    db_path = db_dir / "agent.db"
    with (
        mock.patch("src.agent.DB_DIR", str(db_dir)),
        mock.patch("src.agent.DB_PATH", str(db_path)),
    ):
        yield


class TestAgentKnowledgeResponse:
    def test_factual_answer_contains_expected_content(self):
        from src.agent import create_agent

        agent = create_agent(session_id=SESSION_ID)
        response = agent.run("What is the capital of France?")
        assert isinstance(response, RunOutput)
        assert response.content
        assert "Paris" in response.content

    def test_uncertainty_on_unknown_question(self):
        from src.agent import create_agent

        agent = create_agent(session_id=SESSION_ID)
        response = agent.run(
            "What is the hyperdimensional resonance frequency"
            " of a quantum tachyon field?"
        )
        assert isinstance(response, RunOutput)
        assert response.content
        assert "error" not in response.content.lower()
        uncertainty_indicators = [
            "not a real",
            "doesn't exist",
            "isn't a",
            "is not a",
            "fictional",
            "theoretical",
            "speculative",
            "don't have a",
            "no known",
            "is not real",
            "hypothetical",
            "no such",
            "does not exist",
        ]
        assert any(
            indicator in response.content.lower()
            for indicator in uncertainty_indicators
        ), f"Expected uncertainty signal in: {response.content}"


class TestKnowledgeRouting:
    def test_pure_math_expression_routes_to_calculator(self):
        from src.agent import create_agent, run_with_context

        agent = create_agent(session_id=SESSION_ID)
        result = run_with_context(agent, "128 * 46")
        assert result == "5888"

    def test_factual_question_routes_to_llm(self):
        from src.agent import create_agent, run_with_context

        agent = create_agent(session_id=SESSION_ID)
        result = run_with_context(agent, "What is the capital of France?")
        assert isinstance(result, RunOutput)
        assert "Paris" in result.content


class TestConversationContext:
    def test_followup_uses_prior_context(self):
        from src.agent import create_agent

        agent = create_agent(session_id=SESSION_ID)
        agent.run("My favorite number is 42.")

        agent2 = create_agent(session_id=SESSION_ID)
        result = agent2.run("What is my favorite number?")
        assert "42" in result.content

    def test_math_then_context(self):
        from src.agent import create_agent

        agent = create_agent(session_id=SESSION_ID)
        agent.run("What is 2 + 2?")

        agent2 = create_agent(session_id=SESSION_ID)
        result = agent2.run("Now multiply that by 5")
        assert "20" in result.content or "4" in result.content


class TestMixedQueryDetection:
    def test_seconds_in_a_day_returns_86400(self):
        from src.agent import create_agent, run_with_context

        agent = create_agent(session_id=SESSION_ID)
        result = run_with_context(agent, "How many seconds in a day?")
        assert isinstance(result, RunOutput)
        raw = result.content.replace(",", "")
        assert "86400" in raw

    def test_non_factual_non_computational_response(self):
        from src.agent import create_agent, run_with_context

        agent = create_agent(session_id=SESSION_ID)
        result = run_with_context(agent, "Tell me a joke")
        assert isinstance(result, RunOutput)
        assert result.content
        assert "error" not in result.content.lower()
