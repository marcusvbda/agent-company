from .base import BaseProvider


class ClaudeProvider(BaseProvider):
    def __init__(self, name="claude"):
        super().__init__(name)

    def execute(self, prompt: str) -> str:
        return super().execute("claude", "-p", prompt)
