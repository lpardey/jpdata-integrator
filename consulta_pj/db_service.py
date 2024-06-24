import logging

from consulta_pj.crawler.schemas import MovimientoSchema

from .crawler import (
    ActuacionSchema,
    CausaSchema,
    ImplicadoSchema,
    IncidenteSchema,
    JudicaturaSchema,
    LitiganteSchema,
    LitiganteTipo,
)
from .models import Actuacion, Causa, Implicado, Incidente, Judicatura, Litigante, Movimiento


class DBService:
    async def get_or_create_litigante(self, litigante: LitiganteSchema, ids_causas: list[str]) -> str:
        litigante_object, created = await Litigante.get_or_create(cedula=litigante.cedula)
        logging.info(f"Litigante: {litigante_object} created: {created}")
        causas = await Causa.filter(idJuicio__in=ids_causas)
        if litigante.tipo == LitiganteTipo.ACTOR:
            await litigante_object.causas_actor.add(*causas)
        else:
            await litigante_object.causas_demandado.add(*causas)
        await litigante_object.save()
        return litigante_object.cedula

    async def update_or_create_litigante(self, litigante: LitiganteSchema, ids_causas: list[str]) -> str:
        litigante_object, _ = await Litigante.update_or_create(cedula=litigante.cedula)
        causas = await Causa.filter(idJuicio__in=ids_causas)
        if litigante.tipo == LitiganteTipo.ACTOR:
            await litigante_object.causas_actor.add(*causas)
        else:
            await litigante_object.causas_demandado.add(*causas)
        await litigante_object.save()
        return litigante_object.cedula

    async def get_or_create_causa(self, causa: CausaSchema) -> str:
        causa_object, _ = await Causa.get_or_create(
            {
                "idJuicio": causa.idJuicio,
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

    async def get_or_create_judicatura(self, judicatura: JudicaturaSchema) -> int:
        judicatura_object, _ = await Judicatura.get_or_create(
            {
                "idJudicatura": judicatura.idJudicatura,
                "ciudad": judicatura.ciudad.strip(),
                "nombreJudicatura": judicatura.nombre.strip(),
            },
            idJudicatura=judicatura.idJudicatura,
        )
        return judicatura_object.idJudicatura

    async def update_or_create_judicatura(self, judicatura: JudicaturaSchema) -> int:
        judicatura_object, _ = await Judicatura.update_or_create(
            idJudicatura=judicatura.idJudicatura,
            defaults={
                "ciudad": judicatura.ciudad.strip(),
                "nombreJudicatura": judicatura.nombre.strip(),
            },
        )
        return judicatura_object.idJudicatura

    async def bulk_create_judicatura(self, judicaturas: list[JudicaturaSchema]) -> list[int]:
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

    # async def bulk_update_or_create_judicaturas(
    #     self, judicaturas: list[JudicaturaSchema]
    # ) -> tuple[set[int], set[int]]:
    #     judicaturas_ids = {judicatura.idJudicatura for judicatura in judicaturas}
    #     existing_judicaturas = set(
    #         await Judicatura.filter(idJudicatura__in=judicaturas_ids).values_list("idJudicatura", flat=True)
    #     )
    #     judicaturas_to_create = judicaturas_ids - existing_judicaturas
    #     new_judicaturas = [
    #         Judicatura(
    #             idJudicatura=judicatura.idJudicatura, ciudad=judicatura.ciudad, nombreJudicatura=judicatura.nombre
    #         )
    #         for judicatura in judicaturas
    #         if judicatura.idJudicatura in judicaturas_to_create
    #     ]
    #     await Judicatura.bulk_create(new_judicaturas)
    #     return (judicaturas_to_create, existing_judicaturas)

    async def get_or_create_movimiento(self, id_movimiento: int, causa_id: str, judicatura_id: int) -> int:
        movimiento, _ = await Movimiento.get_or_create(
            {"idMovimientoJuicioIncidente": id_movimiento, "causa_id": causa_id, "judicatura_id": judicatura_id},
            idMovimientoJuicioIncidente=id_movimiento,
        )
        return movimiento.idMovimientoJuicioIncidente

    async def update_or_create_movimiento(self, id_movimiento: int, causa_id: str, judicatura_id: int) -> int:
        movimiento, _ = await Movimiento.update_or_create(
            idMovimientoJuicioIncidente=id_movimiento, defaults={"causa_id": causa_id, "judicatura_id": judicatura_id}
        )
        return movimiento.idMovimientoJuicioIncidente

    async def bulk_create_movimiento(self, movimientos: list[MovimientoSchema], causa_id: str) -> list[int]:
        new_movimientos = [
            Movimiento(
                idMovimientoJuicioIncidente=movimiento.idMovimiento,
                causa_id=causa_id,
                judicatura_id=movimiento.judicatura.idJudicatura,
            )
            for movimiento in movimientos
        ]
        await Movimiento.bulk_create(new_movimientos, ignore_conflicts=True)
        return [movimiento.idMovimientoJuicioIncidente for movimiento in new_movimientos]

    async def get_or_create_incidente(self, incidente: IncidenteSchema, judicatura_id: int) -> int:
        incidente_object, _ = await Incidente.get_or_create(
            {
                "idIncidente": incidente.idIncidente,
                "fechaIngreso": incidente.fechaCrea,
                "judicatura_id": judicatura_id,
            },
            idIncidente=incidente.idIncidente,
        )
        return incidente_object.idIncidente

    async def update_or_create_incidente(self, incidente: IncidenteSchema, judicatura_id: int) -> int:
        incidente_object, _ = await Incidente.update_or_create(
            idIncidente=incidente.idIncidente,
            defaults={"fechaIngreso": incidente.fechaCrea, "judicatura_id": judicatura_id},
        )
        return incidente_object.idIncidente

    async def bulk_create_incidente(self, data: list[tuple[IncidenteSchema, int]]) -> list[int]:
        new_incidentes = [
            Incidente(
                idIncidente=incidente.idIncidente,
                fechaIngreso=incidente.fechaCrea,
                judicatura_id=judicatura_id,
            )
            for incidente, judicatura_id in data
        ]
        await Incidente.bulk_create(new_incidentes, ignore_conflicts=True)
        return [incidente.idIncidente for incidente in new_incidentes]

    async def get_or_create_implicado(self, implicado: ImplicadoSchema, tipo: LitiganteTipo, incidente_id) -> int:
        implicado_object, _ = await Implicado.get_or_create(
            {"id": implicado.idImplicado, "nombre": implicado.nombre, "representante": implicado.representante},
            id=implicado.idImplicado,
        )
        incidente = await Incidente.get(idIncidente=incidente_id)
        if tipo == LitiganteTipo.ACTOR:
            await implicado_object.incidentes_actor.add(incidente)
        else:
            await implicado_object.incidentes_demandado.add(incidente)
        return implicado_object.id

    async def update_or_create_implicado(self, implicado: ImplicadoSchema, tipo: LitiganteTipo, incidente_id) -> int:
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

    async def get_or_create_actuacion(self, actuacion: ActuacionSchema, judicatura_id: int, incidente_id: int) -> int:
        actuacion_object, _ = await Actuacion.get_or_create(
            {
                "codigo": actuacion.codigo,
                "actividad": actuacion.actividad,
                "fecha": actuacion.fecha,
                "tipo": actuacion.tipo.strip(),
                "judicatura_id": judicatura_id,
                "incidente_id": incidente_id,
                "nombreArchivo": actuacion.nombreArchivo.strip(),
            },
            codigo=actuacion.codigo,
            incidente__idIncidente=incidente_id,
        )
        return actuacion_object.codigo

    async def update_or_create_actuacion(
        self, actuacion: ActuacionSchema, judicatura_id: int, incidente_id: int
    ) -> int:
        actuacion_object, _ = await Actuacion.update_or_create(
            codigo=actuacion.codigo,
            incidente__idIncidente=incidente_id,
            defaults={
                "actividad": actuacion.actividad,
                "fecha": actuacion.fecha,
                "tipo": actuacion.tipo.strip(),
                "judicatura_id": judicatura_id,
                "incidente_id": incidente_id,
                "nombreArchivo": actuacion.nombreArchivo.strip(),
            },
        )
        return actuacion_object.codigo

    async def get_causas_by_actor_id(self, cedula: str) -> list[str]:
        actor = await Litigante.get(cedula=cedula).prefetch_related("causas_actor")
        causas = await actor.causas_actor.all().values_list("idJuicio", flat=True)
        return causas  # type: ignore

    async def get_causas_by_demandado_id(self, cedula: str) -> list[str]:
        demandado = await Litigante.get(cedula=cedula).prefetch_related("causas_demandado")
        causas = await demandado.causas_demandado.all().values_list("idJuicio", flat=True)
        return causas  # type: ignore

    # async def get_causa_by_id(self, id: str) -> Causa | None:
    #     causa = await Causa.get_or_none(idJuicio=id).prefetch_related("litigantes", "movimientos")
    #     return causa

    # async def get_or_create_litigantes_by_id(self, cedulas: set[str]) -> set[str]:
    #     existing_litigantes_ids: set[str] = set(
    #         await Litigante.filter(cedula__in=cedulas).values_list("cedula", flat=True)  # type: ignore
    #     )
    #     litigantes_to_create = cedulas - existing_litigantes_ids
    #     new_litigantes = [await Litigante.create(cedula=cedula) for cedula in litigantes_to_create]
    #     new_ids = existing_litigantes_ids | {litigante.cedula for litigante in new_litigantes}
    #     return new_ids

    # async def _update_causa(self, data: CausasResponse) -> Causa:
    #     causa = await Causa.get(idJuicio=data.idJuicio)
    #     await causa.update_from_dict(data.model_dump())
    #     await causa.save()
    #     return causa

    # async def _update_or_create_causas(self, causas: list[CausasResponse]) -> list[Causa]:
    #     all_ids = [causa.idJuicio for causa in causas]
    #     existing_procesos_ids: list[str] = list(
    #         await Causa.filter(idJuicio__in=all_ids).values_list("idJuicio", flat=True)  # type: ignore
    #     )

    #     causas_to_create = [causa for causa in causas if causa.idJuicio not in existing_procesos_ids]
    #     causas_to_update = [causa for causa in causas if causa.idJuicio in existing_procesos_ids]

    #     new_causas = [await Causa.create(**causa.model_dump()) for causa in causas_to_create]
    #     updated_causas = [await self._update_causa(causa) for causa in causas_to_update]

    #     causas = new_causas + updated_causas
    #     return causas

    # async def update_actor_causas(self, cedula_actor: str, causas: list[CausasResponse]) -> list[str]:
    #     litigante = await Litigante.get(cedula=cedula_actor)
    #     causas = await self._update_or_create_causas(causas)
    #     await litigante.causas_actor.add(*causas)

    #     all_idJuicio = [causa.idJuicio for causa in causas]
    #     return all_idJuicio

    # async def update_demandado_causas(self, cedula_demandado: str, causas: list[CausasResponse]) -> list[str]:
    #     demandado = await Litigante.get(cedula=cedula_demandado)
    #     causas = await self._update_or_create_causas(causas, demandado)
    #     await demandado.causas_demandado.add(*causas)

    #     all_idJuicio = [causa.idJuicio for causa in causas]
    #     return all_idJuicio

    # async def update_or_create_movimiento_causa(self, data: MovimientoCausaSchema) -> Movimiento:
    #     causa = await Causa.get(idJuicio=data.causa.idJuicio)
    #     # causa = await self.get_causa_by_id(data.causa.idJuicio)
    #     # if causa is None:
    #     #     causa = await Causa.create(**data.causa.model_dump())
    #     judicatura = await Judicatura.get(data.judicatura.idJudicatura)
    #     movimiento_causa = await Movimiento.get_or_none(causa=causa.idJuicio, judicatura=judicatura.idJudicatura)
    #     if movimiento_causa is None:
    #         movimiento_causa = await Movimiento.create(causa=causa.idJuicio, judicatura=judicatura.idJudicatura)
    #     return movimiento_causa

    # async def get_or_create_implicados_by_id(self, ids: set[str]) -> set[str]:
    #     existing_implicados_ids = set(await Implicado.filter(cedula__in=ids).values_list("id", flat=True))
    #     implicados_to_create = ids - existing_implicados_ids
    #     new_implicados = [await Implicado.create(id=id) for id in implicados_to_create]
    #     new_ids = existing_implicados_ids | {implicado.id for implicado in new_implicados}
    #     return new_ids

    # async def update_or_create_judicatura(self, data: JudicaturaSchema) -> str:
    #     judicatura = await Judicatura.get_or_none(idJudicatura=data.idJudicatura)
    #     if judicatura is None:
    #         judicatura = await Judicatura.create(**data.model_dump(exclude={"lstIncidenteJudicatura"}))
    #     await self._update_incidentes_judicatura(judicatura, data.lstIncidenteJudicatura)
    #     return judicatura.idJudicatura

    # async def _update_incidentes_judicatura(self, judicatura: Judicatura, incidentes: list[IncidenteSchema]):
    #     pass

    # # async def update_movimientos(
    # #     self, id_juicio: list[str], movimientos:
    # # ) -> list[str]:
    # #     proceso = await Proceso.get(idJuicio=id_juicio)
    # #     await InformacionAdicionalDeProceso.filter(juicio=proceso).delete()
    # #     fresh_informaciones = [
    # #         await InformacionAdicionalDeProceso.create(**info.model_dump(), juicio=proceso)
    # #         for info in informacion.causas
    # #     ]
    # #     result = [info.id for info in fresh_informaciones]
    # #     return result
