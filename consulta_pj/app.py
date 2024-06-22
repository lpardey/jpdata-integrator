import logging

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from . import crawler
from .client import ProcesosJudicialesClient
from .schemas import (
    ActuacionesJudicialesRequest,
    CausaActor,
    CausaDemandado,
    CausasSchema,
    GetExisteIngresoDirectoRequest,
)

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


# @app.get("/actor/{cedula}")
# async def get_actor(cedula: str):
#     await crawler.get_actor_info(cedula)
#     return {"status": "ok"}


# @app.get("/demandado/{cedula}")
# async def get_demandado(cedula: str):
#     await crawler.get_demandado_info(cedula)
#     return {"status": "ok"}


@app.post("/adquirirCausasActores")
async def adquirir_causas_actores(actores: list[str]):
    await crawler.get_actores_info(actores)
    return {"status": "ok"}


@app.post("/adquirirCausasDemandados")
async def adquirir_causas_demandados(actores: list[str]):
    await crawler.get_demandados_info(actores)
    return {"status": "ok"}


@app.post("/adquirirCausas")
async def adquirir_causas(cedulas: list[str]):
    await crawler.get_actores_info(cedulas)
    await crawler.get_demandados_info(cedulas)
    return {"status": "ok"}


# @app.get("/causas/actor/{cedula}")
# async def get_causas_actor(cedula: str):
#     async with ProcesosJudicialesClient() as client:
#         "0968599020001"
#         request = CausasSchema(actor=CausaActor(cedulaActor=cedula))
#         response = await client.get_causas(request)
#         return response


# @app.get("/causas/demandado/{cedula}")
# async def get_causas_demandado(cedula: str):
#     async with ProcesosJudicialesClient() as client:
#         "1791251237001"
#         request = CausasSchema(demandado=CausaDemandado(cedulaDemandado=cedula))
#         response = await client.get_causas(request)
#         return response


# @app.get("/proceso/incidentes/{proceso}")
# async def get_incidentes_proceso(proceso: str):
#     "13284202419612"
#     async with ProcesosJudicialesClient() as client:
#         response = await client.get_incidente_judicatura(proceso)
#         return response


# @app.get("/proceso/informacionJuicio/{proceso}")
# async def get_informacion_proceso(proceso: str):
#     "13284202419612"
#     async with ProcesosJudicialesClient() as client:
#         response = await client.get_informacion_juicio(proceso)
#         return response


# @app.get("/proceso/informacionJuicio/{proceso}/ingresoDirecto/{movimiento}")
# async def get_existe_ingreso_directo(proceso: str, movimiento: int):
#     {"idJuicio": "13284202419612", "idMovimientoJuicioIncidente": 26373431}
#     request = GetExisteIngresoDirectoRequest(idJuicio=proceso, idMovimientoJuicioIncidente=movimiento)
#     async with ProcesosJudicialesClient() as client:
#         response = await client.get_existe_ingreso_directo(request)
#         return response


# @app.get("/proceso/informacionJuicio/{proceso}/actuacionesJudiciales/")
# async def get_actuaciones_judiciales(proceso: str):
#     # 13284202419612 proceso  26373431 movimiento
#     # request = {
#     #     "aplicativo": "web",
#     #     "idIncidenteJudicatura": 27748985,
#     #     "idJudicatura": "23331",
#     #     "idJuicio": "23331202402373",
#     #     "idMovimientoJuicioIncidente": 26371178,
#     #     "incidente": 1,
#     #     "nombreJudicatura": "UNIDAD JUDICIAL CIVIL DEL CANTÓN SANTO DOMINGO",
#     # }
#     async with ProcesosJudicialesClient() as client:
#         incidente_judicatura = await client.get_incidente_judicatura(proceso)
#         request = ActuacionesJudicialesRequest(
#             idIncidenteJudicatura=incidente_judicatura.incidentesJudicaturas[0]
#             .lstIncidenteJudicatura[0]
#             .idIncidenteJudicatura,
#             idJudicatura=incidente_judicatura.incidentesJudicaturas[0].idJudicatura,
#             idJuicio=proceso,
#             idMovimientoJuicioIncidente=incidente_judicatura.incidentesJudicaturas[0]
#             .lstIncidenteJudicatura[0]
#             .idMovimientoJuicioIncidente,
#             incidente=incidente_judicatura.incidentesJudicaturas[0].lstIncidenteJudicatura[0].incidente,
#             nombreJudicatura=incidente_judicatura.incidentesJudicaturas[0].nombreJudicatura,
#         )
#         response = await client.get_actuaciones_judiciales(request)
#         return response


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["consulta_pj.models"]},
    add_exception_handlers=True,
    generate_schemas=True,
)
