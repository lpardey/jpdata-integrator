from pydantic import BaseModel

from consulta_pj.crawler import ActuacionSchema, IncidenteSchema


class CreateIncidenteRequest(BaseModel):
    incidente: IncidenteSchema
    judicatura_id: str
    movimiento_id: int


class CreateActuacionRequest(BaseModel):
    actuacion: ActuacionSchema
    judicatura_id: str
    incidente_id: int
