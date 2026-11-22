from .agent import Agent;

class Sector:
    def __init__(self, name: str, agents: list[Agent]):
        self.name = name
        self.agents = agents
        