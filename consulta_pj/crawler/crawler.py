import logging

import backoff
import orjson

from consulta_pj.client import ActuacionesResponse as ClientActuacionesResponse
from consulta_pj.client import (
    CausaActor,
    CausaDemandado,
    CausasRequest,
    CausasResponse,
    ProcesosJudicialesClient,
    ProcesosJudicialesClientException,
    get_actuaciones_request,
)
from consulta_pj.client import IncidenteSchema as ClientIncidenteSchema
from consulta_pj.client import LitiganteSchema as ClientLitiganteSchema
from consulta_pj.client import (
    MovimientoSchema as ClientMovimientoSchema,
)
from consulta_pj.concurrency import gather_with_concurrency, log_progress

from .schemas import (
    ActuacionSchema,
    CausaSchema,
    ImplicadoSchema,
    IncidenteSchema,
    InformacionLitigante,
    JudicaturaSchema,
    LitiganteSchema,
    LitiganteTipo,
    MovimientoSchema,
)


async def get_actor_info(cedula: str, max_concurrency: int = 15) -> InformacionLitigante:
    litigante = LitiganteSchema(cedula=cedula, tipo=LitiganteTipo.ACTOR)
    causas_request = CausasRequest(actor=CausaActor(cedulaActor=cedula))
    return await get_litigante_info(litigante, causas_request, max_concurrency)


async def get_demandados_info(cedulas_demandados: list[str], max_concurrency: int = 15) -> None:
    tasks = (get_demandado_info(cedula) for cedula in cedulas_demandados)
    tasks_with_progress = (
        log_progress("Demandado", index, len(cedulas_demandados), task, level=logging.WARNING)
        for index, task in enumerate(tasks)
    )
    await gather_with_concurrency(max_concurrency, tasks_with_progress)


async def get_demandado_info(cedula: str, max_concurrency: int = 15) -> InformacionLitigante:
    litigante = LitiganteSchema(cedula=cedula, tipo=LitiganteTipo.DEMANDADO)
    causas_request = CausasRequest(demandado=CausaDemandado(cedulaDemandado=cedula))
    return await get_litigante_info(litigante, causas_request, max_concurrency)


async def get_litigante_info(
    litigante: LitiganteSchema,
    causas_request: CausasRequest,
    max_concurrency: int,
) -> InformacionLitigante:
    async with ProcesosJudicialesClient() as client:
        causas = await client.get_causas(causas_request)
        total_causas = len(causas)
        tasks = ((causa.idJuicio, get_causa(causa, client)) for causa in causas)
        tasks_with_progress = (
            log_progress(f"Actor {litigante.cedula} - Causa {idJuicio}", index, total_causas, task)
            for index, (idJuicio, task) in enumerate(tasks)
        )
        causas_info = await gather_with_concurrency(max_concurrency, tasks_with_progress)
        result = InformacionLitigante(litigante=litigante, causas=causas_info)
        return result


@backoff.on_exception(backoff.expo, ProcesosJudicialesClientException, max_time=60)
async def get_causa(causa: CausasResponse, client: ProcesosJudicialesClient) -> CausaSchema:
    try:
        movimientos_response = await client.get_movimientos(causa.idJuicio)
        movimientos_raw = [
            await _process_movimiento(causa.idJuicio, movimiento, client)
            for movimiento in movimientos_response.movimientos
        ]
        movimientos = [movimiento for movimiento in movimientos_raw if movimiento is not None]
        causa_schema = CausaSchema(
            idJuicio=causa.idJuicio,
            nombreDelito=causa.nombreDelito,
            fechaIngreso=causa.fechaIngreso,
            movimientos=movimientos,
        )
        return causa_schema
    except ProcesosJudicialesClientException as e:
        logging.exception(e)
        logging.error(f"Error al obtener información de la causa {causa.idJuicio}")
        logging.error(f"Procesando causa {causa.idJuicio}: {orjson.dumps(causa.model_dump()).decode()}")
        raise
    except Exception as e:
        logging.exception(e)
        logging.error("Unexpected error")
        raise


async def _process_movimiento(
    idJuicio: str,
    movimiento: ClientMovimientoSchema,
    client: ProcesosJudicialesClient,
) -> MovimientoSchema | None:
    if not movimiento.lstIncidenteJudicatura:
        return None

    actuaciones_requests = [
        (incidente, get_actuaciones_request(idJuicio, incidente, movimiento))
        for incidente in movimiento.lstIncidenteJudicatura
    ]

    actuaciones_judiciales = [
        (incidente, await client.get_actuaciones(request)) for incidente, request in actuaciones_requests
    ]

    incidentes = [_get_incidentes_schema(incidente, actuaciones) for incidente, actuaciones in actuaciones_judiciales]

    idMovimiento = movimiento.lstIncidenteJudicatura[0].idMovimientoJuicioIncidente
    judicatura = JudicaturaSchema(
        idJudicatura=movimiento.idJudicatura, nombre=movimiento.nombreJudicatura, ciudad=movimiento.ciudad
    )

    result = MovimientoSchema(idMovimiento=idMovimiento, judicatura=judicatura, incidentes=incidentes)
    return result


def _get_incidentes_schema(
    incidente: ClientIncidenteSchema,
    actuaciones_response: ClientActuacionesResponse,
) -> IncidenteSchema:
    actuaciones = [
        ActuacionSchema.model_validate(actuacion, from_attributes=True)
        for actuacion in actuaciones_response.actuaciones
    ]
    actores = _get_implicados(incidente.lstLitiganteActor or [])
    demandados = _get_implicados(incidente.lstLitiganteDemandado or [])
    result = IncidenteSchema(
        idIncidente=incidente.idIncidenteJudicatura,
        fechaCrea=incidente.fechaCrea,
        actuaciones=actuaciones,
        actores=actores,
        demandados=demandados,
    )
    return result


def _get_implicados(litigantes: list[ClientLitiganteSchema]) -> list[ImplicadoSchema]:
    return [
        ImplicadoSchema(
            idImplicado=litigante.idLitigante,
            nombre=litigante.nombresLitigante,
            representante=litigante.representadoPor,
        )
        for litigante in litigantes
    ]
