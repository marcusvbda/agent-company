from classes.agent import Agent
from classes.message import Message


class AgentRuntime:
    def __init__(self):
        self.agents = {}

    def register(self, agent: Agent):
        self.agents[agent.name] = agent

    def send(self, message: Message) -> str:
        agent = self.agents[message.recipient]
        
        return agent.execute(message.task)