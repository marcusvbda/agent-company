from fastapi import FastAPI
from .api.sectors import router as sectors_router

app = FastAPI()

@app.get("/")
async def CheckHealth():
    return 'Ok'

app.include_router(sectors_router, prefix="/sectors", tags=["Sectors"])