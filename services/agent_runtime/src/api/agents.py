from ..repositories.agent_repository import AgentRepository
from .base import BaseAPI


class AgentsAPI(BaseAPI):
    def __init__(self):
        super().__init__(AgentRepository, "Agent")


router = AgentsAPI().router
