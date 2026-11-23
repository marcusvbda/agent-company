from ..model.run import Run
from .base import BaseRepository

_runs: list[Run] = []


class RunRepository(BaseRepository[Run]):
    def __init__(self):
        super().__init__(_runs)
