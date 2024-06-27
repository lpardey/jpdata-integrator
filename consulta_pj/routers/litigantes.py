from fastapi import APIRouter, Path

from consulta_pj.crawler import LitiganteTipo
from consulta_pj.handler import ProcessResponse, handler

from .default_examples import ACTORES_EXAMPLES, DEMANDADOS_EXAMPLES

router = APIRouter(prefix="/litigantes", tags=["Litigantes"])


@router.get("/")
async def get_litigantes(cedula: str, tipo: LitiganteTipo) -> ProcessResponse:
    """
    Returns an object with the ids of the successful and failed processed causas/procesos, and a flag to
    indicate if the litigante was associated with the new causas/proceso
    """
    response = await handler.process_litigante(cedula, tipo, raise_on_error=True)
    # just for typing:
    if response is None:
        raise ValueError("Unexpected error while processing litigante data.")
    return response


@router.get("/actores/{cedula}")
async def process_actor_data(cedula: str = Path(..., openapi_examples=ACTORES_EXAMPLES)) -> ProcessResponse:
    """
    Returns an object with the cedula/id of the successful and failed processed causas/procesos for actores
    """
    response = await handler.process_litigante(cedula, LitiganteTipo.ACTOR, raise_on_error=True)
    # This is just for typing
    if response is None:
        raise ValueError("Unexpected error while processing litigante data.")
    return response


@router.get("/demandantes/{cedula}")
async def process_demandante_data(cedula: str = Path(..., openapi_examples=DEMANDADOS_EXAMPLES)) -> ProcessResponse:
    """
    Returns an object with the cedula/id of the successful and failed processed causas/procesos for demandados
    """
    response = await handler.process_litigante(cedula, LitiganteTipo.DEMANDADO, raise_on_error=True)
    # This is just for typing
    if response is None:
        raise ValueError("Unexpected error while processing litigante data.")
    return response
