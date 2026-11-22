from ..model.sector import Sector
from ..model.agent import Agent


class SectorRepository:
    def __init__(self):
        self.sectors: list[Sector] = [
            Sector("Designer",[
                Agent("Mark"),
                Agent("Nina"),
            ]),
            Sector("Social Media",[
                Agent("Ana"),
            ])
        ]

    def get_all(self):
        return self.sectors
    