from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from ..repositories.sector_repository import SectorRepository
from ..schemas.agent import PromptRequest
from ..schemas.orchestrator import OrchestratorResponse
from ..services.orchestrator import run_orchestrator

router = APIRouter(prefix="/orchestrator", tags=["Orchestrator"])

SectorsRepoDep = Annotated[SectorRepository, Depends()]


@router.post("")
async def orchestrate(
    sectors: SectorsRepoDep, body: PromptRequest
) -> OrchestratorResponse:
    try:
        return await run_orchestrator(body.prompt, sectors.get())
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
