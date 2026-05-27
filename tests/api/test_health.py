from unittest import mock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    with mock.patch("src.api.app.create_agent"):
        from src.api.app import app

        with TestClient(app) as c:
            yield c


class TestHealthEndpoint:
    def test_health_returns_ok_when_ai_available(self, client):
        client.app.state.ai_available = True
        resp = client.get("/health")

        assert resp.status_code == 200
        data = resp.json()
        assert data == {"status": "ok", "mode": "full"}

    def test_health_returns_degraded_when_ai_unavailable(self, client):
        client.app.state.ai_available = False
        resp = client.get("/health")

        assert resp.status_code == 200
        data = resp.json()
        assert data == {"status": "degraded", "mode": "calculator-only"}
