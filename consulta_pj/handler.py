import asyncio
import logging
import time
from functools import wraps

import backoff
from pydantic import BaseModel
from tortoise.exceptions import BaseORMException

from consulta_pj.crawler import CausaSchema, IncidenteSchema, InformacionLitigante, LitiganteTipo, crawler

from .concurrency import gather_with_concurrency, log_progress
from .db_service import DBService


def timeme(func):
    @wraps(func)
    async def process(func, *args, **params):
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **params)
        else:
            return func(*args, **params)

    @wraps(func)
    async def helper(*args, **params):
        logging.info("{}.time".format(func.__name__))
        start = time.time()
        result = await process(func, *args, **params)
        logging.info(f"Time - {func.__name__}: {time.time() - start}")
        return result

    return helper


class ProcessResponse(BaseModel):
    successful: list[str]
    error: dict[str, str]


async def process_actores_info(cedulas_actores: list[str], max_concurrency: int = 15) -> None:
    tasks = [process_litigante(actor, LitiganteTipo.ACTOR) for actor in cedulas_actores]
    tasks_with_progress = (
        log_progress("Actor", index, len(cedulas_actores), task, level=logging.WARNING)
        for index, task in enumerate(tasks)
    )
    await gather_with_concurrency(max_concurrency, tasks_with_progress)


async def process_demandados_info(cedulas_demandados: list[str], max_concurrency: int = 15) -> None:
    tasks = [process_litigante(actor, LitiganteTipo.DEMANDADO) for actor in cedulas_demandados]
    tasks_with_progress = (
        log_progress("Actor", index, len(cedulas_demandados), task, level=logging.WARNING)
        for index, task in enumerate(tasks)
    )
    await gather_with_concurrency(max_concurrency, tasks_with_progress)


async def process_litigante(cedula: str, tipo: LitiganteTipo) -> ProcessResponse | None:
    try:
        if tipo.ACTOR:
            data = await crawler.get_actor_info(cedula)
        else:
            data = await crawler.get_demandado_info(cedula)
        start_time = time.time()
        logging.info(f"Persisting data for litigante {data.litigante.nombre}")
        response = await persist_causas(data)
        end_time = time.time()
        logging.info(f"Elapsed time: {end_time-start_time}")
        return response
    except Exception as e:
        logging.exception(e)
        logging.error("Error processing demandado")


# @timeme
# async def process_actor(cedula: str) -> ProcessResponse | None:
#     try:
#         data = await crawler.get_actor_info(cedula)
#         start_time = time.time()
#         logging.info(f"Persisting data for litigante {data.litigante.nombre}")
#         response = await persist_causas(data)
#         end_time = time.time()
#         logging.info(f"Elapsed time: {end_time-start_time}")
#         return response
#     except Exception as e:
#         logging.exception(e)
#         logging.error("Error processing actor")


@timeme
async def persist_causas(data: InformacionLitigante) -> ProcessResponse | None:
    try:
        db_service = DBService()
        tasks_causas = [process_causa(causa) for causa in data.causas]
        id_causas = await gather_with_concurrency(20, tasks_causas)
        successful_causas = [causa for causa, error in id_causas if not error]
        await db_service.update_or_create_litigante(data.litigante, successful_causas)
        error_causas = {causa: error for causa, error in id_causas if error}
        response = ProcessResponse(successful=successful_causas, error=error_causas)
        return response
    except Exception as e:
        pass
        # logging.exception(e)
        # logging.error("Error processing causas")


async def process_causa(causa: CausaSchema) -> tuple[str, str]:
    try:
        db_service = DBService()
        id_causa = await db_service.update_or_create_causa(causa)
        logging.info(f"Causa {causa.idJuicio} persisted with id {id_causa}")

        # judicaturas_tasks = [
        #     db_service.update_or_create_judicatura(movimiento.judicatura)
        #     for movimiento in causa.movimientos
        # ]
        # await gather_with_concurrency(1, judicaturas_tasks)
        await db_service.bulk_create_judicatura([movimiento.judicatura for movimiento in causa.movimientos])
        logging.info("Judicaturas persisted")
        # movimientos_tasks = [
        #     db_service.update_or_create_movimiento(m.idMovimiento, id_causa, m.judicatura.idJudicatura)
        #     for m in causa.movimientos
        # ]
        # await gather_with_concurrency(1, movimientos_tasks)
        await db_service.bulk_create_movimiento(causa.movimientos, id_causa)
        logging.info("Movimientos persisted")

        await db_service.bulk_create_incidente(
            [
                (incidente, movimiento.judicatura.idJudicatura)
                for movimiento in causa.movimientos
                for incidente in movimiento.incidentes
            ]
        )
        logging.info("Incidentes persisted")

        incidentes_tasks = [
            process_incidente(incidente, movimiento.judicatura.idJudicatura)
            for movimiento in causa.movimientos
            for incidente in movimiento.incidentes
        ]
        await gather_with_concurrency(1, incidentes_tasks)

        return id_causa, ""
    except Exception as e:
        logging.exception(e)
        logging.error("aydiohm")
        return causa.idJuicio, str(e)


