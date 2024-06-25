from fastapi import APIRouter, Path

from consulta_pj.db_service import DBService
from consulta_pj.models import (
    Actuacion_Pydantic,
    Causa_Pydantic,
    Movimiento_Pydantic,
)

from .default_examples import ACTORES_EXAMPLES, CAUSA_EXAMPLE, MOVIMIENTO_EXAMPLE

router = APIRouter(prefix="/causas", tags=["Causas"])


# Only for verification
@router.get("/actores/{cedula}", response_model=list[Causa_Pydantic])
async def get_causas_actor(cedula: str = Path(..., openapi_examples=CAUSA_EXAMPLE)):
    db_service = DBService()
    response = await db_service.get_causas_by_actor_id(cedula)
    return response


@router.get("/actores/{cedula}/ids")
async def get_causas_ids_actor(cedula: str = Path(..., openapi_examples=ACTORES_EXAMPLES)) -> list[str]:
    db_service = DBService()
    response = await db_service.get_causas_ids_by_actor_id(cedula)
    return response


# Only for verification
@router.get("/actores/{cedula}/movimientos", response_model=list[Movimiento_Pydantic])
async def get_movimientos_actor(cedula: str = Path(..., openapi_examples=CAUSA_EXAMPLE)):
    db_service = DBService()
    response = await db_service.get_moviminetos_by_actor_id(cedula)
    return response


# Only for verification
@router.get("/actores/{cedula}/movimientos/{movimiento_id}/actuaciones", response_model=list[Actuacion_Pydantic])
async def get_actuaciones_actor_by_movimiento_id(
    cedula: str = Path(..., openapi_examples=CAUSA_EXAMPLE),
    movimiento_id: int = Path(..., openapi_examples=MOVIMIENTO_EXAMPLE),
):
    db_service = DBService()
    response = await db_service.get_actuaciones_actor_by_movimiento_id(cedula, movimiento_id)
    return response


# DEMANDADOS
# Only for verification
@router.get("/demandados/{cedula}", response_model=list[Causa_Pydantic])
async def get_causas_demandado(cedula: str = Path(..., openapi_examples=CAUSA_EXAMPLE)):
    db_service = DBService()
    response = await db_service.get_causas_by_demandado_id(cedula)
    return response


@router.get("/demandados/{cedula}/ids")
async def get_causas_ids_demandado(cedula: str = Path(..., openapi_examples=ACTORES_EXAMPLES)) -> list[str]:
    db_service = DBService()
    response = await db_service.get_causas_ids_by_demandado_id(cedula)
    return response


# Only for verification
@router.get("/demandados/{cedula}/movimientos", response_model=list[Movimiento_Pydantic])
async def get_movimientos_demandado(cedula: str = Path(..., openapi_examples=CAUSA_EXAMPLE)):
    db_service = DBService()
    response = await db_service.get_moviminetos_by_demandado_id(cedula)
    return response


# Only for verification
@router.get("/demandados/{cedula}/movimientos/{movimiento_id}/actuaciones", response_model=list[Actuacion_Pydantic])
async def get_actuaciones_demandado_by_movimiento_id(
    cedula: str = Path(..., openapi_examples=CAUSA_EXAMPLE),
    movimiento_id: int = Path(..., openapi_examples=MOVIMIENTO_EXAMPLE),
):
    db_service = DBService()
    response = await db_service.get_actuaciones_demandado_by_movimiento_id(cedula, movimiento_id)
    return response
