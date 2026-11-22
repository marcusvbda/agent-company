from ..model.agent import Agent

class AgentRepository:
    def __init__(self):
        self.agents: list[Agent] = []

    def get_all(self):
        return self.agents