import logging

from fastapi import FastAPI, Path
from fastapi.openapi.models import Example
from tortoise.contrib.fastapi import register_tortoise

from . import handler
from .crawler import LitiganteTipo
from .db_service import DBService
from .handler import ProcessResponse
from .models import (
    Actuacion,
    Actuacion_Pydantic,
    Causa,
    Causa_Pydantic,
    Implicado,
    Incidente,
    Litigante,
    Movimiento,
    Movimiento_Pydantic,
)

logging.basicConfig(level=logging.INFO)


ACTORES_EXAMPLES: dict[str, Example] = {
    "0968599020001": Example(value="0968599020001"),
    "0992339411001": Example(value="0992339411001"),
    "1722218474": Example(value="1722218474"),
}
DEMANDADOS_EXAMPLES = {"1791251237001": {"value": "1791251237001"}, "0968599020001": {"value": "0968599020001"}}
PROCESOS_EXAMPLES = {"Actor": {"value": "02331202200019"}, "Demandado": {"value": "17230202115775"}}
CAUSA_EXAMPLE = {"1722218474": {"value": "1722218474"}}
MOVIMIENTO_EXAMPLE = {"25957977": {"value": 25957977}}


app = FastAPI(title="Prueba Tusdatos.co")


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/stats")
async def get_stats() -> dict[str, int]:
    return {
        "litigantes": await Litigante.all().count(),
        "causas": await Causa.all().count(),
        "movimientos": await Movimiento.all().count(),
        "actuaciones": await Actuacion.all().count(),
        "incidentes": await Incidente.all().count(),
        "implicados": await Implicado.all().count(),
    }


@app.get("/litigantes/{cedula}", response_model=ProcessResponse)
async def process_litigante_data(
    cedula: str = Path(..., openapi_examples=ACTORES_EXAMPLES),
) -> ProcessResponse | None:
    response = await handler.process_litigante(cedula, LitiganteTipo.ACTOR)
    return response


# Only for verification
@app.get("/causas/actores/{cedula}", response_model=list[Causa_Pydantic], tags=["verificacion"])
async def get_causas_actor(cedula: str = Path(..., openapi_examples=CAUSA_EXAMPLE)):
    db_service = DBService()
    response = await db_service.get_causas_by_actor_id(cedula)
    return response


@app.get("/causasId/actores/{cedula}")
async def get_causas_id_actor(cedula: str = Path(..., openapi_examples=ACTORES_EXAMPLES)) -> list[str]:
    db_service = DBService()
    response = await db_service.get_causas_ids_by_actor_id(cedula)
    return response


# Only for verification
@app.get("/causas/actores/{cedula}/movimientos", response_model=list[Movimiento_Pydantic], tags=["verificacion"])
async def get_movimientos_actor(cedula: str = Path(..., openapi_examples=CAUSA_EXAMPLE)):
    db_service = DBService()
    response = await db_service.get_moviminetos_by_actor_id(cedula)
    return response


# Only for verification
@app.get(
    "/causas/actores/{cedula}/movimientos/{movimiento_id}/actuaciones",
    response_model=list[Actuacion_Pydantic],
    tags=["verificacion"],
)
async def get_actor_actuaciones_by_movimiento_id(
    cedula: str = Path(..., openapi_examples=CAUSA_EXAMPLE),
    movimiento_id: int = Path(..., openapi_examples=MOVIMIENTO_EXAMPLE),
):
    db_service = DBService()
    response = await db_service.get_actor_actuaciones_by_movimiento_id(cedula, movimiento_id)
    return response


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",  # "sqlite://db.sqlite3",  # or in memory db: "sqlite://:memory:"
    modules={"models": ["consulta_pj.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
