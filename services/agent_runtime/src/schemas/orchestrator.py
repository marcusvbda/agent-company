from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from .base import Response

EventType = Literal[
    "run_started",
    "orchestrator_thinking",
    "delegated",
    "agent_working",
    "agent_replied",
    "final",
    "error",
]


class RunEvent(Response):
    type: EventType
    agent: str | None = None
    content: str | None = None
    workspace: Path | None = None


class RunResponse(Response):
    id: str
    prompt: str
    status: Literal["running", "done", "error"]
    events: list[RunEvent]


class Delegation(BaseModel):
    agent_id: str
    prompt: str


class Decision(BaseModel):
    delegate: list[Delegation] = []
    final: str | None = None
