from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class LitiganteTipo(StrEnum):
    ACTOR = "ACTOR"
    DEMANDADO = "DEMANDADO"


class JudicaturaSchema(BaseModel):
    idJudicatura: str
    nombre: str
    ciudad: str


class ImplicadosSchema(BaseModel):
    idImplicado: int
    nombre: str
    representante: str | None


class ActuacionSchema(BaseModel):
    codigo: int
    fecha: datetime
    tipo: str
    actividad: str
    nombreArchivo: str | None


class IncidenteSchema(BaseModel):
    idIncidente: int
    fechaCrea: datetime
    actores: list[ImplicadosSchema]
    demandados: list[ImplicadosSchema]
    actuaciones: list[ActuacionSchema]


class LitiganteSchema(BaseModel):
    cedula: str
    nombre: str = ""
    tipo: LitiganteTipo


class MovimientoSchema(BaseModel):
    idMovimiento: int
    judicatura: JudicaturaSchema
    incidentes: list[IncidenteSchema]


class CausaSchema(BaseModel):
    idJuicio: str
    movimientos: list[MovimientoSchema]


class InformacionLitigante(BaseModel):
    litigante: LitiganteSchema
    causas: list[CausaSchema]
