from pydantic import BaseModel


class SectorResponse(BaseModel):
    name: str