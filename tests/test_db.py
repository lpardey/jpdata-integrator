import pytest

from consulta_pj.crawler.schemas import InformacionLitigante, LitiganteSchema, LitiganteTipo
from consulta_pj.db_service import DBService
from consulta_pj.db_service.models import Causa, Litigante


@pytest.fixture(autouse=True)
async def auto_in_memory_db(in_memory_db):
    yield


@pytest.mark.parametrize("tipo", [LitiganteTipo.ACTOR, LitiganteTipo.DEMANDADO])
async def test_create_litigante_without_causas(tipo: LitiganteTipo):
    db_service = DBService()
    litigante = LitiganteSchema(cedula="1234", nombre="Prueba", tipo=tipo)

    cedula = await db_service.update_or_create_litigante(litigante, [])
    litigante_in_db = await Litigante.get(cedula=cedula)
    causas_in_db = await litigante_in_db.causas_actor.all()

    assert await Litigante.all().count() == 1
    assert cedula == litigante.cedula == litigante_in_db.cedula
    assert len(causas_in_db) == 0


@pytest.mark.parametrize("tipo", [LitiganteTipo.ACTOR, LitiganteTipo.DEMANDADO])
async def test_create_litigante_with_causas(tipo: LitiganteTipo, informacion_litigante_1234: InformacionLitigante):
    informacion_litigante_1234.litigante.tipo = tipo
    db_service = DBService()
    litigante = LitiganteSchema(cedula="1234", nombre="Prueba", tipo=tipo)
    causas_ids = [await db_service.get_or_create_causa(causa) for causa in informacion_litigante_1234.causas]

    await db_service.update_or_create_litigante(litigante, causas_ids)

    filter_field = "demandados__cedula" if tipo == LitiganteTipo.DEMANDADO else "actores__cedula"
    filter_config = {filter_field: litigante.cedula}
    assert await Causa.filter(**filter_config).count() == 3


@pytest.mark.parametrize("tipo", [LitiganteTipo.ACTOR, LitiganteTipo.DEMANDADO])
async def test_create_litigante_with_previously_existing_causas(
    tipo: LitiganteTipo, informacion_litigante_1234: InformacionLitigante
):
    db_service = DBService()
    litigante = informacion_litigante_1234.litigante
    litigante.tipo = tipo
    existing_causa_id = await db_service.get_or_create_causa(informacion_litigante_1234.causas[0])
    litigante_id = await db_service.update_or_create_litigante(litigante, [existing_causa_id])

    new_causa_id = await db_service.get_or_create_causa(informacion_litigante_1234.causas[1])
    await db_service.update_or_create_litigante(litigante, [new_causa_id])

    litigante_in_db = await Litigante.get(cedula=litigante_id)

    if tipo == LitiganteTipo.DEMANDADO:
        causas_in_db = await litigante_in_db.causas_demandado.all()
    else:
        causas_in_db = await litigante_in_db.causas_actor.all()

    assert litigante_id == litigante.cedula == litigante_in_db.cedula
    assert {causa.idJuicio for causa in causas_in_db} == {existing_causa_id, new_causa_id}
