import asyncio
from unittest import mock

import pytest
from fastapi.testclient import TestClient


class FakeRunOutput:
    def __init__(self, content, messages=None, tools=None):
        self.content = content
        self.messages = messages or []
        self.tools = tools or []


@pytest.fixture
def client():
    with mock.patch("src.api.app.create_agent"):
        from src.api.app import app

        with TestClient(app) as c:
            yield c


class TestSession:
    def test_followup_with_same_session_id(self, client):
        sid = "test-session-123"
        with (
            mock.patch("src.api.routes.create_agent") as mock_create,
            mock.patch("src.api.routes.run_with_context") as mock_run,
        ):
            mock_create.return_value = mock.MagicMock()
            mock_run.return_value = FakeRunOutput(
                content="Got it!", messages=[mock.MagicMock()]
            )
            resp1 = client.post(
                "/query",
                json={
                    "query": "My favorite number is 42",
                    "session_id": sid,
                },
            )
            assert resp1.status_code == 200
            mock_create.assert_called_once_with(session_id=sid)

            mock_run.return_value = FakeRunOutput(
                content="42", messages=[mock.MagicMock()]
            )
            resp2 = client.post(
                "/query",
                json={
                    "query": "What is my favorite number?",
                    "session_id": sid,
                },
            )
            assert resp2.status_code == 200
            assert resp2.json()["response"] == "42"

    def test_new_session_id_creates_new_agent(self, client):
        with (
            mock.patch("src.api.routes.create_agent") as mock_create,
            mock.patch("src.api.routes.run_with_context") as mock_run,
        ):
            mock_create.return_value = mock.MagicMock()
            mock_run.return_value = FakeRunOutput(
                content="ok", messages=[mock.MagicMock()]
            )
            resp = client.post(
                "/query",
                json={"query": "hello", "session_id": "fresh-session"},
            )
            assert resp.status_code == 200
            mock_create.assert_called_once_with(session_id="fresh-session")


class TestVerbose:
    def test_verbose_true_includes_tool_calls(self, client):
        with mock.patch("src.api.routes.run_with_context") as mock_run:
            tool = mock.MagicMock()
            tool.tool_name = "calculator"
            tool.tool_args = {"expression": "128 * 46"}
            tool.result = "5888"
            tool.metrics = mock.MagicMock()
            tool.metrics.duration = 0.012

            mock_run.return_value = FakeRunOutput(
                content="5888",
                messages=[mock.MagicMock()],
                tools=[tool],
            )
            resp = client.post(
                "/query",
                json={"query": "128 * 46", "verbose": True},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["response"] == "5888"
        assert data["tool_calls"] == [
            {
                "tool_name": "calculator",
                "input": "128 * 46",
                "output": "5888",
                "duration_ms": 12,
            }
        ]

    def test_verbose_false_omits_tool_calls(self, client):
        with mock.patch("src.api.routes.run_with_context") as mock_run:
            tool = mock.MagicMock()
            tool.tool_name = "calculator"
            tool.tool_args = {"expression": "128 * 46"}
            tool.result = "5888"
            tool.metrics = mock.MagicMock()
            tool.metrics.duration = 0.012

            mock_run.return_value = FakeRunOutput(
                content="5888",
                messages=[mock.MagicMock()],
                tools=[tool],
            )
            resp = client.post(
                "/query",
                json={"query": "128 * 46"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["response"] == "5888"
        assert data.get("tool_calls") is None

    def test_verbose_true_omits_tool_calls_when_no_tools_used(self, client):
        with mock.patch("src.api.routes.run_with_context") as mock_run:
            mock_run.return_value = FakeRunOutput(
                content="Paris",
                messages=[mock.MagicMock()],
                tools=None,
            )
            resp = client.post(
                "/query",
                json={
                    "query": "What is the capital of France?",
                    "verbose": True,
                },
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["response"] == "Paris"
        assert data.get("tool_calls") is None


class TestQueryEndpoint:
    def test_factual_question_returns_paris(self, client):
        with mock.patch("src.api.routes.run_with_context") as mock_run:
            mock_run.return_value = FakeRunOutput(
                content="Paris", messages=[mock.MagicMock()]
            )
            resp = client.post(
                "/query",
                json={"query": "What is the capital of France?"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["response"] == "Paris"

    def test_calculation_returns_5888(self, client):
        with mock.patch("src.api.routes.run_with_context") as mock_run:
            mock_run.return_value = "5888"
            resp = client.post("/query", json={"query": "128 * 46"})

        assert resp.status_code == 200
        data = resp.json()
        assert data["response"] == "5888"

    def test_empty_query_returns_422(self, client):
        resp = client.post("/query", json={"query": ""})

        assert resp.status_code == 422

    def test_query_too_long_returns_413(self, client):
        long_query = "x" * 10001
        resp = client.post("/query", json={"query": long_query})
        assert resp.status_code == 413
        assert "too long" in resp.json()["detail"].lower()

    def test_agent_timeout_returns_504(self, client):
        with mock.patch(
            "src.api.routes.asyncio.wait_for",
            mock.AsyncMock(side_effect=asyncio.TimeoutError()),
        ):
            resp = client.post("/query", json={"query": "hello"})

        assert resp.status_code == 504
        assert "timeout" in resp.json()["detail"].lower()
