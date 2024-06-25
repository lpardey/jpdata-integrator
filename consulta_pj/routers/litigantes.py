from fastapi import APIRouter, Path

from consulta_pj.crawler import LitiganteTipo
from consulta_pj.handler import ProcessResponse, handler

from .default_examples import ACTORES_EXAMPLES, DEMANDADOS_EXAMPLES

router = APIRouter(prefix="/litigantes", tags=["Litigantes"])


@router.get("/actores/{cedula}")
async def process_actor_data(cedula: str = Path(..., openapi_examples=ACTORES_EXAMPLES)) -> ProcessResponse | None:
    response = await handler.process_litigante(cedula, LitiganteTipo.ACTOR)
    return response


@router.get("/demandantes/{cedula}")
async def process_demandante_data(
    cedula: str = Path(..., openapi_examples=DEMANDADOS_EXAMPLES),
) -> ProcessResponse | None:
    response = await handler.process_litigante(cedula, LitiganteTipo.DEMANDADO)
    return response
