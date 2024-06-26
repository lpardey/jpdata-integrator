from tortoise.contrib.pydantic import PydanticModel

from consulta_pj.crawler import (
    CausaSchema,
    ImplicadoSchema,
    JudicaturaSchema,
    LitiganteSchema,
    LitiganteTipo,
    MovimientoSchema,
)
from consulta_pj.models import (
    Actuacion,
    Causa,
    Causa_Pydantic,
    Implicado,
    Incidente,
    Judicatura,
    Litigante,
    Movimiento,
    Movimiento_Pydantic,
)

from .schemas import CreateActuacionRequest, CreateIncidenteRequest
from .serializers import SerializedActuacionSchema, SerializedCausaSchema, _serialize_causa


class DBService:
    async def update_or_create_litigante(self, litigante: LitiganteSchema, causas_ids: list[str]) -> str:
        litigante_object, _ = await Litigante.update_or_create(cedula=litigante.cedula)
        causas = await Causa.filter(idJuicio__in=causas_ids)
        if litigante.tipo == LitiganteTipo.ACTOR:
            await litigante_object.causas_actor.add(*causas)
        else:
            await litigante_object.causas_demandado.add(*causas)
        await litigante_object.save()
        return litigante_object.cedula

    async def get_or_create_causa(self, causa: CausaSchema) -> str:
        causa_object, _ = await Causa.get_or_create(
            {
                "nombreDelito": causa.nombreDelito.strip(),
                "fechaIngreso": causa.fechaIngreso,
            },
            idJuicio=causa.idJuicio,
        )
        return causa_object.idJuicio

    async def update_or_create_causa(self, causa: CausaSchema) -> str:
        causa_object, _ = await Causa.update_or_create(
            idJuicio=causa.idJuicio,
            defaults={"nombreDelito": causa.nombreDelito.strip(), "fechaIngreso": causa.fechaIngreso},
        )
        return causa_object.idJuicio

    async def bulk_create_causa(self, causas: list[CausaSchema]) -> list[str]:
        new_causas = [
            Causa(
                idJuicio=causa.idJuicio,
                nombreDelito=causa.nombreDelito.strip(),
                fechaIngreso=causa.fechaIngreso,
            )
            for causa in causas
        ]
        await Causa.bulk_create(new_causas, ignore_conflicts=True)
        return [causa.idJuicio for causa in new_causas]

    async def get_or_create_judicatura(self, judicatura: JudicaturaSchema) -> str:
        judicatura_object, _ = await Judicatura.get_or_create(
            {
                "ciudad": judicatura.ciudad.strip(),
                "nombreJudicatura": judicatura.nombre.strip(),
            },
            idJudicatura=judicatura.idJudicatura,
        )
        return judicatura_object.idJudicatura

    async def update_or_create_judicatura(self, judicatura: JudicaturaSchema) -> str:
        judicatura_object, _ = await Judicatura.update_or_create(
            idJudicatura=judicatura.idJudicatura,
            defaults={
                "ciudad": judicatura.ciudad.strip(),
                "nombreJudicatura": judicatura.nombre.strip(),
            },
        )
        return judicatura_object.idJudicatura

    async def bulk_create_judicatura(self, judicaturas: list[JudicaturaSchema]) -> list[str]:
        new_judicaturas = [
            Judicatura(
                idJudicatura=judicatura.idJudicatura,
                ciudad=judicatura.ciudad.strip(),
                nombreJudicatura=judicatura.nombre.strip(),
            )
            for judicatura in judicaturas
        ]
        await Judicatura.bulk_create(new_judicaturas, ignore_conflicts=True)
        return [judicatura.idJudicatura for judicatura in new_judicaturas]

    async def get_or_create_movimiento(self, id_movimiento: int, causa_id: str) -> int:
        movimiento, _ = await Movimiento.get_or_create(
            {"causa_id": causa_id},
            idMovimientoJuicioIncidente=id_movimiento,
        )
        return movimiento.idMovimientoJuicioIncidente

    async def update_or_create_movimiento(self, id_movimiento: int, causa_id: str) -> int:
        movimiento, _ = await Movimiento.update_or_create(
            idMovimientoJuicioIncidente=id_movimiento, defaults={"causa_id": causa_id}
        )
        return movimiento.idMovimientoJuicioIncidente

    async def bulk_create_movimiento(self, movimientos: list[MovimientoSchema], causa_id: str) -> list[int]:
        new_movimientos = [
            Movimiento(idMovimientoJuicioIncidente=movimiento.idMovimiento, causa_id=causa_id)
            for movimiento in movimientos
        ]
        await Movimiento.bulk_create(new_movimientos, ignore_conflicts=True)
        return [movimiento.idMovimientoJuicioIncidente for movimiento in new_movimientos]

    async def get_or_create_incidente(self, request: CreateIncidenteRequest) -> int:
        incidente_object, _ = await Incidente.get_or_create(
            {
                "fechaCrea": request.incidente.fechaCrea,
                "judicatura_id": request.judicatura_id,
            },
            idIncidente=request.incidente.idIncidente,
        )
        return incidente_object.idIncidente

    async def update_or_create_incidente(self, request: CreateIncidenteRequest) -> int:
        incidente_object, _ = await Incidente.update_or_create(
            idIncidente=request.incidente.idIncidente,
            defaults={"fechaCrea": request.incidente.fechaCrea, "judicatura_id": request.judicatura_id},
        )
        return incidente_object.idIncidente

    async def bulk_create_incidente(self, requests: list[CreateIncidenteRequest]) -> list[int]:
        new_incidentes = [
            Incidente(
                idIncidente=request.incidente.idIncidente,
                fechaCrea=request.incidente.fechaCrea,
                judicatura_id=request.judicatura_id,
                movimiento_id=request.movimiento_id,
            )
            for request in requests
        ]
        await Incidente.bulk_create(new_incidentes, ignore_conflicts=True)
        return [incidente.idIncidente for incidente in new_incidentes]

    async def get_or_create_implicado(self, implicado: ImplicadoSchema, tipo: LitiganteTipo, incidente_id: int) -> int:
        implicado_object, _ = await Implicado.get_or_create(
            {"nombre": implicado.nombre, "representante": implicado.representante},
            id=implicado.idImplicado,
        )
        incidente = await Incidente.get(idIncidente=incidente_id)
        if tipo == LitiganteTipo.ACTOR:
            await implicado_object.incidentes_actor.add(incidente)
        else:
            await implicado_object.incidentes_demandado.add(incidente)
        return implicado_object.id

    async def update_or_create_implicado(
        self, implicado: ImplicadoSchema, tipo: LitiganteTipo, incidente_id: int
    ) -> int:
        representante = implicado.representante.strip() if implicado.representante else None
        implicado_object, _ = await Implicado.update_or_create(
            id=implicado.idImplicado, defaults={"nombre": implicado.nombre, "representante": representante}
        )
        incidente = await Incidente.get(idIncidente=incidente_id)
        if tipo == LitiganteTipo.ACTOR:
            await implicado_object.incidentes_actor.add(incidente)
        else:
            await implicado_object.incidentes_demandado.add(incidente)
        return implicado_object.id

    async def get_or_create_actuacion(self, request: CreateActuacionRequest) -> int:
        actuacion_object, _ = await Actuacion.get_or_create(
            {
                "codigo": request.actuacion.codigo,
                "actividad": request.actuacion.actividad,
                "fecha": request.actuacion.fecha,
                "tipo": request.actuacion.tipo.strip(),
                "judicatura_id": request.judicatura_id,
                "incidente_id": request.incidente_id,
                "nombreArchivo": request.actuacion.nombreArchivo.strip() if request.actuacion.nombreArchivo else None,
            },
            uuid=request.actuacion.uuid,
        )
        return actuacion_object.codigo

    async def update_or_create_actuacion(self, request: CreateActuacionRequest) -> int:
        actuacion_object, _ = await Actuacion.update_or_create(
            uuid=request.actuacion.uuid,
            defaults={
                "uuid": request.actuacion.uuid,
                "codigo": request.actuacion.codigo,
                "actividad": request.actuacion.actividad,
                "fecha": request.actuacion.fecha,
                "tipo": request.actuacion.tipo.strip(),
                "judicatura_id": request.judicatura_id,
                "incidente_id": request.incidente_id,
                "nombreArchivo": request.actuacion.nombreArchivo.strip() if request.actuacion.nombreArchivo else None,
            },
        )
        return actuacion_object.uuid

    async def bulk_create_actuacion(self, requests: list[CreateActuacionRequest]) -> list[int]:
        new_actuaciones = [
            Actuacion(
                uuid=request.actuacion.uuid,
                codigo=request.actuacion.codigo,
                incidente_id=request.incidente_id,
                actividad=request.actuacion.actividad,
                fecha=request.actuacion.fecha,
                tipo=request.actuacion.tipo.strip(),
                judicatura_id=request.judicatura_id,
                nombreArchivo=request.actuacion.nombreArchivo.strip() if request.actuacion.nombreArchivo else None,
            )
            for request in requests
        ]
        await Actuacion.bulk_create(new_actuaciones, ignore_conflicts=True)
        return [actuacion.uuid for actuacion in new_actuaciones]

    async def get_causas_by_actor_id(self, cedula: str) -> list[PydanticModel]:
        actor = await Litigante.get(cedula=cedula).prefetch_related("causas_actor")
        raw_causas = await actor.causas_actor.all()
        causas = [await Causa_Pydantic.from_tortoise_orm(causa) for causa in raw_causas]
        return causas

    async def get_causas_by_demandado_id(self, cedula: str) -> list[PydanticModel]:
        demandado = await Litigante.get(cedula=cedula).prefetch_related("causas_demandado")
        raw_causas = await demandado.causas_demandado.all()
        causas = [await Causa_Pydantic.from_tortoise_orm(causa) for causa in raw_causas]
        return causas

    async def get_causas_ids_by_actor_id(self, cedula: str) -> list[str]:
        actor = await Litigante.get(cedula=cedula).prefetch_related("causas_actor")
        causas: list[str] = await actor.causas_actor.all().values_list("idJuicio", flat=True)  # type: ignore
        return causas

    async def get_causas_ids_by_demandado_id(self, cedula: str) -> list[str]:
        demandado = await Litigante.get(cedula=cedula).prefetch_related("causas_demandado")
        causas: list[str] = await demandado.causas_demandado.all().values_list("idJuicio", flat=True)  # type: ignore
        return causas

    async def get_moviminetos_by_actor_id(self, cedula: str) -> list[PydanticModel]:
        actor = await Litigante.get(cedula=cedula).prefetch_related("causas_actor__movimientos__judicatura")
        raw_movimientos = [movimiento for causa in actor.causas_actor for movimiento in causa.movimientos]
        movimientos = [await Movimiento_Pydantic.from_tortoise_orm(movimiento) for movimiento in raw_movimientos]
        return movimientos

    async def get_moviminetos_by_demandado_id(self, cedula: str) -> list[PydanticModel]:
        demandado = await Litigante.get(cedula=cedula).prefetch_related("causas_demandado__movimientos__judicatura")
        raw_movimientos = [movimiento for causa in demandado.causas_demandado for movimiento in causa.movimientos]
        movimientos = [await Movimiento_Pydantic.from_tortoise_orm(movimiento) for movimiento in raw_movimientos]
        return movimientos

    async def get_causas_by_cedula(self, cedula: str, tipo: LitiganteTipo) -> list[SerializedCausaSchema]:
        if tipo == LitiganteTipo.ACTOR:
            raw_causas = await Causa.filter(actores__cedula=cedula).prefetch_related(
                "actores", "demandados", "movimientos__incidentes", "movimientos__incidentes__judicatura"
            )
        else:
            raw_causas = await Causa.filter(demandados__cedula=cedula).prefetch_related(
                "actores", "demandados", "movimientos__incidentes", "movimientos__incidentes__judicatura"
            )
        causas = [await _serialize_causa(causa) for causa in raw_causas]
        return causas

    async def get_actuaciones_by_incidente(self, incidente_id: int) -> list[SerializedActuacionSchema]:
        incidente = await Incidente.get(idIncidente=incidente_id).prefetch_related("actuaciones")
        actuaciones_raw = await incidente.actuaciones.all()
        actuaciones = [SerializedActuacionSchema.model_validate(actuacion) for actuacion in actuaciones_raw]
        return actuaciones
