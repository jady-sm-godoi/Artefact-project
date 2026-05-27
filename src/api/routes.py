from __future__ import annotations

from typing import Dict, List, Optional

from agno.agent import Agent
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from src.agent import create_agent, run_with_context


class ToolCall(BaseModel):
    tool_name: str
    input: str
    output: str
    duration_ms: int


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=10000)
    session_id: Optional[str] = None
    verbose: bool = False


class QueryResponse(BaseModel):
    response: str
    tool_calls: Optional[List[ToolCall]] = None


class HealthResponse(BaseModel):
    status: str
    mode: str


router = APIRouter()
_sessions: Dict[str, Agent] = {}


def _build_tool_calls(result) -> List[ToolCall]:
    """Adapter: traduz ToolExecution (Agno) → ToolCall (contrato público)
    isola consumidor da API de detalhes internos do framework.
    Normaliza duration s→ms, desaninha expression de tool_args."""
    tools = getattr(result, "tools", None)
    if not tools:
        return []
    calls: List[ToolCall] = []
    for t in tools:
        expr = ""
        if t.tool_args:
            expr = t.tool_args.get("expression", "")
        duration_ms = 0
        if t.metrics and t.metrics.duration is not None:
            duration_ms = round(t.metrics.duration * 1000)
        calls.append(
            ToolCall(
                tool_name=t.tool_name or "",
                input=expr,
                output=t.result or "",
                duration_ms=duration_ms,
            )
        )
    return calls


@router.post("/query")
async def handle_query(req: QueryRequest, request: Request):
    if req.session_id:
        if req.session_id not in _sessions:
            _sessions[req.session_id] = create_agent(
                session_id=req.session_id
            )
        agent = _sessions[req.session_id]
    else:
        agent = request.app.state.agent
    result = run_with_context(agent, req.query)
    if isinstance(result, str):
        return QueryResponse(response=result)
    content = result.content
    if req.verbose:
        calls = _build_tool_calls(result)
        return QueryResponse(response=content, tool_calls=calls or None)
    return QueryResponse(response=content)


@router.get("/health")
async def handle_health(request: Request):
    ai_ok = getattr(request.app.state, "ai_available", False)
    if ai_ok:
        return HealthResponse(status="ok", mode="full")
    return HealthResponse(status="degraded", mode="calculator-only")
