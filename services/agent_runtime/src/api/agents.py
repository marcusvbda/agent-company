from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..model.agent import Agent
from ..providers.claude_provider import ClaudeProvider
from ..repositories.agent_repository import AgentRepository

router = APIRouter()

AgentsRepoDep = Annotated[AgentRepository, Depends()]


@router.get("/")
async def get_all(repository: AgentsRepoDep):
    return repository.get()


@router.get("/{id}")
async def find_one(repository: AgentsRepoDep, id: str):
    agent = repository.find(id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.get("/test/")
async def test_execute():
    agent = Agent("Mark", ClaudeProvider())
    return await agent.provider.execute("Say Hello")
