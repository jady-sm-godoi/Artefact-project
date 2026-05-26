from agno.run.agent import RunOutput


class TestAgentKnowledgeResponse:
    def test_factual_answer_contains_expected_content(self):
        from src.agent import create_agent

        agent = create_agent()
        response = agent.run("What is the capital of France?")
        assert isinstance(response, RunOutput)
        assert response.content
        assert "Paris" in response.content

    def test_uncertainty_on_unknown_question(self):
        from src.agent import create_agent

        agent = create_agent()
        response = agent.run(
            "What is the hyperdimensional resonance frequency"
            " of a quantum tachyon field?"
        )
        assert isinstance(response, RunOutput)
        assert response.content
        assert "error" not in response.content.lower()
        uncertainty_indicators = [
            "not a real",
            "not a valid",
            "doesn't exist",
            "isn't a",
            "is not a",
            "fictional",
            "theoretical",
            "speculative",
            "don't have a",
            "no known",
            "not an actual",
            "is not real",
            "not real",
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

        agent = create_agent()
        result, messages = run_with_context(agent, [], "128 * 46")
        assert result == "5888"

    def test_factual_question_routes_to_llm(self):
        from src.agent import create_agent, run_with_context

        agent = create_agent()
        result, messages = run_with_context(
            agent, [], "What is the capital of France?"
        )
        assert isinstance(result, RunOutput)
        assert "Paris" in result.content


class TestConversationContext:
    def test_followup_uses_prior_context(self):
        from src.agent import create_agent, run_with_context

        agent = create_agent()
        messages: list = []

        result1, messages = run_with_context(
            agent, messages, "My favorite number is 42."
        )
        assert isinstance(result1, RunOutput)
        assert result1.content

        result2, messages = run_with_context(
            agent, messages, "What is my favorite number?"
        )
        assert isinstance(result2, RunOutput)
        assert "42" in result2.content

    def test_math_then_context(self):
        from src.agent import create_agent, run_with_context

        agent = create_agent()
        messages: list = []

        result1, messages = run_with_context(agent, messages, "2 + 2")
        assert result1 == "4"

        result2, messages = run_with_context(
            agent, messages, "Now multiply that by 5"
        )
        assert isinstance(result2, RunOutput)
        assert "20" in result2.content or "4" in result2.content
