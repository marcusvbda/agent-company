from ..model.sector import Sector
from .base import BaseRepository

_sectors: list[Sector] = []


class SectorRepository(BaseRepository[Sector]):
    def __init__(self):
        super().__init__(_sectors)
