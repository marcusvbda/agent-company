from fastapi import APIRouter, Depends
from ..schema.sector import SectorResponse
from ..repositories.sector import SectorRepository

router = APIRouter()


@router.get("/")
async def get_sectors(repository: SectorRepository = Depends()) -> list[SectorResponse]:
    return repository.get_all()