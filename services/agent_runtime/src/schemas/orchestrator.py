from pathlib import Path

from pydantic import BaseModel

from .base import Response


class Step(Response):
    agent: str | None
    workspace: Path | None = None
    task: str
    result: str


class OrchestratorResponse(Response):
    result: str
    steps: list[Step]


# What the orchestrator model must answer (validated, not trusted).
class Delegation(BaseModel):
    agent_id: str
    prompt: str


class Decision(BaseModel):
    delegate: list[Delegation] = []
    final: str | None = None
