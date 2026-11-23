from ..model.agent import Agent
from ..providers.chatgpt import ChatGPTProvider

MOCK = [
    Agent("Mark", ChatGPTProvider()),
    Agent("Nina", ChatGPTProvider()),
]
