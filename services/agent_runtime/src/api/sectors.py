from ..repositories.sector_repository import SectorRepository
from .base import BaseAPI


class SectorsAPI(BaseAPI):
    def __init__(self):
        super().__init__(SectorRepository, "Sector")


router = SectorsAPI().router
