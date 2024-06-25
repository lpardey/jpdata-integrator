from datetime import datetime

from pydantic import BaseModel

class JudicaturaSchema(BaseModel):
    idJudicatura: str
    nombreJudicatura: str
    ciudad: str

class IncidenteSchema(BaseModel):
    idIncidente: str
    fechaCreacion: datetime | None
    tipoIncidente: str
    actores: list[ImplicadoSchema]
    demandados: list[ImplicadoSchema]
    actuaciones: list[ActuacionSchema]

class GroupedMovimientosSchema(BaseModel):
    judicatura: JudicaturaSchema
    incicentes: list[IncidenteSchema]

class CausaSchema(BaseModel):
    idJuicio: str
    nombreDelito: str
    fechaIngreso: datetime
    actores: list[LitiganteSchema]
    demandados: list[LitiganteSchema]
    movimientos: dict[str, GroupedMovimientosSchema]


class CausasResponse(BaseModel):
    cedula: str
    causas: list[CausaSchema]


class ActoresSchema(BaseModel)
