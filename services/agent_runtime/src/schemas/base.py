from pydantic import BaseModel, ConfigDict


class Request(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)


class Response(BaseModel):
    model_config = ConfigDict(from_attributes=True)
