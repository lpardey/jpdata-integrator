import logging

import pytest

from consulta_pj.client import CausaActor, CausasRequest
from consulta_pj.concurrency import gather_with_concurrency
from consulta_pj.crawler import LitiganteSchema, LitiganteTipo, crawler
from consulta_pj.time_decorator import time_async

ACTORES = [
    "Mayra Sangoquiza",
    "Luz Mirian Portocarrero Branda",
    "Magaly Elizabeth Montalvan",
    "Fausto Enrique Alvarado Contreras",
    "Vieira Peña Pablo Efrain",
    "Carlos Ricardo Ferber Vera",
    "Nelly Silva De Leon",
    "Leon Silva Pablo Alfredo",
    "Magaly Elizabeth Montalvan Macas",
    "Pachacama Cajilema Maria Ubaldina",
    "Cesat Alfredo Sanchez Naucin",
    "Chavez Aguirre Julio",
    "Gusman Merizalde Juan Vicente",
    "Trujillo Suarez Gloria Alicia",
    "Delgado Piedra Pablo Andres",
]


@pytest.mark.parametrize("max_concurrency", [1, 2, 5, 10, 15])
async def test_crawler_parallel_litigantes(max_concurrency):
    await run_multiple_litigantes(ACTORES, max_concurrency)


@time_async
async def run_multiple_litigantes(actores, max_concurrency):
    litigantes = [LitiganteSchema(cedula="", nombre=nombre, tipo=LitiganteTipo.ACTOR) for nombre in actores]
    causas = [CausasRequest(actor=CausaActor(nombreActor=nombre)) for nombre in actores]
    tasks = [crawler.get_litigante_info(litigante, causa, 1) for litigante, causa in zip(litigantes, causas)]
    results = await gather_with_concurrency(max_concurrency, tasks)
    logging.info(f"Results: {[len(result.causas) for result in results]}")
    return results


@pytest.mark.parametrize("max_concurrency", [1, 5, 15])
async def test_crawler_parallel_causas(max_concurrency):
    informacion_litigantes = await run_multiple_causas("0968599020001", max_concurrency)
    assert informacion_litigantes is not None
    assert len(informacion_litigantes.causas) == 143


@time_async
async def run_multiple_causas(actor_id, max_concurrency):
    informacion_litigantes = await crawler.get_actor_info(actor_id, max_concurrency)
    return informacion_litigantes
