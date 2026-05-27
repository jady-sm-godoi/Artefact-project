from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from src.agent import run_with_context


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


@router.post("/query")
async def handle_query(req: QueryRequest, request: Request):
    agent = request.app.state.agent
    result = run_with_context(agent, req.query)
    if isinstance(result, str):
        return QueryResponse(response=result)
    return QueryResponse(response=result.content)
