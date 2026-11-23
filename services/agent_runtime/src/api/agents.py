from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..model.agent import Agent
from ..providers.base import SYSTEM_PROMPT, WORKSPACES_DIR
from ..providers.claude_provider import ClaudeProvider
from ..repositories.agent_repository import AgentRepository
from ..repositories.sector_repository import SectorRepository
from ..schemas.agent import AgentResponse, CreateAgent, ExecuteResponse, PromptRequest

router = APIRouter(prefix="/agents", tags=["Agents"])

AgentsRepoDep = Annotated[AgentRepository, Depends()]
SectorsRepoDep = Annotated[SectorRepository, Depends()]


@router.get("/")
async def get_all(repository: AgentsRepoDep) -> list[AgentResponse]:
    return repository.get()


@router.post("/", status_code=201)
async def create(
    repository: AgentsRepoDep, sectors: SectorsRepoDep, body: CreateAgent
) -> AgentResponse:
    sector = sectors.find(body.sector_id)
    if sector is None:
        raise HTTPException(status_code=404, detail="Sector not found")
    provider = ClaudeProvider(
        model=body.model,
        effort=body.effort,
        system_prompt=f"{SYSTEM_PROMPT}\n\nYou are {body.name}. {body.instructions}",
    )
    agent = Agent(body.name, provider, sector.id, body.instructions)
    provider.workspace = (WORKSPACES_DIR / agent.id).resolve()
    sector.agents.append(agent)
    return repository.add(agent)


@router.get("/{id}")
async def find_one(repository: AgentsRepoDep, id: str) -> AgentResponse:
    agent = repository.find(id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.post("/{id}/execute")
async def execute(
    repository: AgentsRepoDep, id: str, body: PromptRequest
) -> ExecuteResponse:
    agent = repository.find(id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    try:
        return ExecuteResponse(response=await agent.provider.execute(body.prompt))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
