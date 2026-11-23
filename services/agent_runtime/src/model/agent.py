from uuid import uuid4


class Agent:
    def __init__(self, name: str):
        self.id: str = str(uuid4())
        self.name = name
