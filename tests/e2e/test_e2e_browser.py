import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
from playwright.sync_api import expect

HERE = Path(__file__).resolve().parent.parent.parent
APP = "src.api.app:app"

_HEADED = os.environ.get("E2E_HEADED", "").strip() in ("1", "true", "yes")


@pytest.fixture(scope="module")
def server_url():
    proc = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            APP, "--host", "127.0.0.1",
            "--port", "8765", "--log-level", "error",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)
    yield "http://127.0.0.1:8765"
    proc.terminate()
    proc.wait()


@pytest.fixture(scope="module")
def browser():
    from playwright.sync_api import sync_playwright

    launch_kwargs = {"headless": not _HEADED}
    if _HEADED:
        launch_kwargs["slow_mo"] = 500
    with sync_playwright() as pw:
        browser = pw.chromium.launch(**launch_kwargs)
        yield browser
        browser.close()


def test_page_loads_and_shows_title(browser, server_url):
    context = browser.new_context()
    page = context.new_page()
    page.goto(server_url)

    expect(page).to_have_title("Artefact Agent")
    expect(page.locator(".brand")).to_contain_text("Artefact")
    expect(page.locator("#userInput")).to_be_visible()
    expect(page.locator("#sendBtn")).to_be_visible()

    context.close()


def test_empty_state_with_suggestions(browser, server_url):
    context = browser.new_context()
    page = context.new_page()
    page.goto(server_url)

    expect(page.locator(".empty-state")).to_be_visible()
    suggestion_btns = page.locator(".suggestion-btn")
    expect(suggestion_btns.first).to_be_visible()
    assert suggestion_btns.count() == 3

    context.close()


def test_typing_in_input_enables_send(browser, server_url):
    context = browser.new_context()
    page = context.new_page()
    page.goto(server_url)

    send_btn = page.locator("#sendBtn")
    expect(send_btn).to_be_disabled()

    page.locator("#userInput").fill("hello")
    expect(send_btn).to_be_enabled()

    context.close()


def test_send_message_shows_user_message(browser, server_url):
    context = browser.new_context()
    page = context.new_page()
    page.goto(server_url)

    page.locator("#userInput").fill("What is the capital of France?")
    page.locator("#sendBtn").click()

    page.locator(".message.user").wait_for(timeout=10000)
    msg = page.locator(".message.user")
    expect(msg).to_contain_text("What is the capital of France?")
    page.locator(".message.agent").wait_for(timeout=30000)
    expect(page.locator(".message.agent")).to_be_visible()

    context.close()


def test_suggestion_button_sends_query(browser, server_url):
    context = browser.new_context()
    page = context.new_page()
    page.goto(server_url)

    page.locator(".suggestion-btn").first.click()
    page.locator(".message.user").wait_for(timeout=10000)
    page.locator(".message.agent").wait_for(timeout=30000)

    expect(page.locator(".message.agent")).to_be_visible()
    expect(page.locator(".typing-dots")).to_be_hidden()

    context.close()


def test_health_status_indicator(browser, server_url):
    context = browser.new_context()
    page = context.new_page()
    page.goto(server_url)

    page.locator(".status-dot.online").wait_for(timeout=10000)
    expect(page.locator(".status-dot.online")).to_be_visible()
    expect(page.locator(".status-label")).to_contain_text("online")

    context.close()
