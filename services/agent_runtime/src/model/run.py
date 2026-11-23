import asyncio
from collections.abc import AsyncIterator
from uuid import uuid4

from ..schemas.orchestrator import RunEvent

TERMINAL = ("final", "error")


class Run:
    def __init__(self, prompt: str):
        self.id: str = str(uuid4())
        self.prompt = prompt
        self.events: list[RunEvent] = []
        self._changed = asyncio.Condition()

    @property
    def finished(self) -> bool:
        return bool(self.events) and self.events[-1].type in TERMINAL

    @property
    def status(self) -> str:
        if not self.finished:
            return "running"
        return "error" if self.events[-1].type == "error" else "done"

    async def publish(self, event: RunEvent) -> None:
        async with self._changed:
            self.events.append(event)
            self._changed.notify_all()

    async def subscribe(self, start: int = 0) -> AsyncIterator[tuple[int, RunEvent]]:
        i = start
        while True:
            async with self._changed:
                await self._changed.wait_for(
                    lambda: i < len(self.events) or self.finished
                )
            if i >= len(self.events):
                return
            yield i, self.events[i]
            i += 1
