from . import crawler
from .schemas import (
    ActuacionSchema,
    CausaSchema,
    ImplicadoSchema,
    IncidenteSchema,
    InformacionLitigante,
    JudicaturaSchema,
    LitiganteSchema,
    LitiganteTipo,
    MovimientoSchema,
)

__all__ = [
    "crawler",
    "CausaSchema",
    "ActuacionSchema",
    "LitiganteTipo",
    "JudicaturaSchema",
    "IncidenteSchema",
    "LitiganteSchema",
    "ImplicadoSchema",
    "InformacionLitigante",
    "MovimientoSchema",
]
