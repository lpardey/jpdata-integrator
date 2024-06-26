import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest
from tortoise import Tortoise
from tortoise.contrib.test import _init_db, getDBConfig

from consulta_pj.client import CausasResponse


@pytest.fixture()
async def in_memory_db():
    config = getDBConfig(app_label="models", modules=["consulta_pj.models"])
    await _init_db(config)
    yield
    await Tortoise._drop_databases()


@pytest.fixture
def causas_response() -> CausasResponse:
    return CausasResponse(
        idJuicio="5678",
        nombreDelito="Homicidio",
        fechaIngreso=datetime(2021, 1, 1, tzinfo=timezone.utc),
    )


@pytest.fixture()
def informacion_litigante_data() -> dict[str, Any]:
    filename = Path("tests/fixtures/informacion_litigante.json")
    with open(filename, "r") as f:
        return json.load(f)
