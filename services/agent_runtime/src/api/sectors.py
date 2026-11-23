from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..repositories.sector_repository import SectorRepository

router = APIRouter()

RepositoryDep = Annotated[SectorRepository, Depends()]


@router.get("/")
async def get_all(repository: RepositoryDep):
    return repository.get()


@router.get("/{id}")
async def find_one(id: str, repository: RepositoryDep):
    sector = repository.find(id)
    if sector is None:
        raise HTTPException(status_code=404, detail="Sector not found")
    return sector
