from consulta_pj.crawler.schemas import InformacionLitigante
from consulta_pj.db_service.models import Litigante
from consulta_pj.handler import handler


async def test_handler_persist_causas(informacion_litigante_1234: InformacionLitigante, in_memory_db):
    await handler.persist_causas(informacion_litigante_1234)

    litigante = await Litigante.get(cedula="1234")
    causas_in_db = await litigante.causas_actor.all()

    assert len(causas_in_db) == len(informacion_litigante_1234.causas)
