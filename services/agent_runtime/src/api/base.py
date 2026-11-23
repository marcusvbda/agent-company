from typing import Annotated, Any, Protocol

from fastapi import APIRouter, Depends, HTTPException


class Repository(Protocol):
    def get(self) -> list[Any]: ...

    def find(self, id: str) -> Any | None: ...


class BaseAPI:
    def __init__(self, repository_class: type[Repository], resource_name: str):
        self.router = APIRouter()

        RepositoryDep = Annotated[repository_class, Depends()]

        @self.router.get("/")
        async def get_all(repository: RepositoryDep):
            return repository.get()

        @self.router.get("/{id}")
        async def find_one(id: str, repository: RepositoryDep):
            item = repository.find(id)
            if item is None:
                raise HTTPException(
                    status_code=404, detail=f"{resource_name} not found"
                )
            return item
