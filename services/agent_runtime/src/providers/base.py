class BaseProvider:
    def __init__(self, name: str):
        self.name = name

    async def execute(self, prompt: str) -> str:
        raise NotImplementedError
