import pytest

from consulta_pj.crawler.schemas import InformacionLitigante
from consulta_pj.db_service import DBService
from consulta_pj.db_service.serializers import _serialize_grouped_movimientos_list
from consulta_pj.handler import handler
from consulta_pj.models import Actuacion


@pytest.fixture()
async def populate_db_with_litigante_1234(informacion_litigante_1234: InformacionLitigante, in_memory_db):
    await handler.persist_causas(informacion_litigante_1234)


@pytest.fixture()
async def populate_db_with_litigante_5678(informacion_litigante_5678: InformacionLitigante, in_memory_db):
    await handler.persist_causas(informacion_litigante_5678)


async def test_get_actuaciones_by_incidente(
    informacion_litigante_1234: InformacionLitigante, populate_db_with_litigante_1234
):
    db_service = DBService()
    incidente_id = informacion_litigante_1234.causas[0].movimientos[0].incidentes[0].idIncidente

    result = await db_service.get_actuaciones_by_incidente(incidente_id)
    actuaciones = await Actuacion.filter(incidente__idIncidente=incidente_id).all()

    assert len(result) > 0
    assert len(result) == len(actuaciones)
    assert all([actuacion.actividad in [r.actividad for r in result] for actuacion in actuaciones])


async def test_serialize_grouped_movimientos_list(
    informacion_litigante_5678: InformacionLitigante, populate_db_with_litigante_5678
):
    id_juicio = informacion_litigante_5678.causas[0].idJuicio

    result = await _serialize_grouped_movimientos_list(id_juicio)

    assert len(result) == 2
    assert len(result[0].incidentes[0].actuaciones) == 5
    assert len(result[1].incidentes[0].actuaciones) == 2
