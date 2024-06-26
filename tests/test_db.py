import pytest

from consulta_pj.crawler.schemas import LitiganteSchema, LitiganteTipo
from consulta_pj.db_service import DBService
from consulta_pj.models import Litigante


@pytest.fixture(autouse=True)
async def auto_in_memory_db(in_memory_db):
    yield


async def test_get_actor():
    await Litigante.create(cedula="1234")
    actor = await Litigante.get(cedula="1234")
    assert actor.cedula == "1234"


async def test_create_actor_without_causas():
    db_service = DBService()
    causas_ids = []
    actor = LitiganteSchema(cedula="3456", nombre="Prueba", tipo=LitiganteTipo.ACTOR)
    actor_id = await db_service.update_or_create_litigante(actor, causas_ids)
    litigante_in_db = await Litigante.get(cedula=actor_id)
    causas_in_db = await litigante_in_db.causas_actor.all()

    assert await Litigante.all().count() == 1
    assert actor_id == actor.cedula == litigante_in_db.cedula
    assert len(causas_ids) == len(causas_in_db)


async def test_create_actors_with_previously_existing_causas():
    db_service = DBService()
    existing_causas_ids = ["1234", "5678"]
    actor = LitiganteSchema(cedula="3456", nombre="Prueba", tipo=LitiganteTipo.ACTOR)
    actor_id = await db_service.update_or_create_litigante(actor, existing_causas_ids)
    new_causas_ids = ["1234", "5678", "9012"]
    await db_service.update_or_create_litigante(actor, new_causas_ids)

    all_causas_ids = set(existing_causas_ids) | set(new_causas_ids)
    litigante_in_db = await Litigante.get(cedula=actor_id)
    causas_in_db = await litigante_in_db.causas_actor.all()

    assert await Litigante.all().count() == 1
    assert actor_id == actor.cedula == litigante_in_db.cedula
    assert len(causas_in_db) == len(all_causas_ids)


async def test_create_demandados():
    db_service = DBService()
    causas_ids = ["1234", "5678"]
    demandado = LitiganteSchema(cedula="3456", nombre="Prueba", tipo=LitiganteTipo.DEMANDADO)
    demandados_ids = await db_service.update_or_create_litigante(demandado, causas_ids)

    assert len(demandados_ids) == 2
    assert demandados_ids == causas_ids
    assert await Litigante.all().count() == 2
    assert await Litigante.filter(cedula__in=causas_ids).count() == 2


async def test_create_demandados_with_previously_existing_demandados():
    db_service = DBService()
    existing_causas_ids = ["1234", "5678"]
    demandado = LitiganteSchema(cedula="3456", nombre="Prueba", tipo=LitiganteTipo.DEMANDADO)
    await db_service.update_or_create_litigante(demandado, existing_causas_ids)

    new_causas_ids = ["1234", "5678", "9012"]
    demandados_ids = await db_service.update_or_create_litigante(demandado, new_causas_ids)

    all_ids = set(existing_causas_ids) | set(new_causas_ids)

    assert len(demandados_ids) == 3
    assert demandados_ids == all_ids
    assert await Litigante.all().count() == 3
    assert await Litigante.filter(cedula__in=all_ids).count() == 3
