import json
from unittest import mock

from consulta_pj.client import ProcesosJudicialesClient
from consulta_pj.client.schemas import (
    ActuacionesRequest,
    ActuacionesResponse,
    CausasRequest,
    CausasResponse,
    MovimientosResponse,
)


async def get_causas_mocked_data(_, request: CausasRequest) -> list[CausasResponse]:
    filename = f"tests/fixtures/causas_response_{request.actor.cedulaActor or request.demandado.cedulaDemandado}.json"
    with open(filename) as f:
        data = json.load(f)
        return [CausasResponse(**causa) for causa in data]


mock_get_causas = mock.patch.object(ProcesosJudicialesClient, "get_causas", get_causas_mocked_data)


async def get_movimientos(_, proceso: str) -> MovimientosResponse:
    filename = f"tests/fixtures/movimientos_response_{proceso}.json"
    with open(filename) as f:
        data = json.load(f)
        return MovimientosResponse(movimientos=data)


mock_get_movimientos = mock.patch.object(ProcesosJudicialesClient, "get_movimientos", get_movimientos)


async def get_actuaciones(_, request: ActuacionesRequest) -> ActuacionesResponse:
    filename = f"tests/fixtures/actuaciones_judiciales_response_{request.idJuicio}.json"
    with open(filename) as f:
        data = json.load(f)
        return ActuacionesResponse(actuaciones=data)


mock_get_actuaciones_judiciales = mock.patch.object(ProcesosJudicialesClient, "get_actuaciones", get_actuaciones)
