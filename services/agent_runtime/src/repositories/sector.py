from ..model.sector import Sector

class SectorRepository:
    def __init__(self):
        self.sectores : list[Sector] = []
        
    def get_all(self) -> list[Sector]:
        return self.sectors