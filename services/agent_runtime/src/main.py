from fastapi import FastAPI

from .api import agents, orchestrator

app = FastAPI()


for module in (agents, orchestrator):
    app.include_router(module.router)
