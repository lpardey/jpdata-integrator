import logging

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from consulta_pj.settings import get_settings

from .routers import causas_router, healthcheck_router, litigantes_router, statistics_router

logging.basicConfig(level=logging.INFO)

settings = get_settings()
app = FastAPI(title=settings.app_title)

app.include_router(healthcheck_router)
app.include_router(statistics_router)
app.include_router(litigantes_router)
app.include_router(causas_router)

register_tortoise(
    app,
    db_url=settings.db_uri,
    modules={"models": ["consulta_pj.db_service.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
