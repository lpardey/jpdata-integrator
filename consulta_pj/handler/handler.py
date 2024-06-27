import logging

from consulta_pj.concurrency import gather_with_concurrency, log_progress
from consulta_pj.crawler import CausaSchema, IncidenteSchema, InformacionLitigante, LitiganteTipo, crawler
from consulta_pj.db_service import CreateActuacionRequest, CreateIncidenteRequest, DBService
from consulta_pj.time_decorator import time_async

from .schemas import ProcessResponse


async def process_actores(cedulas_actores: list[str], max_concurrency: int = 15) -> None:
    tasks = [process_litigante(cedula, LitiganteTipo.ACTOR) for cedula in cedulas_actores]
    tasks_with_progress = (
        log_progress("Actor", index, len(cedulas_actores), task, level=logging.WARNING)
        for index, task in enumerate(tasks)
    )
    await gather_with_concurrency(max_concurrency, tasks_with_progress)


async def process_demandados(cedulas_demandados: list[str], max_concurrency: int = 15) -> None:
    tasks = [process_litigante(cedula, LitiganteTipo.DEMANDADO) for cedula in cedulas_demandados]
    tasks_with_progress = (
        log_progress("Demandado", index, len(cedulas_demandados), task, level=logging.WARNING)
        for index, task in enumerate(tasks)
    )
    await gather_with_concurrency(max_concurrency, tasks_with_progress)


@time_async
async def process_litigante(cedula: str, tipo: LitiganteTipo, raise_on_error: bool = False) -> ProcessResponse | None:
    try:
        if tipo == LitiganteTipo.ACTOR:
            data = await crawler.get_actor_info(cedula)
        else:
            data = await crawler.get_demandado_info(cedula)
        response = await persist_causas(data)
        return response
    except Exception as e:
        logging.exception(e)
        logging.error("Error processing demandado")
        if raise_on_error:
            raise e
    return None


@time_async
async def persist_causas(data: InformacionLitigante) -> ProcessResponse:
    tasks_causas = [process_causa(causa) for causa in data.causas]
    id_causas = await gather_with_concurrency(1, tasks_causas)
    successful_causas = [causa for causa, error in id_causas if not error]
    error_causas = {causa: error for causa, error in id_causas if error}
    response = ProcessResponse(successful=successful_causas, error=error_causas)
    try:
        db_service = DBService()
        await db_service.update_or_create_litigante(data.litigante, successful_causas)
        response.litigante_updated = True
    except Exception as e:
        logging.exception(e)
        logging.error("Error associating litigante with causas")
    return response


async def process_causa(causa: CausaSchema) -> tuple[str, str]:
    try:
        db_service = DBService()
        id_causa = await db_service.update_or_create_causa(causa)

        judicaturas = [movimiento.judicatura for movimiento in causa.movimientos]
        await db_service.bulk_create_judicatura(judicaturas)

        await db_service.bulk_create_movimiento(causa.movimientos, id_causa)

        incidentes = [
            CreateIncidenteRequest(
                incidente=incidente,
                judicatura_id=movimiento.judicatura.idJudicatura,
                movimiento_id=movimiento.idMovimiento,
            )
            for movimiento in causa.movimientos
            for incidente in movimiento.incidentes
        ]

        await db_service.bulk_create_incidente(incidentes)

        actuaciones_requests = [
            CreateActuacionRequest(
                actuacion=actuacion,
                judicatura_id=movimiento.judicatura.idJudicatura,
                incidente_id=incidente.idIncidente,
            )
            for movimiento in causa.movimientos
            for incidente in movimiento.incidentes
            for actuacion in incidente.actuaciones
        ]
        await db_service.bulk_create_actuacion(actuaciones_requests)

        incidentes_tasks = [
            process_implicados(incidente) for movimiento in causa.movimientos for incidente in movimiento.incidentes
        ]
        await gather_with_concurrency(1, incidentes_tasks)

        return id_causa, ""
    except Exception as e:
        logging.exception(e)
        logging.error("Unexpected error")
        return causa.idJuicio, str(e)


async def process_implicados(incidente: IncidenteSchema) -> tuple[list[int], list[int]]:
    db_service = DBService()
    id_incidente = incidente.idIncidente
    actores_implicados = [
        await db_service.update_or_create_implicado(actor, LitiganteTipo.ACTOR, id_incidente)
        for actor in incidente.actores
    ]
    demandados_implicados = [
        await db_service.update_or_create_implicado(demandado, LitiganteTipo.DEMANDADO, id_incidente)
        for demandado in incidente.demandados
    ]
    return actores_implicados, demandados_implicados
