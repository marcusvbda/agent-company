from typing import Protocol


class HasId(Protocol):
    id: str


class BaseRepository[T: HasId]:
    def __init__(self, items: list[T]):
        self.items = items

    def get(self) -> list[T]:
        return list(self.items)

    def find(self, id: str) -> T | None:
        return next((item for item in self.items if item.id == id), None)
