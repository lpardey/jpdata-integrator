from .causas import router as causas_router
from .healthcheck import router as healthcheck_router
from .litigantes import router as litigantes_router
from .stats import router as statistics_router

__all__ = ["healthcheck_router", "statistics_router", "litigantes_router", "causas_router"]
