from consulta_pj.crawler.schemas import InformacionLitigante
from consulta_pj.handler import handler
from consulta_pj.models import Litigante


async def test_handler_persist_causas(informacion_litigante: InformacionLitigante, in_memory_db):
    await handler.persist_causas(informacion_litigante)

    litigante = await Litigante.get(cedula="1234")
    causas_in_db = await litigante.causas_actor.all()

    assert len(causas_in_db) == len(informacion_litigante.causas)
