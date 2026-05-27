from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field


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
