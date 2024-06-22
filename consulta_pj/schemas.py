from datetime import datetime

from pydantic import BaseModel


class CausaActor(BaseModel):
    cedulaActor: str = ""
    nombreActor: str = ""


class CausaDemandado(BaseModel):
    cedulaDemandado: str = ""
    nombreDemandado: str = ""


class PaginatedRequest(BaseModel):
    page: int = 1
    size: int = 10


class CausasSchema(BaseModel):
    numeroCausa: str = ""
    actor: CausaActor = CausaActor()
    demandado: CausaDemandado = CausaDemandado()
    provincia: str = ""
    numeroFiscalia: str = ""
    recaptcha: str = "verdad"


class CausasRequest(CausasSchema, PaginatedRequest):
    pass


class ContarCausasRequest(CausasSchema):
    pass


class CausasResponse(BaseModel):
    id: int
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


class LitiganteSchema(BaseModel):
    tipoLitigante: str
    nombresLitigante: str
    representadoPor: str | None
    idLitigante: int


class IncidenteJudicaturaSchema(BaseModel):
    idIncidenteJudicatura: int
    idMovimientoJuicioIncidente: int
    idJudicaturaDestino: str
    fechaCrea: datetime
    incidente: int
    lstLitiganteActor: list[LitiganteSchema] | None
    lstLitiganteDemandado: list[LitiganteSchema] | None
    litiganteActor: str | None = None
    litiganteDemandado: str | None = None


class JudicaturaSchema(BaseModel):
    idJudicatura: str
    nombreJudicatura: str
    ciudad: str
    lstIncidenteJudicatura: list[IncidenteJudicaturaSchema]


class GetIncidenteJudicaturaResponse(BaseModel):
    incidentesJudicaturas: list[JudicaturaSchema]


class GetInformacionJuicioResponse(BaseModel):
    causas: list[CausasResponse]


class GetExisteIngresoDirectoRequest(BaseModel):
    idJuicio: str
    idMovimientoJuicioIncidente: int


class GetExisteIngresoDirectoResponse(BaseModel):
    ingresado: str


class ActuacionesJudicialesRequest(BaseModel):
    aplicativo: str = "web"
    idIncidenteJudicatura: int
    idJudicatura: str
    idJuicio: str
    idMovimientoJuicioIncidente: int
    incidente: int
    nombreJudicatura: str


class ActuacionJudicial(BaseModel):
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


class GetActuacionesJudicialesResponse(BaseModel):
    actuaciones_judiciales: list[ActuacionJudicial]
