from typing import Any

from consulta_pj.client import CausaActor, CausasRequest
from consulta_pj.crawler import LitiganteSchema, LitiganteTipo, crawler
from tests.mocks.client import mock_get_actuaciones_judiciales, mock_get_causas, mock_get_movimientos


@mock_get_causas
@mock_get_movimientos
@mock_get_actuaciones_judiciales
async def test_crawler_get_litigante_info(informacion_litigante_1234: dict[str, Any]):
    litigante = LitiganteSchema(cedula="1234", tipo=LitiganteTipo.ACTOR)
    causas = CausasRequest(actor=CausaActor(cedulaActor="1234"))

    informacion_litigante_result = await crawler.get_litigante_info(litigante, causas, 1)

    assert informacion_litigante_result is not None
    assert informacion_litigante_result.litigante.cedula == "1234"
    assert len(informacion_litigante_result.causas) == 3
    assert informacion_litigante_1234 == informacion_litigante_result


@mock_get_causas
@mock_get_movimientos
@mock_get_actuaciones_judiciales
async def test_crawler_get_actor_info(informacion_litigante_1234: dict[str, Any]):
    informacion_litigante_result = await crawler.get_actor_info("1234")

    assert informacion_litigante_result is not None
    assert informacion_litigante_result.litigante.cedula == "1234"
    assert len(informacion_litigante_result.causas) == 3
    assert informacion_litigante_1234 == informacion_litigante_result
