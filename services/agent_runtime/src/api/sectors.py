from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..model.sector import Sector
from ..repositories.sector_repository import SectorRepository
from ..schemas.sector import CreateSector, SectorResponse

router = APIRouter(prefix="/sectors", tags=["Sectors"])

RepositoryDep = Annotated[SectorRepository, Depends()]


@router.get("/")
async def get_all(repository: RepositoryDep) -> list[SectorResponse]:
    return repository.get()


@router.post("/", status_code=201)
async def create(repository: RepositoryDep, body: CreateSector) -> SectorResponse:
    return repository.add(Sector(body.name, []))


@router.get("/{id}")
async def find_one(id: str, repository: RepositoryDep) -> SectorResponse:
    sector = repository.find(id)
    if sector is None:
        raise HTTPException(status_code=404, detail="Sector not found")
    return sector
