from ..model.agent import Agent
from ..providers.claude_provider import ClaudeProvider

MOCK = [
    Agent("Mark", ClaudeProvider()),
    Agent("Nina", ClaudeProvider()),
]
