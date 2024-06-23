from __future__ import annotations

from tortoise import fields
from tortoise.models import Model


class Litigante(Model):
    cedula = fields.CharField(max_length=24, primary_key=True)
    causas_actor: fields.ManyToManyRelation[Causa] = fields.ManyToManyField(
        "models.Causa", related_name="actores", through="causa_litigante_actor"
    )
    causas_demandado: fields.ManyToManyRelation[Causa] = fields.ManyToManyField(
        "models.Causa", related_name="demandados", through="causa_litigante_demandado"
    )

    last_updated = fields.DatetimeField(auto_now=True)


class Causa(Model):
    idJuicio = fields.CharField(max_length=64, primary_key=True)
    nombreDelito = fields.CharField(max_length=255)
    fechaIngreso = fields.DatetimeField()

    litigantes: fields.ManyToManyRelation[Litigante]
    movimientos: fields.ReverseRelation[Movimiento]


class Movimiento(Model):
    idMovimientoJuicioIncidente = fields.IntField(primary_key=True)
    causa: fields.ForeignKeyRelation[Causa] = fields.ForeignKeyField("models.Causa", related_name="movimientos")
    judicatura: fields.ForeignKeyRelation[Judicatura] = fields.ForeignKeyField(
        "models.Judicatura", related_name="movimientos"
    )
    incidentes: fields.ReverseRelation[Incidente]


class Judicatura(Model):
    idJudicatura = fields.IntField(primary_key=True)
    nombreJudicatura = fields.CharField(max_length=255, null=True)
    ciudad = fields.CharField(max_length=255)

    movimientos: fields.ReverseRelation[Movimiento]
    incidentes: fields.ReverseRelation[Incidente]


class Incidente(Model):
    idIncidente = fields.IntField(primary_key=True)
    judicatura: fields.ForeignKeyRelation[Judicatura] = fields.ForeignKeyField(
        "models.Judicatura", related_name="incidentes"
    )

    fechaCrea = fields.DatetimeField()

    actores: fields.ManyToManyRelation[Implicado]
    demandados: fields.ManyToManyRelation[Implicado]

    actuaciones: fields.ReverseRelation[Actuacion]

    last_updated = fields.DatetimeField(auto_now=True)


class Implicado(Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=255)
    representante = fields.CharField(max_length=255)

    incidentes_demandado: fields.ManyToManyRelation[Incidente] = fields.ManyToManyField(
        "models.Incidente", related_name="demandados", through="incidente_implicado_demandado"
    )

    incidentes_actor: fields.ManyToManyRelation[Incidente] = fields.ManyToManyField(
        "models.Incidente", related_name="actores", through="incidente_implicado_actor"
    )


class Actuacion(Model):
    codigo = fields.IntField(primary_key=True)
    judicatura: fields.ForeignKeyRelation[Incidente] = fields.ForeignKeyField(
        "models.Incidente", related_name="actuaciones"
    )
    fecha = fields.DatetimeField()
    tipo = fields.CharField(max_length=64)
    actividad = fields.TextField()
    nombreArchivo = fields.CharField(max_length=255, null=True)
