import logging

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .routers import causas_router, healthcheck_router, litigantes_router, statistics_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Prueba Tusdatos.co")

app.include_router(healthcheck_router)
app.include_router(statistics_router)
app.include_router(litigantes_router)
app.include_router(causas_router)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["consulta_pj.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
