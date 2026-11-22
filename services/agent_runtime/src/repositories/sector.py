from ..model.sector import Sector


class SectorRepository:
    def __init__(self):
        self.sectors: list[Sector] = []

    def get_all(self):
        return self.sectors