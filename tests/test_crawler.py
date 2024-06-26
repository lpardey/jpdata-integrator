import json
from typing import Any

from consulta_pj.client import CausaActor, CausasRequest
from consulta_pj.crawler import InformacionLitigante, LitiganteSchema, LitiganteTipo, crawler
from tests.mocks.client import mock_get_actuaciones_judiciales, mock_get_causas, mock_get_movimientos


@mock_get_causas
@mock_get_movimientos
@mock_get_actuaciones_judiciales
async def test_crawler_get_litigante_info(informacion_litigante_data: dict[str, Any]):
    expected_result = InformacionLitigante(**informacion_litigante_data)
    litigante = LitiganteSchema(cedula="1234", tipo=LitiganteTipo.ACTOR)
    causas = CausasRequest(actor=CausaActor(cedulaActor="1234"))
    informacion_litigante = await crawler.get_litigante_info(litigante, causas, 1)
    assert informacion_litigante is not None
    assert informacion_litigante.litigante.cedula == "1234"
    assert len(informacion_litigante.causas) == 3

    assert expected_result == informacion_litigante


@mock_get_causas
@mock_get_movimientos
@mock_get_actuaciones_judiciales
async def test_crawler_get_actor_info(informacion_litigante_data: dict[str, Any]):
    expected_result = InformacionLitigante(**informacion_litigante_data)
    informacion_litigante = await crawler.get_actor_info("1234")
    assert informacion_litigante is not None
    assert informacion_litigante.litigante.cedula == "1234"
    assert len(informacion_litigante.causas) == 3
    with open("tests/fixtures/informacion_litigante.json", "w") as f:
        asdf = informacion_litigante.model_dump()
        json.dump(asdf, f, indent=4, default=str)
    assert expected_result == informacion_litigante
