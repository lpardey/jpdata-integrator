import pytest

from consulta_pj.crawler.schemas import InformacionLitigante
from consulta_pj.db_service.serializers import get_actuaciones_by_incidente, get_incidentes_by_causa
from consulta_pj.handler import handler
from consulta_pj.models import Litigante


@pytest.fixture(autouse=True)
async def populated_db(informacion_litigante: InformacionLitigante, in_memory_db):
    await handler.persist_causas(informacion_litigante)


async def test_get_actuaciones_by_incidente(informacion_litigante: InformacionLitigante):
    incidente_id = informacion_litigante.causas[0].movimientos[0].incidentes[0].idIncidente
    expected_result = []
    result = await get_actuaciones_by_incidente(incidente_id)
    assert result == expected_result


async def test_get_incidentes_by_causa(informacion_litigante: InformacionLitigante):
    id_juicio = informacion_litigante.causas[0].idJuicio
    expected_result = []
    result = await get_incidentes_by_causa(id_juicio)
    assert result == expected_result


async def test_handler_persist_causas(informacion_litigante: InformacionLitigante, in_memory_db):
    await handler.persist_causas(informacion_litigante)
    litigante = await Litigante.get(cedula="1234")
    causas = await litigante.causas_actor.all()
    assert len(causas) == 3
