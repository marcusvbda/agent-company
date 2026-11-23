from uuid import uuid4

from .agent import Agent


class Sector:
    def __init__(self, name: str, agents: list[Agent]):
        self.id: str = str(uuid4())
        self.name = name
        self.agents = agents
