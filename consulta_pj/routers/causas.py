from fastapi import APIRouter, Path
from fastapi.exceptions import HTTPException

from consulta_pj.crawler.schemas import LitiganteTipo
from consulta_pj.db_service import DBService
from consulta_pj.db_service.serializers import SerializedActuacionSchema, SerializedCausaSchema

from .default_examples import ACTORES_EXAMPLES, ACTUACIONES_EXAMPLE, CAUSA_EXAMPLE, DEMANDADOS_EXAMPLES

router = APIRouter(prefix="/causas", tags=["Causas"])


@router.get("/")
async def get_causas_by_id(causas_ids: list[str]) -> list[SerializedCausaSchema]:
    """
    Returns the detailed information of all causas/procesos in the list of causas_ids/idJuicios
    """
    db_service = DBService()
    response = await db_service.get_serialized_causas_by_id(causas_ids)
    return response


@router.get("/ids")
async def get_all_causas_ids() -> list[str]:
    """
    Returns the list of all causas_ids/idJuicios. For demo purposes only
    """
    db_service = DBService()
    response = await db_service.get_all_causas_ids()
    return response


@router.get("/{idJuicio}")
async def get_causa_by_id(idJuicio: str = Path(..., openapi_examples=CAUSA_EXAMPLE)) -> SerializedCausaSchema:
    """
    Returns the detailed information of the causa/proceso with the given causa_id/idJuicio
    """
    db_service = DBService()
    response = await db_service.get_serialized_causas_by_id(idJuicio)
    if not response:
        raise HTTPException(404, detail="Causa not found")
    return response[0]


@router.get("/actores/{cedula}")
async def get_causas_actor(cedula: str = Path(..., openapi_examples=ACTORES_EXAMPLES)) -> list[SerializedCausaSchema]:
    """
    Returns the detailed information of all the causas/procesos for an actor by cedula/id
    """
    db_service = DBService()
    response = await db_service.get_causas_by_cedula(cedula, LitiganteTipo.ACTOR)
    return response


@router.get("/actores/{cedula}/ids")
async def get_causas_ids_actor(cedula: str = Path(..., openapi_examples=ACTORES_EXAMPLES)) -> list[str]:
    """
    Returns the list of all causas/procesos ids/cedulas associated for a given actor by id/cedula
    """
    db_service = DBService()
    response = await db_service.get_causas_ids_by_actor_id(cedula)
    return response


@router.get("/demandados/{cedula}")
async def get_causas_demandado(
    cedula: str = Path(..., openapi_examples=DEMANDADOS_EXAMPLES),
) -> list[SerializedCausaSchema]:
    """
    Returns the detailed information of all the causas/procesos for a demandado by cedula/id
    """
    db_service = DBService()
    response = await db_service.get_causas_by_cedula(cedula, LitiganteTipo.DEMANDADO)
    return response


@router.get("/demandados/{cedula}/ids")
async def get_causas_ids_demandado(cedula: str = Path(..., openapi_examples=DEMANDADOS_EXAMPLES)) -> list[str]:
    """
    Returns the list of all causas/procesos ids/cedulas associated for a given actor by id/cedula
    """
    db_service = DBService()
    response = await db_service.get_causas_ids_by_demandado_id(cedula)
    return response


@router.get("/{idJuicio}/actuaciones")
async def get_actuaciones_by_idJuicio(
    idJuicio: str = Path(..., openapi_examples=ACTUACIONES_EXAMPLE),
) -> list[SerializedActuacionSchema]:
    """
    Returns the list of a detailed information of all actuaciones associated to a given causa/proceso by causa_id/idJuicio
    """
    db_service = DBService()
    response = await db_service.get_actuaciones_by_causa_id(idJuicio)
    return response
