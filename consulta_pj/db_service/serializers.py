import itertools
from datetime import datetime
from typing import Iterable

from pydantic import BaseModel, ConfigDict

from consulta_pj.crawler.schemas import JudicaturaSchema, LitiganteSchema, LitiganteTipo
from consulta_pj.models import Causa, Incidente, Judicatura


class SerializedActuacionSchema(BaseModel):
    codigo: int
    fecha: datetime
    tipo: str
    actividad: str
    nombreArchivo: str | None

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class SerializedImplicadoSchema(BaseModel):
    id: int
    nombre: str
    representante: str | None

    model_config = ConfigDict(from_attributes=True)


class SerializedIncidenteSchema(BaseModel):
    idIncidente: int
    fechaCrea: datetime | None
    actores: list[SerializedImplicadoSchema]
    demandados: list[SerializedImplicadoSchema]
    actuaciones: list[SerializedActuacionSchema]

    model_config = ConfigDict(from_attributes=True)


class GroupedMovimientosSchema(BaseModel):
    judicatura: JudicaturaSchema
    incidentes: list[SerializedIncidenteSchema]

    model_config = ConfigDict(from_attributes=True)


class SerializedMovimientoSchema(BaseModel):
    idMovimientoJuicioIncidente: int
    incidentes: list[SerializedIncidenteSchema]


class SerializedCausaSchema(BaseModel):
    idJuicio: str
    nombreDelito: str
    fechaIngreso: datetime
    actores: list[LitiganteSchema]
    demandados: list[LitiganteSchema]
    movimientos: list[GroupedMovimientosSchema]


async def get_causas_by_cedula(cedula: str, tipo: LitiganteTipo) -> list[SerializedCausaSchema]:
    if tipo == LitiganteTipo.ACTOR:
        raw_causas = await Causa.filter(actores__cedula=cedula).prefetch_related(
            "actores", "demandados", "movimientos__incidentes", "movimientos__incidentes__judicatura"
        )
    else:
        raw_causas = await Causa.filter(demandados__cedula=cedula).prefetch_related(
            "actores", "demandados", "movimientos__incidentes", "movimientos__incidentes__judicatura"
        )
    causas = [await _serialize_causa(causa) for causa in raw_causas]
    return causas


async def _serialize_causa(causa: Causa) -> SerializedCausaSchema:
    raw_actores = await causa.actores.all()
    raw_demandados = await causa.demandados.all()
    actores = [LitiganteSchema(cedula=actor.cedula, tipo=LitiganteTipo.ACTOR) for actor in raw_actores]
    demandados = [LitiganteSchema(cedula=actor.cedula, tipo=LitiganteTipo.DEMANDADO) for actor in raw_demandados]
    grouped_incidentes = await get_incidentes_by_causa(causa.idJuicio)
    serialized_causa = SerializedCausaSchema(
        idJuicio=causa.idJuicio,
        nombreDelito=causa.nombreDelito,
        fechaIngreso=causa.fechaIngreso,
        actores=actores,
        demandados=demandados,
        movimientos=grouped_incidentes,
    )
    return serialized_causa


async def get_incidentes_by_causa(idJuicio: int) -> list[GroupedMovimientosSchema]:
    incidentes_raw = (
        await Incidente.filter(movimiento__causa__idJuicio=idJuicio)
        .prefetch_related("judicatura")
        .order_by("judicatura__idJudicatura")
    )
    grouped_incidentes = itertools.groupby(incidentes_raw, key=lambda incidente: incidente.judicatura.idJudicatura)
    grouped_movimientos = [
        await _serialize_grouped_movimientos(judicatura_id, incidentes)
        for judicatura_id, incidentes in grouped_incidentes
    ]
    return grouped_movimientos


async def _serialize_grouped_movimientos(
    judicatura_id: int, incidentes: Iterable[Incidente]
) -> GroupedMovimientosSchema:
    incidentes = [await _serialize_incident(incidente) for incidente in incidentes]
    raw_judicatura = await Judicatura.get(idJudicatura=judicatura_id)
    judicatura = JudicaturaSchema(
        idJudicatura=raw_judicatura.idJudicatura, nombre=raw_judicatura.nombreJudicatura, ciudad=raw_judicatura.ciudad
    )
    grouped_movimiento = GroupedMovimientosSchema(judicatura=judicatura, incidentes=incidentes)
    return grouped_movimiento


async def _serialize_incident(incidente: Incidente) -> SerializedIncidenteSchema:
    actores_raw = await incidente.actores.all()
    demandados_raw = await incidente.demandados.all()
    actuaciones_raw = await incidente.actuaciones.all()

    actores = [SerializedImplicadoSchema.model_validate(actor) for actor in actores_raw]
    demandados = [SerializedImplicadoSchema.model_validate(demandado) for demandado in demandados_raw]
    actuaciones = [SerializedActuacionSchema.model_validate(actuacion) for actuacion in actuaciones_raw]

    return SerializedIncidenteSchema(
        idIncidente=incidente.idIncidente,
        fechaCrea=incidente.fechaCrea,
        actores=actores,
        demandados=demandados,
        actuaciones=actuaciones,
    )


async def get_actuaciones_by_incidente(incidente_id: int) -> list[SerializedActuacionSchema]:
    incidente = await Incidente.get(idIncidente=incidente_id).prefetch_related("actuaciones")
    actuaciones_raw = await incidente.actuaciones.all()
    actuaciones = [SerializedActuacionSchema.model_validate(actuacion) for actuacion in actuaciones_raw]
    return actuaciones
