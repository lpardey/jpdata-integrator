from fastapi import FastAPI, Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from tortoise.contrib.fastapi import register_tortoise

from consulta_pj.crawler.schemas import InformacionLitigante
from consulta_pj.db_service import DBService

from . import handler
from .crawler import LitiganteTipo, crawler

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


# @app.get("/actor/{cedula}")
# async def get_actor(cedula: str):
#     await crawler.get_actor_info(cedula)
#     return {"status": "ok"}


# @app.get("/demandado/{cedula}")
# async def get_demandado(cedula: str):
#     await crawler.get_demandado_info(cedula)
#     return {"status": "ok"}


# @app.post("/adquirirCausasDemandados")
# async def adquirir_causas_demandados(actores: list[str] = ["1791251237001"]) -> dict[str, str]:
#     await crawler.get_demandados_info(actores)
#     return {"status": "ok"}


# @app.post("/adquirirCausas")
# async def adquirir_causas(cedulas: list[str]) -> dict[str, str]:
#     await crawler.get_actores_info(cedulas)
#     await crawler.get_demandados_info(cedulas)
#     return {"status": "ok"}

ACTORES_EXAMPLES = {"0968599020001": {"value": "0968599020001"}, "0992339411001": {"value": "0992339411001"}}
DEMANDADOS_EXAMPLES = {"1791251237001": {"value": "1791251237001"}, "0968599020001": {"value": "0968599020001"}}
PROCESOS_EXAMPLES = {"Actor": {"value": "02331202200019"}, "Demandado": {"value": "17230202115775"}}


@app.get("/actores/{cedula}")
async def get_actor_info(cedula: str):
    response = await handler.process_litigante(cedula, LitiganteTipo.ACTOR)
    return response


@app.get("/demandados/{cedula}")
async def get_demandado_info(cedula: str) -> InformacionLitigante:
    response = await crawler.get_demandado_info(cedula)
    return response


@app.get("/causas/actor/{cedula}")
async def get_causas_actor(
    cedula: str = Path(..., openapi_examples=ACTORES_EXAMPLES),
) -> list[str]:
    db_service = DBService()
    response = await db_service.get_causas_by_actor_id(cedula)
    return response


@app.get("/causas/demandado/{cedula}")
async def get_causas_demandado(cedula: str = Path(..., openapi_examples=DEMANDADOS_EXAMPLES)) -> list[str]:
    db_service = DBService()
    response = await db_service.get_causas_by_demandado_id(cedula)
    return response


@app.get("/asdf/{cedula}")
async def get_asdf(cedula: str = "0968599020001") -> handler.ProcessResponse | None:
    asdf = await crawler.get_actor_info(cedula)
    with open("qwer.json", "w") as f:
        import json

        json.dump(asdf.model_dump(), f, default=str)


# @app.get("/causas/{id}", response_model=Proceso_Pydantic)
# async def get_proceso(id: str = Path(..., openapi_examples=PROCESOS_EXAMPLES)):
#     db_service = DBService()
#     proceso = await db_service.get_proceso_by_id(id)
#     response = await Proceso_Pydantic.from_tortoise_orm(proceso)
#     return response


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
    db_url="sqlite://db.sqlite3",  # "sqlite://db.sqlite3",  # or in memory db: "sqlite://:memory:"
    modules={"models": ["consulta_pj.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
