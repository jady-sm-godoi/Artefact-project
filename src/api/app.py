from __future__ import annotations

import logging
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request

from src.agent import create_agent
from src.api.routes import router

load_dotenv()

logger = logging.getLogger("artefact-api")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Initializing agent...")
    app.state.agent = create_agent()
    logger.info("Agent ready")
    app.state.ai_available = True
    yield
    logger.info("Shutting down agent...")


app = FastAPI(
    title="Artefact Agent API",
    lifespan=lifespan,
    docs_url="/docs",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.monotonic()
    response = await call_next(request)
    duration = time.monotonic() - start
    logger.info(
        "%s %s %s %.3fms",
        request.method,
        request.url.path,
        response.status_code,
        duration * 1000,
    )
    return response


app.include_router(router)
