from datetime import datetime

from pydantic import BaseModel


class ActuacionesRequest(BaseModel):
    aplicativo: str = "web"
    idIncidenteJudicatura: int
    idJudicatura: str
    idJuicio: str
    idMovimientoJuicioIncidente: int
    incidente: int
    nombreJudicatura: str


class CausaActor(BaseModel):
    cedulaActor: str = ""
    nombreActor: str = ""


class CausaDemandado(BaseModel):
    cedulaDemandado: str = ""
    nombreDemandado: str = ""


class PaginatedRequest(BaseModel):
    page: int = 1
    size: int = 10


class CausasRequest(BaseModel):
    numeroCausa: str = ""
    actor: CausaActor = CausaActor()
    demandado: CausaDemandado = CausaDemandado()
    provincia: str = ""
    numeroFiscalia: str = ""
    recaptcha: str = "verdad"


class CausasRequestBody(CausasRequest, PaginatedRequest):
    pass


class ContarCausasRequest(CausasRequest):
    pass


class CausasResponse(BaseModel):
    idJuicio: str
    estadoActual: str | None = None
    idMateria: int | None = None
    idProvincia: int | None = None
    idCanton: int | None = None
    idJudicatura: int | None = None
    nombreDelito: str
    fechaIngreso: datetime
    nombre: str | None = None
    cedula: str | None = None
    idEstadoJuicio: int | None = None
    nombreMateria: str | None = None
    nombreEstadoJuicio: str | None = None
    nombreJudicatura: str | None = None
    nombreTipoResolucion: str | None = None
    nombreTipoAccion: str | None = None
    fechaProvidencia: datetime | None = None
    nombreProvidencia: str | None = None
    nombreProvincia: str | None = None
    iedocumentoAdjunto: str | None = None


class Actuacion(BaseModel):
    codigo: int
    idJudicatura: str
    idJuicio: str
    fecha: datetime
    tipo: str
    actividad: str
    visible: str
    origen: str
    idMovimientoJuicioIncidente: int
    ieTablaReferencia: str
    ieDocumentoAdjunto: str
    escapeOut: str
    uuid: str
    alias: str
    nombreArchivo: str
    tipoIngreso: str
    idTablaReferencia: str


class ActuacionesResponse(BaseModel):
    actuaciones: list[Actuacion]


class JudicaturaSchema(BaseModel):
    idJudicatura: str
    nombreJudicatura: str
    ciudad: str


class LitiganteSchema(BaseModel):
    idLitigante: int
    tipoLitigante: str
    nombresLitigante: str
    representadoPor: str | None


class IncidenteSchema(BaseModel):
    incidente: int
    idIncidenteJudicatura: int
    idMovimientoJuicioIncidente: int
    idJudicaturaDestino: str
    fechaCrea: datetime
    lstLitiganteActor: list[LitiganteSchema] | None
    lstLitiganteDemandado: list[LitiganteSchema] | None
    litiganteActor: str | None = None
    litiganteDemandado: str | None = None


class MovimientoSchema(JudicaturaSchema):
    lstIncidenteJudicatura: list[IncidenteSchema]


class MovimientosResponse(BaseModel):
    movimientos: list[MovimientoSchema]


def get_actuaciones_request(
    idJuicio: str,
    incidente: IncidenteSchema,
    movimiento: MovimientoSchema,
) -> ActuacionesRequest:
    return ActuacionesRequest(
        idIncidenteJudicatura=incidente.idIncidenteJudicatura,
        idJudicatura=movimiento.idJudicatura,
        idJuicio=idJuicio,
        idMovimientoJuicioIncidente=incidente.idMovimientoJuicioIncidente,
        incidente=incidente.incidente,
        nombreJudicatura=movimiento.nombreJudicatura,
    )
