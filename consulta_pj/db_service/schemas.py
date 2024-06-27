from pydantic import BaseModel

from consulta_pj.crawler import ActuacionSchema as CrawlerActuacionSchema
from consulta_pj.crawler import IncidenteSchema as CrawlerIncidenteSchema


class CreateIncidenteRequest(BaseModel):
    incidente: CrawlerIncidenteSchema
    judicatura_id: str
    movimiento_id: int


class CreateActuacionRequest(BaseModel):
    actuacion: CrawlerActuacionSchema
    judicatura_id: str
    incidente_id: int
