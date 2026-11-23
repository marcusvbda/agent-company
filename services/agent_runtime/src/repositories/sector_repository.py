from ..mock.sectors_mock import MOCK as mock_sectors
from ..model.sector import Sector
from .base import BaseRepository


class SectorRepository(BaseRepository[Sector]):
    def __init__(self):
        super().__init__(mock_sectors)
