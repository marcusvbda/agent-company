from fastapi import APIRouter, Depends

from ..repositories.sector import SectorRepository

router = APIRouter()


@router.get("/")
async def get_sectors(repository: SectorRepository = Depends()):
    return repository.get_all()