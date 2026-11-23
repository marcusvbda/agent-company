from uuid import uuid4

from ..providers.base import BaseProvider


class Agent:
    def __init__(
        self,
        name: str,
        provider: BaseProvider,
        sector_id: str | None = None,
        instructions: str = "",
    ):
        self.id: str = str(uuid4())
        self.name = name
        self.provider = provider
        self.sector_id = sector_id
        self.instructions = instructions
