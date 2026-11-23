from pathlib import Path

from pydantic import Field

from ..providers.base import Effort
from .base import Request, Response


class CreateAgent(Request):
    name: str = Field(min_length=1)
    instructions: str = ""
    model: str | None = Field(default=None, min_length=1)
    effort: Effort | None = None


class PromptRequest(Request):
    prompt: str = Field(min_length=1)


class ProviderResponse(Response):
    name: str
    model: str | None
    effort: Effort | None
    workspace: Path


class AgentResponse(Response):
    id: str
    name: str
    instructions: str
    provider: ProviderResponse


class ExecuteResponse(Response):
    response: str
