import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest
from tortoise import Tortoise
from tortoise.contrib.test import _init_db, getDBConfig

from consulta_pj.client import CausasResponse
from consulta_pj.crawler.schemas import InformacionLitigante


@pytest.fixture()
async def in_memory_db():
    config = getDBConfig(app_label="models", modules=["consulta_pj.db_service.models"])
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


def read_informacion_litigante(cedula: str) -> dict[str, Any]:
    filename = Path(f"tests/fixtures/informacion_litigante_{cedula}.json")
    with open(filename, "r") as f:
        return json.load(f)


@pytest.fixture
def raw_informacion_litigante_1234() -> dict[str, Any]:
    return read_informacion_litigante("1234")


@pytest.fixture
def raw_informacion_litigante_5678() -> dict[str, Any]:
    return read_informacion_litigante("5678")


@pytest.fixture
def informacion_litigante_1234(raw_informacion_litigante_1234: dict[str, Any]) -> InformacionLitigante:
    data = InformacionLitigante(**raw_informacion_litigante_1234)
    return data


@pytest.fixture
def informacion_litigante_5678(raw_informacion_litigante_5678: dict[str, Any]) -> InformacionLitigante:
    data = InformacionLitigante(**raw_informacion_litigante_5678)
    return data
