from ..mock.agents_mock import MOCK as agents_mock
from ..model.agent import Agent
from .base import BaseRepository


class AgentRepository(BaseRepository[Agent]):
    def __init__(self):
        super().__init__(agents_mock)
