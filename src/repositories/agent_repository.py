from ..model.agent import Agent
from .base import BaseRepository

_agents: list[Agent] = []


class AgentRepository(BaseRepository[Agent]):
    def __init__(self):
        super().__init__(_agents)
