from .base import BaseProvider


class ChatGPTProvider(BaseProvider):
    def __init__(self, name="chatgpt"):
        super().__init__(name)
