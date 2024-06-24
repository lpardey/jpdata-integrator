from pydantic import BaseModel


class ProcessResponse(BaseModel):
    successful: list[str]
    error: dict[str, str]
    litigante_updated: bool = False
