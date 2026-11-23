from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from .base import Response

EventType = Literal[
    "run_started",  # content: the user's request
    "orchestrator_thinking",
    "delegated",  # agent + content: the task the orchestrator sent
    "agent_working",  # agent: started working on it
    "agent_replied",  # agent + content: its result (+ workspace with its files)
    "final",  # content: the deliverable (ends the stream)
    "error",  # content: what went wrong (ends the stream)
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


# What the orchestrator model must answer (validated, not trusted).
class Delegation(BaseModel):
    agent_id: str
    prompt: str


class Decision(BaseModel):
    delegate: list[Delegation] = []
    final: str | None = None
