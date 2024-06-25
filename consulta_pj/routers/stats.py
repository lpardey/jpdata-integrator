from fastapi import APIRouter

from consulta_pj.models import Actuacion, Causa, Implicado, Incidente, Litigante, Movimiento

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("")
async def get_stats() -> dict[str, int]:
    return {
        "litigantes": await Litigante.all().count(),
        "causas": await Causa.all().count(),
        "movimientos": await Movimiento.all().count(),
        "actuaciones": await Actuacion.all().count(),
        "incidentes": await Incidente.all().count(),
        "implicados": await Implicado.all().count(),
    }
