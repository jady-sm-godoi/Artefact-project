from unittest import mock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    with mock.patch("src.api.app.create_agent"):
        from src.api.app import app

        with TestClient(app) as c:
            yield c


class TestFrontendServing:
    def test_index_returns_html(self, client):
        resp = client.get("/")

        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/html")

    def test_index_contains_chat_ui_elements(self, client):
        resp = client.get("/")
        html = resp.text

        assert "Artefact Agent" in html
        assert "userInput" in html
        assert "inputForm" in html
        assert "sendBtn" in html
        assert "messages" in html

    def test_index_has_empty_state_with_suggestions(self, client):
        resp = client.get("/")
        html = resp.text

        assert "suggestion" in html or "suggestions" in html
        assert "128" in html
        assert "France" in html

    def test_index_references_static_assets(self, client):
        resp = client.get("/")
        html = resp.text

        assert "/static/style.css" in html
        assert "/static/app.js" in html


class TestStaticFiles:
    def test_css_is_served(self, client):
        resp = client.get("/static/style.css")

        assert resp.status_code == 200
        assert "css" in resp.headers["content-type"]

    def test_js_is_served(self, client):
        resp = client.get("/static/app.js")

        assert resp.status_code == 200
        assert "javascript" in resp.headers["content-type"]

    def test_html_is_served(self, client):
        resp = client.get("/static/index.html")

        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/html")

    def test_unknown_static_returns_404(self, client):
        resp = client.get("/static/nonexistent.txt")

        assert resp.status_code == 404


class TestFrontendApiIntegration:
    def test_frontend_and_health_serve_together(self, client):
        frontend = client.get("/")
        health = client.get("/health")

        assert frontend.status_code == 200
        assert health.status_code == 200
        assert health.json()["status"] == "ok"

    def test_frontend_with_degraded_api_still_serves(self, client):
        client.app.state.ai_available = False

        frontend = client.get("/")
        health = client.get("/health")

        assert frontend.status_code == 200
        assert health.json()["status"] == "degraded"
        assert "Artefact" in frontend.text

    def test_api_docs_still_accessible(self, client):
        resp = client.get("/docs")

        assert resp.status_code == 200