async def process_incidente(incidente: IncidenteSchema, id_judicatura: int):
    db_service = DBService()
    id_incidente = await db_service.update_or_create_incidente(incidente, id_judicatura)
    for actor in incidente.actores:
        await db_service.update_or_create_implicado(actor, LitiganteTipo.ACTOR, id_incidente)

    for demandado in incidente.demandados:
        await db_service.update_or_create_implicado(demandado, LitiganteTipo.DEMANDADO, id_incidente)

    for actuacion in incidente.actuaciones:
        await db_service.update_or_create_actuacion(actuacion, id_judicatura, id_incidente)


async def process_incidente_old(incidente: IncidenteSchema, id_judicatura: int):
    db_service = DBService()
    id_incidente = await db_service.update_or_create_incidente(incidente, id_judicatura)
    for actor in incidente.actores:
        await db_service.update_or_create_implicado(actor, LitiganteTipo.ACTOR, id_incidente)

    for demandado in incidente.demandados:
        await db_service.update_or_create_implicado(demandado, LitiganteTipo.DEMANDADO, id_incidente)

    for actuacion in incidente.actuaciones:
        await db_service.update_or_create_actuacion(actuacion, id_judicatura, id_incidente)


@backoff.on_exception(backoff.expo, BaseORMException, max_time=60)
async def process_causa_old(causa: CausaSchema) -> tuple[str, str]:
    db_service = DBService()
    id_causa = await db_service.update_or_create_causa(causa)
    judicaturas_tasks = {
        movimiento.judicatura.idJudicatura: db_service.get_or_create_judicatura(movimiento.judicatura)
        for movimiento in causa.movimientos
    }
    await gather_with_concurrency(20, judicaturas_tasks.values())
    for movimiento in causa.movimientos:
        judicatura_id = movimiento.judicatura.idJudicatura

        await db_service.update_or_create_movimiento(movimiento.idMovimiento, id_causa, judicatura_id)

        for incidente in movimiento.incidentes:
            id_incidente = await db_service.update_or_create_incidente(incidente, judicatura_id)

            for actor in incidente.actores:
                await db_service.get_or_create_implicado(actor, LitiganteTipo.ACTOR, id_incidente)

            for demandado in incidente.demandados:
                await db_service.get_or_create_implicado(demandado, LitiganteTipo.DEMANDADO, id_incidente)

            for actuacion in incidente.actuaciones:
                await db_service.update_or_create_actuacion(actuacion, judicatura_id, id_incidente)
    return id_causa, ""
    # except Exception:
    #     raise
    # logging.exception(e)
    # logging.error("aydiohm")
    # return causa.idJuicio, str(e)


@backoff.on_exception(backoff.expo, BaseORMException, max_time=60)
async def process_causa_old2(causa: CausaSchema) -> tuple[str, str]:
    db_service = DBService()
    id_causa = await db_service.update_or_create_causa(causa)
    for movimiento in causa.movimientos:
        judicatura = movimiento.judicatura
        id_judicatura = await db_service.update_or_create_judicatura(judicatura)
        await db_service.update_or_create_movimiento(movimiento.idMovimiento, id_causa, id_judicatura)

        for incidente in movimiento.incidentes:
            id_incidente = await db_service.update_or_create_incidente(incidente, id_judicatura)

            for actor in incidente.actores:
                await db_service.update_or_create_implicado(actor, LitiganteTipo.ACTOR, id_incidente)

            for demandado in incidente.demandados:
                await db_service.update_or_create_implicado(demandado, LitiganteTipo.DEMANDADO, id_incidente)

            for actuacion in incidente.actuaciones:
                await db_service.update_or_create_actuacion(actuacion, id_judicatura, id_incidente)
    return id_causa, ""
    # except Exception:
    #     raise
    # logging.exception(e)
    # logging.error("aydiohm")
    # return causa.idJuicio, str(e)
