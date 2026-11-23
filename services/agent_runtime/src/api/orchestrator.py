from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse

from ..model.run import Run
from ..repositories.run_repository import RunRepository
from ..repositories.sector_repository import SectorRepository
from ..schemas.agent import PromptRequest
from ..schemas.orchestrator import RunResponse
from ..services.orchestrator import execute_run

router = APIRouter(prefix="/orchestrator", tags=["Orchestrator"])

SectorsRepoDep = Annotated[SectorRepository, Depends()]
RunsRepoDep = Annotated[RunRepository, Depends()]


def find_run(runs: RunRepository, id: str) -> Run:
    run = runs.find(id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("", status_code=202)
async def start(
    sectors: SectorsRepoDep,
    runs: RunsRepoDep,
    background: BackgroundTasks,
    body: PromptRequest,
) -> RunResponse:
    """Starts the work and answers right away; follow it on /runs/{id}/events."""
    run = runs.add(Run(body.prompt))
    background.add_task(execute_run, run, sectors.get())
    return run


@router.get("/runs/{id}")
async def get_run(runs: RunsRepoDep, id: str) -> RunResponse:
    return find_run(runs, id)


@router.get("/runs/{id}/events")
async def stream_events(
    runs: RunsRepoDep,
    id: str,
    last_event_id: Annotated[int | None, Header()] = None,
) -> StreamingResponse:
    """Server-Sent Events. Replays what already happened, then follows live.

    The browser's EventSource resends `Last-Event-ID` when it reconnects, so it
    resumes where it stopped. The front must close the stream on final/error.
    """
    run = find_run(runs, id)
    start = 0 if last_event_id is None else last_event_id + 1

    async def sse() -> AsyncIterator[str]:
        async for i, event in run.subscribe(start):
            yield f"id: {i}\nevent: {event.type}\ndata: {event.model_dump_json()}\n\n"

    return StreamingResponse(
        sse(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
