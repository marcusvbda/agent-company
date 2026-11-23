from fastapi import FastAPI

from .api import agents, orchestrator, sectors

app = FastAPI()


@app.get("/")
async def CheckHealth():
    return "Ok"


for module in (agents, orchestrator, sectors):
    app.include_router(module.router)
