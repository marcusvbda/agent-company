from uuid import uuid4

from ..providers.base import BaseProvider


class Agent:
    def __init__(
        self,
        name: str,
        provider: BaseProvider,
        instructions: str = "",
    ):
        self.id: str = str(uuid4())
        self.name = name
        self.provider = provider
        self.instructions = instructions
