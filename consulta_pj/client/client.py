from types import TracebackType
from typing import Self
from urllib.parse import urlencode

import aiohttp
import orjson

from .exceptions import ProcesosJudicialesClientException
from .schemas import (
    ActuacionesJudicialesRequest,
    CausasRequest,
    CausasResponse,
    CausasSchema,
    ContarCausasRequest,
    GetActuacionesJudicialesResponse,
    MovimientosResponse,
)


class WebClient:
    API_URL: str = ""
    BASE_HEADERS: dict[str, str] = dict()

    def __init__(self) -> None:
        self.session: aiohttp.ClientSession | None = None

    def get_headers(self) -> dict[str, str]:
        return self.BASE_HEADERS

    async def __aenter__(self) -> Self:
        self.session = await aiohttp.ClientSession(
            headers=self.get_headers(),
            raise_for_status=self.check_status,
        ).__aenter__()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        if self.session:
            await self.session.__aexit__(exc_type, exc, tb)

    async def check_status(self, response: aiohttp.ClientResponse) -> None:
        pass


class ProcesosJudicialesClient(WebClient):
    API_URL = "https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/"
    BASE_HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Origin": "https://procesosjudiciales.funcionjudicial.gob.ec",
        "Referer": "https://procesosjudiciales.funcionjudicial.gob.ec/",
    }

    async def check_status(self, response: aiohttp.ClientResponse) -> None:
        if response.status >= 400:
            raise ProcesosJudicialesClientException(f"Error en la petición: {response.status} - {response.reason}")

    async def get_contar_causas(self, request: ContarCausasRequest) -> int:
        if not self.session:
            raise ProcesosJudicialesClientException("No hay una sesión activa")
        endpoint = "contarCausas"
        url = f"{self.API_URL}{endpoint}"
        async with self.session.post(url, data=request.model_dump_json()) as response:
            total_causas = int(await response.text())
            return total_causas

    async def get_causas(self, request: CausasSchema) -> list[CausasResponse]:
        if not self.session:
            raise ProcesosJudicialesClientException("No hay una sesión activa")
        endpoint = "buscarCausas"
        contar_causas_request = ContarCausasRequest(**request.model_dump())
        total_causas = await self.get_contar_causas(contar_causas_request)
        pagination = {"page": 1, "size": total_causas}
        url = f"{self.API_URL}{endpoint}?{urlencode(pagination)}"
        data = CausasRequest(**(request.model_dump() | pagination))
        async with self.session.post(url, data=data.model_dump_json()) as response:
            raw_response_data = await response.text()
            response_data = orjson.loads(raw_response_data)
            causas_actor = [CausasResponse(**causa) for causa in response_data]
            return causas_actor

    # async def get_informacion_juicio(self, proceso: str) -> GetInformacionJuicioResponse:
    #     if not self.session:
    #         raise ProcesosJudicialesClientException("No hay una sesión activa")
    #     endpoint = f"getInformacionJuicio/{proceso}"
    #     url = f"{self.API_URL}{endpoint}"
    #     async with self.session.get(url) as response:
    #         raw_response_data = await response.text()
    #         response_data = orjson.loads(raw_response_data)
    #         return GetInformacionJuicioResponse(causas=response_data)

    async def get_movimientos(self, proceso: str) -> MovimientosResponse:
        if not self.session:
            raise ProcesosJudicialesClientException("No hay una sesión activa")
        endpoint = f"getIncidenteJudicatura/{proceso}"
        api_url = "https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-CLEX-SERVICE/api/consulta-causas-clex/informacion/"
        url = f"{api_url}{endpoint}"
        async with self.session.get(url) as response:
            raw_response_data = await response.text()
            response_data = orjson.loads(raw_response_data)
            return MovimientosResponse(movimientos=response_data)

    # async def get_existe_ingreso_directo(
    #     self, request: GetExisteIngresoDirectoRequest
    # ) -> GetExisteIngresoDirectoResponse:
    #     if not self.session:
    #         raise ProcesosJudicialesClientException("No hay una sesión activa")
    #     endpoint = "existeIngresoDirecto"
    #     api_url = "https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-CLEX-SERVICE/api/consulta-causas-clex/informacion/"
    #     url = f"{api_url}{endpoint}"
    #     async with self.session.post(url, data=request.model_dump_json()) as response:
    #         raw_response_data = await response.text()
    #         response_data = GetExisteIngresoDirectoResponse(**orjson.loads(raw_response_data))
    #         return response_data

    async def get_actuaciones_judiciales(
        self, request: ActuacionesJudicialesRequest
    ) -> GetActuacionesJudicialesResponse:
        if not self.session:
            raise ProcesosJudicialesClientException("No hay una sesión activa")
        endpoint = "actuacionesJudiciales"
        url = f"{self.API_URL}{endpoint}"
        async with self.session.post(url, data=request.model_dump_json()) as response:
            raw_response_data = await response.text()
            response_data = orjson.loads(raw_response_data)
            return GetActuacionesJudicialesResponse(actuaciones_judiciales=response_data)
