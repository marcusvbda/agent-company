from pydantic import Field

from .agent import AgentResponse
from .base import Request, Response


class CreateSector(Request):
    name: str = Field(min_length=1)


class SectorResponse(Response):
    id: str
    name: str
    agents: list[AgentResponse]
