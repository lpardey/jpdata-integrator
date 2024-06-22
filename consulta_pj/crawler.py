import logging

import backoff
import orjson

from consulta_pj.exceptions import ProcesosJudicialesClientException

from .client import ProcesosJudicialesClient
from .concurrency import gather_with_concurrency, log_progress
from .schemas import (
    ActuacionesJudicialesRequest,
    CausaActor,
    CausaDemandado,
    CausasResponse,
    CausasSchema,
    GetExisteIngresoDirectoRequest,
)


async def get_actores_info(cedulas_actores: list[str], max_concurrency: int = 15) -> None:
    tasks = (get_actor_info(cedula) for cedula in cedulas_actores)
    tasks_with_progress = (
        log_progress("Actor", index, len(cedulas_actores), task, level=logging.WARNING)
        for index, task in enumerate(tasks)
    )
    await gather_with_concurrency(max_concurrency, tasks_with_progress)


async def get_actor_info(cedula_actor: str, max_concurrency: int = 15) -> None:
    async with ProcesosJudicialesClient() as client:
        causas_request = CausasSchema(actor=CausaActor(cedulaActor=cedula_actor))
        causas = await client.get_causas(causas_request)
        total_causas = len(causas)
        tasks = ((causa.idJuicio, get_causa(causa, client)) for causa in causas)
        tasks_with_progress = (
            log_progress(f"Actor {cedula_actor} - Causa {idJuicio}", index, total_causas, task)
            for index, (idJuicio, task) in enumerate(tasks)
        )
        await gather_with_concurrency(max_concurrency, tasks_with_progress)


async def get_demandados_info(cedulas_demandados: list[str], max_concurrency: int = 15) -> None:
    tasks = (get_demandado_info(cedula) for cedula in cedulas_demandados)
    tasks_with_progress = (
        log_progress("Demandado", index, len(cedulas_demandados), task, level=logging.WARNING)
        for index, task in enumerate(tasks)
    )
    await gather_with_concurrency(max_concurrency, tasks_with_progress)


async def get_demandado_info(cedula_demandado: str, max_concurrency: int = 15) -> None:
    async with ProcesosJudicialesClient() as client:
        causas_request = CausasSchema(demandado=CausaDemandado(cedulaDemandado=cedula_demandado))
        causas = await client.get_causas(causas_request)
        total_causas = len(causas)
        tasks = ((causa.idJuicio, get_causa(causa, client)) for causa in causas)
        tasks_with_progress = (
            log_progress(f"Demandado {cedula_demandado} - Causa {idJuicio}", index, total_causas, task)
            for index, (idJuicio, task) in enumerate(tasks)
        )
        await gather_with_concurrency(max_concurrency, tasks_with_progress)


@backoff.on_exception(backoff.expo, ProcesosJudicialesClientException, max_time=60)
async def get_causa(causa: CausasResponse, client: ProcesosJudicialesClient) -> None:
    try:
        informacion_juicio = await client.get_informacion_juicio(causa.idJuicio)
        
        incidentes_judicatura = await client.get_incidente_judicatura(causa.idJuicio)

        actuaciones_requests = [
            ActuacionesJudicialesRequest(
                idIncidenteJudicatura=incidente.idIncidenteJudicatura,
                idJudicatura=incidentes.idJudicatura,
                idJuicio=causa.idJuicio,
                idMovimientoJuicioIncidente=incidente.idMovimientoJuicioIncidente,
                incidente=incidente.incidente,
                nombreJudicatura=incidentes.nombreJudicatura,
            )
            for incidentes in incidentes_judicatura.incidentesJudicaturas
            for incidente in incidentes.lstIncidenteJudicatura
        ]

        all_actuaciones_judiciales = [
            (request, await client.get_actuaciones_judiciales(request)) for request in actuaciones_requests
        ]

        requests_ingreso_directo = [
            GetExisteIngresoDirectoRequest(
                idJuicio=causa.idJuicio, idMovimientoJuicioIncidente=incidente.idMovimientoJuicioIncidente
            )
            for incidentes in incidentes_judicatura.incidentesJudicaturas
            for incidente in incidentes.lstIncidenteJudicatura
        ]
        all_ingreso_directo = [
            (request, await client.get_existe_ingreso_directo(request)) for request in requests_ingreso_directo
        ]
    except ProcesosJudicialesClientException as e:
        logging.exception(e)
        logging.error(f"Error al obtener información de la causa {causa.idJuicio}")
        logging.error(f"Procesando causa {causa.idJuicio}: {orjson.dumps(causa.model_dump(), indent=2)}")
        raise
